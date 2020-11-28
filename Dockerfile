FROM ubuntu:18.04
RUN apt-get update

RUN apt-get install -y wget && \
    apt install python3 -y && \
    apt-get install -y python3-pip && \
    apt-get install -y tmux && \
    apt-get install -y build-essential curl file git && \
    
ADD * /home/
