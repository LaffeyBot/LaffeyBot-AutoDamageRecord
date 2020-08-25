import json


class Config:
    def __init__(self):
        with open('config.json') as config_file:
            data = json.load(config_file)
            self.BASE_URL = data['BASE_URL']
            self.USERNAME = data['USERNAME']
            self.PASSWORD = data['PASSWORD']
            self.FETCH_INTERVAL = data['FETCH_INTERVAL']
