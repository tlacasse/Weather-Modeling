
import json
from pprint import pprint
import requests

uri = 'https://waterservices.usgs.gov/nwis/dv/?stateCd={}&format=json'
r = requests.get(uri.format('CT'))
r = str(r.content, 'utf-8')
s = json.loads(r)

x = s['value']['timeSeries'][0]
pprint(x)
x = s['value']['timeSeries'][1]
pprint(x)