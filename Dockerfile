FROM python:3.9-slim
WORKDIR /workdir
RUN apt-get update && apt-get -y install \
    curl \
    pulseaudio \
    ffmpeg \
    xvfb \
    firefox-esr
COPY . .
RUN pip install -r requirements.txt
RUN sh ./sources/get_geckodriver.sh