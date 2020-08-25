import requests
from config import Config
from typing import Dict


def login(username: str, password: str) -> Dict:
    url = Config().BASE_URL + '/v1/auth/login'
    json = dict(username=username, password=password)
    r = requests.post(url, json=json)
    print(r.text)
    return dict(auth=r.json()['jwt'])
