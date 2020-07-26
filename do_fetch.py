import requests
import config


def do_fetch() -> bool:
    url = config.BASE_URL + 'fetch_status?group_id=' + config.GROUP_ID
    result = requests.get(url).text
    return result == 'True'
