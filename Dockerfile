# Basis-Image, das auf dem Raspberry Pi läuft (ARM-Architektur beachten)
FROM python:3.9

# Installiere System-Abhängigkeiten für Audio und Python-Pakete
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libtiff5-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pyaudio
RUN pip install pygame==2.0.0
#RUN python pyaudio/setup.py install
# Erstelle Arbeitsverzeichnis
WORKDIR /usr/src/app
# Kopiere Python-Skript in das Arbeitsverzeichnis
COPY . .
# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt 

# Setze den Container-Einstiegspunkt
CMD ["python", "./src/speech_2_text/main.py"]