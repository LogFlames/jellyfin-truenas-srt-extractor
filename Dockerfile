FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip
RUN pip3 install watchdog

RUN apt-get update && \
    apt-get install -y wget gnupg apt-transport-https cargo libleptonica-dev libtesseract-dev clang pkg-config

RUN apt-get update && \
    apt-get install -y tesseract-ocr-eng tesseract-ocr-swe tesseract-ocr-spa tesseract-ocr-nor tesseract-ocr-dan tesseract-ocr-fin tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-isl

RUN wget -O /usr/share/keyrings/gpg-pub-moritzbunkus.gpg https://mkvtoolnix.download/gpg-pub-moritzbunkus.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gpg-pub-moritzbunkus.gpg] https://mkvtoolnix.download/ubuntu/ jammy main" | tee /etc/apt/sources.list.d/mkvtoolnix.download.list
RUN echo "deb-src [arch=amd64 signed-by=/usr/share/keyrings/gpg-pub-moritzbunkus.gpg] https://mkvtoolnix.download/ubuntu/ jammy main" | tee -a /etc/apt/sources.list.d/mkvtoolnix.download.list

RUN apt-get update && \
    apt-get install -y mkvtoolnix

RUN cargo install --git https://github.com/elizagamedev/vobsubocr

RUN mkdir -p /home/srt_extractor
RUN mkdir -p /home/watching

ENV PYTHONUNBUFFERED=1

WORKDIR /home/srt_extractor

COPY . .

CMD [ "python3", "main.py" ]
