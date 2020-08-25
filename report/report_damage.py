import requests
import config


def report_damage(damage_list: list, auth_header: dict):
    url = config.BASE_URL + '/v1/record/add_record_if_needed'
    params = dict(group_id=config.GROUP_ID, nickname=damage_list[0], damage=damage_list[2])
    print(params)
    result = requests.post(url, json=params, headers=auth_header)
    print(result.text)
