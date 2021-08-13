FROM ubuntu:20.04

WORKDIR /app

COPY . .

RUN apt update
RUN apt install python3 python3-pip -y
RUN pip3 install -r requirements.txt

EXPOSE 6789