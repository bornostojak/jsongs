from json import dumps
from sys import stdout, stderr

def create_config(file: str, example:bool = False) -> None:
    config = {
        "musicdir":(str, "Please define the directory for the music files", "FULL_MUSIC_DIR_PATH"),
        "port": (int, "Please define the port for the server", 8080),
        "debug": (bool, "user debugging (y/N)", False)
    }
    if example:
        stdout.write(dumps({v:k[2] for v,k in config.items()}))
        return

    new_config = {}
    for k,v in config.items():
        value = None
        if v[0] == bool:
            stderr.write(f"{v[1]}: ")
            value = True if input().lower() == "y" else False
        else:
            value = v[0](input(f"{v[1]}: "))
         
        new_config[k] = value
    
    stdout.write(dumps(new_config))
    if file:
        with open(file, 'w') as f:
            f.write(dumps(new_config))