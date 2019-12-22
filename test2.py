import json
import requests

r = requests.get('https://waterdata.usgs.gov/nwis/uv?cb_00060=on&cb_00065=on&format=rdb&site_no=01189995&period=&begin_date=2019-12-09&end_date=2019-12-16')

print(dir(r))
with open('result.txt', 'wb') as file:
    file.write(r.content)
