from posixpath import splitext
from flask import Flask, json, request, send_file, abort, make_response, redirect
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
    all_files=set(os.listdir(CONFIG['filedir']))

    old_songs = list(filter(lambda x: x.filename in all_files, AllSongsResource.all))
    new_songs = [Song(os.path.abspath(os.path.join(CONFIG["filedir"],s))) for s in all_files-set([o.filename for o in old_songs])]
    AllSongsResource.all = [*old_songs, *new_songs] 
    return list(sorted(AllSongsResource.all, key= lambda k: k.filename.lower()))

#def grab_songs():
#    Song.LAST_ID = 0
#    #all_files=[os.patj.abspath(os.path.join(CONFIG['filedir'],p)) for p in  os.listdir(CONFIG['filedir'])]
#    all_files=os.listdir(CONFIG['filedir'])
#    audio_files=set([os.path.join(CONFIG['filedir'],f) for f in list(filter(lambda b: os.path.splitext(b)[-1].lower() in AUDIO_EXTENSIONS, all_files))])
#    not_present = audio_files - set(AllSongsResource.get_all("path"))
#
#    return list(sorted([*list(filter(lambda b: b.path in audio_files, AllSongsResource.get_all())), *[Song(g) for g in not_present]],key= lambda x: x.filename.lower()))

def prep_songs_for_json(songs: Song):
    #return [{k:v for k,v in song.items() if k not in Song.SKIP_ITER} for song in songs]
    return songs

class SongResource(Resource):
    def get(self, song):
        songpath = os.path.join(CONFIG['filedir'], song)
        if os.path.exists(songpath) and os.path.dirname(songpath) == CONFIG["filedir"]:
            return send_file(songpath)
        abort(400)

class AllSongsResource(Resource):
    all = []
    
    @staticmethod
    def get_all(what=None):
        return AllSongsResource.all if not what else [x.__dict__[what] for x in AllSongsResource.all]
        
    def get(self):
        AllSongsResource.__all = grab_songs()
        #return {"songs":prep_songs_for_json(AllSongsResource.get_all())}
        return {"songs":[dict(d) for d in AllSongsResource.get_all()]}

class CoverResource(Resource):
    def get(self, song):
        songpath = os.path.join(CONFIG["filedir"], song)
        if os.path.dirname(songpath) == CONFIG["filedir"] and os.path.exists(songpath):
            s = Song(os.path.join(CONFIG['filedir'], song))
            response = make_response(s.id3["APIC:"].data)
            response.headers.set('Content-Type', 'image/jpeg')
            #response.headers.set(
            #    'Content-Disposition', 'attachment', filename='cover.jpg')
            return response
        else:
            abort(404)


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

@app.route("/")
def rediirect():
    return redirect("/api/v1.0/songs")

if __name__ == "__main__":
    config()
    app.run(debug=True, host="0.0.0.0", port=8080)
