# Basis-Image, das auf dem Raspberry Pi läuft (ARM-Architektur beachten)
FROM python:3.9-slim-buster

# Installiere System-Abhängigkeiten für Audio und Python-Pakete
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt 

# Erstelle Arbeitsverzeichnis
WORKDIR /usr/src/app

# Kopiere Python-Skript in das Arbeitsverzeichnis
COPY . .

# Setze den Container-Einstiegspunkt
CMD ["python", "./src/speech_2_text/main.py"]