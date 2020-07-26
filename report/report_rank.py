import requests
import config


def report_rank(rank: int):
    url = config.BASE_URL + 'add_rank'
    params = dict(api_key=config.API_KEY, group_id=config.GROUP_ID, rank=rank)
    result = requests.get(url, params=params)
    print(result)
