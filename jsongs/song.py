from os import execle, listdir, path as ospath
from mutagen.id3 import ID3

from flask.helpers import send_file
from dataclasses import dataclass
from urllib.parse import quote

@dataclass()
class SongBase:
    name: str
    author: str
    url: str

class Song(object):
    VERSION="v1.0"
    LAST_ID=0
    SKIP_ITER=["id", "path", "filename", "file_format", "extension", "id3"]
    DEFAULT_COVER_URL=""

    def __init__(self, path=None, file_format=None):
        super().__init__()
        self.id = Song.LAST_ID = Song.LAST_ID+1
        self.path = path
        self.filename = ""
        self.title = ""
        self.author = ""
        self.cover= Song.DEFAULT_COVER_URL
        self.extension = ""
        self.id3 = None
        if path != None:
            self.filename = ospath.basename(path)
            self.title = ospath.splitext(self.filename)[0]
            self.extension = ospath.splitext(self.filename)[-1][1:]
            if self.extension.lower() == "mp3":
                try:
                    self.id3 = ID3(self.path)
                    self.title = ", ".join(self.id3['TIT2'].text)
                    self.author = ", ".join(self.id3['TPE1'].text)
                    if "APIC:" in self.id3 and len(self.id3['APIC:'].data) > 1024:
                        self.cover = "/api/{}/cover/".format(Song.VERSION)+quote(self.filename)
                except Exception:
                    pass
        self.url = "/api/{}/songs/".format(Song.VERSION)+quote(self.filename)
        self.file_format = file_format

    def __iter__(self):
        for i,k in self.__dict__.items():
            if not i in Song.SKIP_ITER:
                yield i,k
    
    def __repr__(self):
        return repr(dict(self))
    
    @staticmethod
    def get_songs_from_drectory(path):
        c=0
        return [Song(path=ospath.join(ospath.abspath(path),s)) for s in listdir(ospath.abspath(path))]

