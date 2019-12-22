import requests
from pprint import pprint

uri = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets'
headers = {'token': 'GXVZhqHZGNxUJyWNQNTRYlxBuNGWjZvr'}

r = requests.get(uri, headers=headers)
pprint(r.json())
