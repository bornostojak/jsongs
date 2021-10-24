from .app import *
from sys import argv
import os

if __name__ == "__main__":
    if "--create-config" in argv:
        CFILE=argv[argv.index('--create-config')+1]
        if os.path.exists(CFILE) and input("The file already exists! DO YOU WANT TO OVERWRITE IT (y/N): ").lower() != "y": exit(1)
        with open(CFILE, "w") as file:
            file.write(json.dumps({'musicdir':'MUSIC_DIR_PATH_HERE'}))
        exit(0)
    if "-c" in argv:
        config(argv[argv.index("-c")+1])
    elif "--config" in argv:
        config(argv[argv.index("--config")+1])
    elif os.environ['JSONGS_CONFIG_FILE']:
        config(os.environ['JSONGS_CONFIG_FILE'])
    else:
        config()
    app.run(debug=False, threaded=True, port= 8080, host="0.0.0.0")
