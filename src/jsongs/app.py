from posixpath import splitext
from flask import Flask, json, request, send_file, abort, jsonify, make_response
from flask.helpers import make_response
from flask_restful import Resource, Api, reqparse
from .song import Song
import os, json

app = Flask(__name__)
api = Api(app, prefix="/api/v1.0/")

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name')

AUDIO_EXTENSIONS=[".mp3", ".wav", ".mp2"]
CONFIG = None


def grab_songs():
    Song.LAST_ID = 0
    all_files=os.listdir(os.path.realpath(CONFIG['filedir']))
    audio_files= list(filter(lambda b: os.path.splitext(b)[-1].lower() in AUDIO_EXTENSIONS, all_files))
    return [Song(os.path.join(CONFIG['filedir'],f)) for f in audio_files]


class SongResource(Resource):
    def get(self, song):
        songpath = os.path.join(CONFIG['filedir'], song)
        if os.path.exists(songpath):
            return send_file(songpath)
        abort(400)

class AllSongsResource(Resource):
    def get(self):
        return {"songs":[dict(s) for s in grab_songs()]}

class CoverResource(Resource):
    def get(self, song):
        s = Song(os.path.join(CONFIG['filedir'], song))
        response = make_response(s.id3["APIC:"].data)
        response.headers.set('Content-Type', 'image/jpeg')
        #response.headers.set(
        #    'Content-Disposition', 'attachment', filename='cover.jpg')
        return response


api.add_resource(SongResource, "/songs/<string:song>")
api.add_resource(AllSongsResource, "/songs")
api.add_resource(CoverResource, "/cover/<string:song>")

def config(configfile=None):
    global CONFIG
    if not configfile or not os.path.exists(os.path.realpath(configfile)): 
        configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    if not os.path.exists(configfile):
        print("Please create a config file")
        exit(1)
    with open(configfile, "r") as config:
        CONFIG=json.loads(config.read())
        CONFIG["filedir"]=os.path.realpath(CONFIG["filedir"])
    print(CONFIG)


if __name__ == "__main__":
    config()
    app.run(debug=True, host="0.0.0.0", port=8080)
