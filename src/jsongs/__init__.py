"""Jsonify songs contained in a folder and make them available via an API,"""

import sys
from sys import argv
import os

from .app import *
from .create_config import *


if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "jsongs"
    __version__ = "0.1.1"
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError




def main():
    CONF=None
    if "--create-config" in argv:
        try:
            CFILE=argv[argv.index('--create-config')+1]
            if os.path.exists(CFILE) and input("The file already exists! DO YOU WANT TO OVERWRITE IT (y/N): ").lower() != "y": exit(1)
            #with open(CFILE, "w") as file:
            #    file.write(json.dumps({'musicdir':'MUSIC_DIR_PATH_HERE'}))
        except IndexError:
            create_config(None, example=("--example-config" in argv))
            exit(0)
        create_config(CFILE, example=("--example-config" in argv))
        exit(0)
    if "-c" in argv:
        CONF=config(argv[argv.index("-c")+1])
    elif "--config" in argv:
        CONF=config(argv[argv.index("--config")+1])
    elif os.environ['JSONGS_CONFIG_FILE']:
        CONF=config(os.environ['JSONGS_CONFIG_FILE'])
    else:
        CONF=config(None)
    if not CONF:
        app.run(debug=False, threaded=True, port= 8080, host="0.0.0.0")
    app.run(debug=CONF['debug'], threaded=True, port= CONF['port'], host="0.0.0.0")
