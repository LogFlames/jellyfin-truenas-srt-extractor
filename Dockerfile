FROM alpine:3.20

RUN apt-get update

RUN apt-get install -y python3

RUN mkdir -p /home/src_extractor

WORKDIR /home/src_extractor

COPY . .

CMD [ "python3", "main.py" ]