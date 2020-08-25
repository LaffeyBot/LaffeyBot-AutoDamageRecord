import requests
from config import Config


def report_damage(damage_list: list, auth_header: dict):
    url = Config().BASE_URL + '/v1/record/add_record_if_needed'
    params = dict(nickname=damage_list[0], damage=damage_list[2])
    result = requests.post(url, json=params, headers=auth_header)
    print(result.text)
