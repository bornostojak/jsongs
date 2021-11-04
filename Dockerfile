FROM python:3.9-alpine

RUN mkdir -p /musicdir /config

WORKDIR /home/jsongs
COPY src/jsongs /home/jsongs/jsongs
COPY requirements.txt /home/jsongs/requirements.txt

RUN echo '{"musicdir": "/musicdir", "port": 8080, "debug":false, "nossl":false, "ssl_cert": "", "ssl_privkey": ""}' > /config/config.json
RUN apk add gcc
RUN apk add --no-cache libressl-dev musl-dev libffi-dev
RUN pip install -r /home/jsongs/requirements.txt

ENV JSONGS_CONFIG_FILE "/config/config.json"
ENV NO_SSL 0
EXPOSE 8080
CMD ["python3", "-m", "jsongs"]
