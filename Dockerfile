FROM ubuntu:22.10

RUN apt update

RUN apt install -y hugin

WORKDIR stitcher_app

COPY panorama.py /usr/bin/panorama.py
COPY panostitch.pto panostitch.pto
