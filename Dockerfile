FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip
RUN pip3 install watchdog

RUN deb [arch=amd64 signed-by=/usr/share/keyrings/gpg-pub-moritzbunkus.gpg] https://mkvtoolnix.download/ubuntu/ jammy main
RUN deb-src [arch=amd64 signed-by=/usr/share/keyrings/gpg-pub-moritzbunkus.gpg] https://mkvtoolnix.download/ubuntu/ jammy main

RUN apt-get update
RUN apt-get install -y mkvtoolnix

RUN mkdir -p /home/src_extractor
RUN mkdir -p /home/watching

WORKDIR /home/src_extractor

COPY . .

CMD [ "python3", "main.py" ]
