import requests
from config import Config


def do_fetch(header: dict) -> bool:
    url = Config().BASE_URL + '/v1/user/get_ocr_status'
    result = requests.get(url, headers=header).text
    return result == 'True'


def stop_fetch(header: dict):
    url = Config().BASE_URL + '/v1/user/get_ocr_status'
    json = dict(status=False)
    requests.post(url, headers=header, json=json)
