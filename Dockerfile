FROM python:3.9-alpine

RUN mkdir -p /musicdir /config /etc/jsongs

WORKDIR /home/jsongs
COPY src/jsongs /home/jsongs/jsongs
COPY requirements.txt /home/jsongs/requirements.txt
COPY config/config.json /etc/jsongs/config.json

RUN apk add gcc && \
apk add --no-cache libressl-dev musl-dev libffi-dev && \
pip install -r /home/jsongs/requirements.txt && \
pip install gunicorn 

COPY config/run.sh /run.sh

ENV JSONGS_CONFIG "/config/config.json"
ENV PORT 8080

EXPOSE 8080
CMD ["sh", "/run.sh"]
