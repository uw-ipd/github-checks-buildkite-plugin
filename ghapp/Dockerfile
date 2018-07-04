FROM alpine:latest
RUN apk add --no-cache python3 py3-cryptography bash

COPY . /ghapp

RUN pip3 install /ghapp
