from json import dumps 

def create_config(file: str) -> None:
    config = {
        "musicdir":(str, "Please define the directory for the music files"),
        "port": (int, "Please define the port for the server"),
        "debug": (bool, "user debugging (y/N)")
    }

    new_config = {}
    for k,v in config.items():
        value = None
        if v[0] == bool:
            value = True if input(f"{v[1]}: ").lower() == "y" else False
        else:
            value = v[0](input(f"{v[1]}: "))
         
        new_config[k] = value
    with open(file, 'w') as f:
        f.write(dumps(new_config))