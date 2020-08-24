import requests
import config
from typing import Dict


def login(username: str, password: str) -> Dict:
    url = config.BASE_URL + '/v1/auth/login'
    json = dict(username=username, password=password)
    r = requests.post(url, json=json)
    return dict(auth=r.json()['jwt'])
