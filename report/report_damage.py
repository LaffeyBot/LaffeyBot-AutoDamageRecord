import requests
import config


def report_damage(damage_list: list):
    url = config.BASE_URL + 'add_attack_record'
    params = dict(api_key=config.API_KEY, group_id=config.GROUP_ID, username=damage_list[0], damage=damage_list[2])
    result = requests.get(url, params=params)
    print(result.text)
    # print(result.request.url)
