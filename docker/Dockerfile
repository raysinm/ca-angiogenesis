FROM ubuntu:latest 

RUN apt update && \
    apt upgrade  -y

RUN apt install -y python3-dev python3-pip


COPY ./src /opt/src


RUN pip3 install numpy \
                matplotlib \
                pandas

