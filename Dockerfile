FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip
RUN pip3 install watchdog

RUN apt-get update && \
    apt-get install -y wget gnupg apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O /usr/share/keyrings/gpg-pub-moritzbunkus.gpg https://mkvtoolnix.download/gpg-pub-moritzbunkus.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gpg-pub-moritzbunkus.gpg] https://mkvtoolnix.download/ubuntu/ jammy main" | tee /etc/apt/sources.list.d/mkvtoolnix.download.list
RUN echo "deb-src [arch=amd64 signed-by=/usr/share/keyrings/gpg-pub-moritzbunkus.gpg] https://mkvtoolnix.download/ubuntu/ jammy main" | tee -a /etc/apt/sources.list.d/mkvtoolnix.download.list

RUN apt-get update && \
    apt-get install -y mkvtoolnix && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/src_extractor
RUN mkdir -p /home/watching

WORKDIR /home/src_extractor

COPY . .

CMD [ "python3", "main.py" ]
