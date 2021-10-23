FROM python:3.9-alpine

RUN mkdir -p /home/jsongs/musicdir 

WORKDIR /home/jsongs
COPY jsongs /home/jsongs/jsongs
COPY requirements.txt /home/jsongs/requirements.txt

RUN echo '{"musicdir": "/home/jsongs/musicdir"}' > /home/jsongs/default_config.json
RUN pip install -r /home/jsongs/requirements.txt

ENV JSONGS_CONFIG_FILE "/home/jsongs/default_config.json"
EXPOSE 8080
ENTRYPOINT ["python3", "-m", "jsongs"]
