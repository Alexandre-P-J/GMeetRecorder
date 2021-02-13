FROM python:3.9-slim
WORKDIR /workdir
RUN apt-get update && apt-get -y install \
    curl \
    pulseaudio \
    ffmpeg \
    xvfb \
    firefox-esr
COPY . .
RUN sh ./sources/get_geckodriver.sh
RUN pip install -r requirements.txt
#RUN adduser root pulse-access
CMD ["sh", "./sources/driver.sh"]