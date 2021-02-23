import json

defaults = {
    "app": {
        "environment": "local",
        "debug": "True",
        "cors": "http://localhost:3000",
        "db_path": "../db_example.json"
    },
    "influx": {
        "host": "192.168.1.10",
        "port": 8086,
        "username": "",
        "password": "",
        "database": "cenozoaDev"
    },
    "alert": {
        "url": ""
    }
}

configs = {}

class Config:
    def __init__(self, config_path: str, secrets_path: str):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.__dict__.update(config)
        
        with open(secrets_path, 'r') as secrets_path:
            config = json.load(secrets_path)
            self.__dict__.update(config)