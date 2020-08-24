import requests
import config
import warnings


def report_rank(rank: int):
    url = config.BASE_URL + 'add_rank'
    params = dict(api_key=config.API_KEY, group_id=config.GROUP_ID, rank=rank)
    result = requests.get(url, params=params)
    message = '-----现在的排名：' + str(rank) + '-----------'
    warnings.warn(message)
    print(result)
