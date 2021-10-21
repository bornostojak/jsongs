from .app import *
from sys import argv
import os

if __name__ == "__main__":
    if "-c" in argv:
        config(argv[argv.index("-c")+1])
    elif "--config" in argv:
        config(argv[argv.index("--config")+1])
    else:
        config()
    app.run(debug=False, threaded=True, port= 8080, host="0.0.0.0")