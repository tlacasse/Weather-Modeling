from weather.dataset import open_data, save_data, clean_dataset, Column, FloatColumn, IntColumn
from weather.source import all_datetimes, get_airports, get_selected_river_sites
from weather.usgs import GAGE_HEIGHT, GAGEHEIGHT_TEMPLATE
from weather.noaa import condition_index
from datetime import datetime
from pprint import pprint

river_sites = get_selected_river_sites()
airports = {}
airport_keys = {}
for a in get_airports():
    airports[a] = open_data('data/noaa/airports/{}.data'.format(a))
    airport_keys[a] = [k for k in airports[a].keys() if k[:6] == 'Hourly']

print('LIST COLUMNS')
columns = []
for a in airports.keys():
    for k in airport_keys[a]:
        columns.append('{}_{}'.format(a, k))
for s, v in river_sites:
    columns.append(GAGEHEIGHT_TEMPLATE.format(s.key))

data = {}
for d in all_datetimes():
    data[d] = ['x'] * len(columns)

print(columns)

###############################################################################

print('FILL COLUMNS')

def noaa_to_datetime(s):
    return datetime.strptime(s[:-3], '%Y-%m-%dT%H:%M').replace(minute=45)

def usgs_to_datetime(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M')

print('FILL COLUMNS - NOAA')
for a in airports.keys():
    print(a)
    for k in airport_keys[a]:
        out_col_index = columns.index('{}_{}'.format(a, k))
        for i in range(len(airports[a][k])):
            dt = noaa_to_datetime(airports[a]['DATE'][i])
            data[dt][out_col_index] = airports[a][k][i]

print('FILL COLUMNS - USGS')
for s, v in river_sites:
    print(s.name)
    out_col_index = columns.index(GAGEHEIGHT_TEMPLATE.format(s.key))
    site_data = open_data('data/usgs/sites/{}.data'.format(s.key))
    site_names = open_data('data/usgs/sites/{}.names'.format(s.key))
    gageheight_header = [h for h in site_names if h[-6:] == '_' + GAGE_HEIGHT][0]
    
    for i in range(len(site_data[list(site_data.keys())[0]])):
        dt = usgs_to_datetime(site_data['datetime'][i])
        # NOAA data is at minute 51
        if dt.minute == 45:
            data[dt][out_col_index] = site_data[gageheight_header][i]
  
###############################################################################
          
print('CLEAN DATA')
print('transpose')

transposed = {}
transposed['DateTime'] = [d for d in data.keys()]   
for i, c in enumerate(columns):
   transposed[c] = [x[i] for x in data.values()]
data = transposed

print('specify columns')

columns = []
columns.append(Column('DateTime'))

def zero_if_blank(s):
    return '0' if s == '' else s

for a in airports.keys():
    a = a + '_'
    
    columns.append(FloatColumn(a + 'HourlyAltimeterSetting')
        .set_preprocess(lambda x: x.replace('s', '')))
    columns.append(IntColumn(a + 'HourlyDewPointTemperature')
        .set_preprocess(lambda x: x.replace('s', '')))
    columns.append(IntColumn(a + 'HourlyDryBulbTemperature')
        .set_preprocess(lambda x: x.replace('s', '')))
    columns.append(FloatColumn(a + 'HourlyPrecipitation')
        .set_preprocess(lambda x: zero_if_blank(x.replace('s', ''))))
    columns.append(IntColumn(a + 'HourlyRelativeHumidity'))
    columns.append(IntColumn(a + 'HourlyWetBulbTemperature'))
    columns.append(IntColumn(a + 'HourlyWindDirection')
        .set_preprocess(lambda x: zero_if_blank(x.replace('VRB', '0'))))
    columns.append(IntColumn(a + 'HourlyWindSpeed')
        .set_preprocess(lambda x: zero_if_blank(x.replace('s', ''))))
    
    cond = Column(a + 'HourlySkyConditions')
    cond.set_preprocess(condition_index)
    cond.set_filter(lambda c: c >= 0)
    columns.append(cond)

for s, v in river_sites:
    columns.append(FloatColumn(GAGEHEIGHT_TEMPLATE.format(s.key)))

print('clean data')
print(len(data['DateTime']))
data, fails = clean_dataset(data, columns)
print(len(data['DateTime']))
save_data('data/full.data', data) 
save_data('data/full.fails', fails) 

print()
print('FAILS')
pprint({k: len(v) for k, v in fails.items()})
