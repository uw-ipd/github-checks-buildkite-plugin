FROM alpine:latest
RUN apk add --no-cache python3 py3-cryptography

COPY . /ghapp

RUN pip3 install /ghapp
