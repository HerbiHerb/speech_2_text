import os
import pyaudio
import asyncio
import websockets
import json
import time
import requests
import shutil
import regex
import pathlib
import pygame
import yaml
import redis
from dotenv import load_dotenv

# Deepgram ALternative zu Picovoice
# https://www.youtube.com/watch?v=dq4AiiiaAsY
# https://www.raspberrypi.com/news/raspberry-pi-wearable-subtitles/
# https://deepgram.com/learn/building-a-conversational-ai-flow-with-deepgram

# Microphone test on raspi
# https://www.circuitbasics.com/how-to-record-audio-with-the-raspberry-pi/

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# LISTENING_SOUND_PATH = "src\data\listening_sound.wav"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

# terminal_size = shutil.get_terminal_size()
audio_queue = asyncio.Queue()


def callback(input_data, frame_count, time_info, status_flag):
    audio_queue.put_nowait(input_data)
    return (input_data, pyaudio.paContinue)


def check_wake_word_occurance(wake_word: str, text: str):
    matches = regex.findall("(" + wake_word + "){e<=2}", text)
    if len(matches) > 0:
        return True
    else:
        return False


def get_the_user_id_():
    user_id = None
    try:
        user_id = redis_client.get("user_id")
        user_id = json.loads(user_id)
    except Exception as e:
        print(e)
        if os.path.isfile("..../rag_chat_ui/src/chat_ui/static/tmp/tmp_user_file.json"):
            with open() as f:
                json_data = json.load(f)
                user_id = json_data["user_id"]
    return user_id


async def run(key, silence_interval):
    async with websockets.connect(
        "wss://api.deepgram.com/v1/listen?endpointing=true&interim_results=true&encoding=linear16&sample_rate=16000&channels=1",
        extra_headers={"Authorization": "Token {}".format(key)},
    ) as ws:

        async def microphone():
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback,
            )

            stream.start_stream()

            while stream.is_active():
                await asyncio.sleep(0.1)

            stream.stop_stream()
            stream.close()

        async def sender(ws):
            try:
                while True:
                    data = await audio_queue.get()
                    await ws.send(data)
            except Exception as e:
                print("Error while sending: ".format(str(e)))
                raise

        async def receiver(ws):
            transcript = ""
            last_word_end = 0.0
            endpoint_reached = False
            wake_word_occured = False
            listening_sound_played = False

            async for message in ws:
                message = json.loads(message)
                transcript_cursor = message["start"] + message["duration"]
                # if there are any words in the message
                if len(message["channel"]["alternatives"][0]["words"]) > 0:
                    # handle transcript printing for final messages
                    if message["is_final"]:
                        if len(transcript):
                            transcript += " "
                        transcript += message["channel"]["alternatives"][0][
                            "transcript"
                        ]
                        # print(f"Final: {transcript}")
                        wake_word_occured = check_wake_word_occurance(
                            "hey jarvis", transcript
                        )
                        if wake_word_occured and not listening_sound_played:
                            listening_sound_played = True
                            print("Wake word detected")
                            pygame.init()
                            pygame.mixer.init()
                            pygame.mixer.music.load(os.getenv("LISTENING_SOUND_PATH"))
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                pygame.event.pump()
                            pygame.mixer.quit()
                            pygame.quit()

                    # if the last word in a previous message is silence_interval seconds
                    # older than the first word in this message (and if that last word hasn't already triggered a beep)
                    current_word_begin = message["channel"]["alternatives"][0]["words"][
                        0
                    ]["start"]
                    if (
                        current_word_begin - last_word_end >= silence_interval
                        and last_word_end != 0.0
                    ):
                        endpoint_reached = True

                    last_word_end = message["channel"]["alternatives"][0]["words"][-1][
                        "end"
                    ]
                else:
                    # if there were no words in this message, check if the the last word
                    # in a previous message is silence_interval or more seconds older
                    # than the timestamp at the end of this message (if that last word hasn't already triggered a beep)
                    if (
                        transcript_cursor - last_word_end >= silence_interval
                        and last_word_end != 0.0
                    ):
                        last_word_end = 0.0
                        endpoint_reached = True

                if endpoint_reached:
                    if wake_word_occured:
                        print(transcript)
                        user_id = get_the_user_id_()
                        conv_data = requests.post(
                            url=os.environ["HOST_URL"] + "/add_new_speech_query",
                            data=json.dumps(
                                {
                                    "speech_query": transcript,
                                    "user_id": user_id,
                                }
                            ),
                        )
                    endpoint_reached = False
                    wake_word_occured = False
                    listening_sound_played = False
                    # we set/mark last_word_end to 0.0 to indicate that this last word has already triggered a beep
                    last_word_end = 0.0
                    transcript = ""
                    print("End of speech")

        await asyncio.wait(
            [
                asyncio.ensure_future(microphone()),
                asyncio.ensure_future(sender(ws)),
                asyncio.ensure_future(receiver(ws)),
            ]
        )


if __name__ == "__main__":
    load_dotenv()
    with open(
        "config/config.yaml",
        "r",
    ) as file:
        config = yaml.safe_load(file)
        os.environ["HOST_URL"] = config["host_url"]
        os.environ["CHAT_UI_URL"] = config["chat_ui_url"]
    asyncio.get_event_loop().run_until_complete(run(os.getenv("DEEPGRAM_API_KEY"), 5))
