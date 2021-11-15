"""Flask application for song simple song delivery API"""

# pylint: disable=no-self-use,inconsistent-return-statements

import os
from flask import Flask, send_file, abort, make_response, redirect
from flask_restful import Resource, Api, reqparse

from .config_manager import ConfigManager
from .song import Song

app = Flask(__name__)
api = Api(app, prefix="/api/v1.0/")

parser = reqparse.RequestParser()
parser.add_argument("id", type=int)
parser.add_argument("name")

AUDIO_EXTENSIONS = [".mp3", ".wav", ".mp2"]


def configure_app(config: ConfigManager = ConfigManager()) -> ConfigManager:
    """Configure the app"""

    config_file = list(
        filter(
            lambda x: x[0],
            (
                (os.path.exists(path), path)
                for path in (os.environ.get("JSONGS_CONFIG"), "/etc/jsongs/config.json")
                if path
            ),
        )
    )[0][1]

    config = ConfigManager.generate_from_config_file(config_file)

    if os.environ.get("SSL_CERT") and os.environ.get("SSL_PRIVKEY"):
        config.ssl_cert = os.environ.get("SSL_CERT") or config.ssl_cert
        config.ssl_privkey = os.environ.get("SSL_PRIVKEY") or config.ssl_privkey

    return config


CONFIG = configure_app()


def grab_songs() -> list[Song]:
    """Grab songs from the music folder and prep them for the API"""
    all_files = set(os.listdir(CONFIG["musicdir"]))

    old_songs = list(filter(lambda x: x.filename in all_files, AllSongsResource.all))
    new_songs = [
        Song(os.path.abspath(os.path.join(CONFIG["musicdir"], s)))
        for s in all_files - {o.filename for o in old_songs}
        if True in [s.lower().endswith(x) for x in [".mp3", ".mp2", ".wav"]]
    ]
    AllSongsResource.all = [*old_songs, *new_songs]
    return list(sorted(AllSongsResource.all, key=lambda k: k.filename.lower()))


class SongResource(Resource):
    """SongResource class"""

    def get(self, song):
        """Return the song audio data"""
        songpath = os.path.join(CONFIG["musicdir"], song)
        if os.path.exists(songpath) and os.path.dirname(songpath) == CONFIG["musicdir"]:
            return send_file(songpath)
        abort(400)


class AllSongsResource(Resource):
    """Resource class for returnig list of all in music folger through the API"""

    all = []

    @staticmethod
    def get_all(what=None):
        """Return all songs"""
        return (
            AllSongsResource.all
            if not what
            else [vars(x)[what] for x in AllSongsResource.all]
        )

    def get(self):
        """Resolve the GET request for all songs listed in the API"""
        AllSongsResource.all = grab_songs()
        return {"songs": [dict(d) for d in AllSongsResource.get_all()]}


class CoverResource(Resource):
    """Resource class for returnig individual covers for mp3 which contain them in their tags"""

    def get(self, song):
        """Resolve the GET request for a certain songs cover"""
        songpath = os.path.join(CONFIG["musicdir"], song)
        if os.path.dirname(songpath) == CONFIG["musicdir"] and os.path.exists(songpath):
            song_data = Song(os.path.join(CONFIG["musicdir"], song))
            response = make_response(song_data.id3["APIC:"].data)
            response.headers.set("Content-Type", "image/jpeg")
            return response
        abort(404)


api.add_resource(SongResource, "/songs/<string:song>")
api.add_resource(AllSongsResource, "/songs")
api.add_resource(CoverResource, "/cover/<string:song>")


@app.route("/")
def direct():
    """Redirect to the all songs API endpoint from home path"""
    return redirect("/api/v1.0/songs")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
