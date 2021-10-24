FROM python:3.9-alpine

RUN mkdir -p /musicdir 

WORKDIR /home/jsongs
COPY src/jsongs /home/jsongs/jsongs
COPY requirements.txt /home/jsongs/requirements.txt

RUN echo '{"musicdir": "/musicdir"}' > /home/jsongs/default_config.json
RUN pip install -r /home/jsongs/requirements.txt

ENV JSONGS_CONFIG_FILE "/home/jsongs/default_config.json"
EXPOSE 8080
CMD ["python3", "-m", "jsongs"]
