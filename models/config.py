import json
from types import SimpleNamespace


class Config:
    @staticmethod
    def get():
        config_file = open("config.json")
        return json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))
