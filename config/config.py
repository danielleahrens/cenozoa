import json

defaults = {
    "app": {
        "environment": "local",
    },
    "influx": {
        "host": "192.168.1.10",
        "port": 8086,
        "username": "",
        "password": "",
        "database": "cenozoaDev"
    }
}

configs = {}

class Config:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
            self.__dict__.update(config)