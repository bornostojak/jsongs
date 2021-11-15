"""Configuration manager module"""

from json import loads, dumps
from sys import stdout, stderr, exit as sysexit
import os


class ConfigManager:
    """Configuration manager"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Defining singleton configuration manager"""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.musicdir = ""
            for key, val in ConfigManager.BASE_CONFIG.items():
                cls._instance.__dict__[key] = "" if isinstance(val[2], str) else val[2]

            cls._instance.update(**kwargs)
        return cls._instance

    BASE_CONFIG = {
        "musicdir": (
            str,
            "Please define the directory for the music files",
            "FULL_MUSIC_DIR_PATH",
        )
    }

    def keys(self):
        """Return keys"""
        return self.__dict__.keys()

    def values(self):
        """Return values"""
        return self.__dict__.values()

    def __getitem__(self, key):
        """Return property from object"""
        return self.__dict__[key]

    def __setitem__(self, key, item):
        """Set item defined by key with new value 'item'"""
        self.__dict__[key] = item

    def __delitem__(self, key):
        """Delete item in object"""
        del self.__dict__[key]

    def __repr__(self):
        """repr method"""
        return repr(self.__dict__)

    def __len__(self):
        """Return length of items"""
        return len(self.__dict__)

    def clear(self):
        """Reset all items in the object"""
        self.__dict__.update(**type(self).BASE_CONFIG)

    def update(self, **kwargs):
        """Update configuration"""
        for key, val in kwargs.items():
            if key in type(self).BASE_CONFIG:
                self.__dict__[key] = type(self).BASE_CONFIG[key][0](val)

    @staticmethod
    def create_config(file: str) -> None:
        """Create configuration"""

        if (
            os.path.exists(file)
            and input(
                "The file already exists! DO YOU WANT TO OVERWRITE IT (y/N): "
            ).lower()
            != "y"
        ):
            stderr.write("ERROR: Config file was NOT created!")
            sysexit(1)

        new_config = {}
        for key, val in ConfigManager.BASE_CONFIG.items():
            value = None
            if val[0] == bool:
                stderr.write(f"{val[1]}: ")
                value = True if input().lower() == "y" else val[2]
            else:
                value = val[0](input(f"{val[1]}: "))

            new_config[key] = value

        stdout.write(dumps(new_config))
        if file:
            with open(file, "w", encoding="utf-8") as cfgfile:
                cfgfile.write(dumps(new_config))

    @staticmethod
    def print_example_config() -> None:
        """Print example configuration"""
        stdout.write(dumps({k: v[2] for k, v in ConfigManager.BASE_CONFIG.items()}))

    @classmethod
    def generate_from_config_file(cls: type, path: str):
        """Generate confiuration from config file"""
        config = cls()
        with open(path, "r", encoding="utf-8") as file:
            config.update(**loads(file.read()))
        return config
