from datetime import datetime

from weather.dates import daterange
from weather.dataset import save_data, open_data, create_dataset, Column, FloatColumn, IntColumn
from weather.usgs import RiverLocation

CONDITIONS = ['CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'VV']

def main():
    RIVERS = {}
    RIVERS['FTTV'] = RiverLocation('FTTV', '41.54.29.82', '72.45.33.67', data_file='USGS_farmington_tariffville')
    RIVERS['SBWS'] = RiverLocation('SBWS', '41.57.39.02', '72.42.37.75', data_file='USGS_stony_brook_west_suffield')
    RIVERS['CTTV'] = RiverLocation('CTTV', '41.59.14', '72.36.21', data_file='USGS_ct_thomsonville')
    RIVERS['BBBB'] = RiverLocation('BBBB', '41.54.50.03', '72.32.58.92', data_file='USGS_broadbrook_broadbrook')
   
    AIRPORT_COLUMNS = ['HourlyAltimeterSetting', 'HourlyDewPointTemperature', 'HourlyDryBulbTemperature',
                       'HourlyPrecipitation', 'HourlyRelativeHumidity', 'HourlySeaLevelPressure',
                       'HourlyStationPressure', 'HourlyVisibility', 'HourlyWetBulbTemperature',
                       'HourlyWindDirection', 'HourlyWindSpeed', 'HourlySkyConditions']
    
    COMBINED = {}
    COMBINED_COLUMNS = setup_columns(RIVERS, COMBINED, AIRPORT_COLUMNS)
    
    setup_river_data(RIVERS, COMBINED_COLUMNS, COMBINED)
    setup_airport_data(AIRPORT_COLUMNS, COMBINED, COMBINED_COLUMNS)
    
    save_dataset(COMBINED, COMBINED_COLUMNS, RIVERS)
    
    RIVERS = [(r.code, r.lat, r.long, r.data) for r in RIVERS.values()]
    save_data('data/rivers.data', RIVERS) 
    
def setup_columns(RIVERS, COMBINED, AIRPORT_COLUMNS):
    COMBINED_COLUMNS = []
    for r in RIVERS.keys():
        COMBINED_COLUMNS.append('{}_Discharge'.format(r))
        COMBINED_COLUMNS.append('{}_GageHeight'.format(r))
        
    COMBINED_COLUMNS += AIRPORT_COLUMNS
    
    for d in all_datetimes():
        COMBINED[d] = ['x'] * len(COMBINED_COLUMNS)
    
    return COMBINED_COLUMNS

def setup_river_data(RIVERS, COMBINED_COLUMNS, COMBINED):
    for r in RIVERS.keys():
        river = RIVERS[r]
        discharge_col = COMBINED_COLUMNS.index('{}_Discharge'.format(r))
        gageheight_col = COMBINED_COLUMNS.index('{}_GageHeight'.format(r))
        for i in range(len(RIVERS[r]['Discharge'])):
            dt = datetime.strptime(river['datetime'][i], '%m/%d/%Y %H:%M')
            if dt.minute == 45:
                COMBINED[dt][discharge_col] = river['Discharge'][i]
                COMBINED[dt][gageheight_col] = river['GageHeight'][i]
                
def setup_airport_data(AIRPORT_COLUMNS, COMBINED, COMBINED_COLUMNS):
    data = open_data('data/NOAA_hourly.data')
    for i in range(len(data[AIRPORT_COLUMNS[0]])):
        dt = datetime.strptime(data['DATE'][i][:-3], '%Y-%m-%dT%H:%M').replace(minute=45)
        for c in AIRPORT_COLUMNS:
            n = COMBINED_COLUMNS.index(c)
            COMBINED[dt][n] = data[c][i]
                
def save_dataset(COMBINED, COMBINED_COLUMNS, RIVERS):
    TRANSPOSED = {}
    TRANSPOSED['DateTime'] = [d for d in COMBINED.keys()]   
    for i, c in enumerate(COMBINED_COLUMNS):
       TRANSPOSED[c] = [x[i] for x in COMBINED.values()]
    
    columns = []
    columns.append(Column('DateTime'))
    for c in ['Discharge', 'GageHeight']:
        for r in RIVERS.keys():
            columns.append(FloatColumn('{}_{}'.format(r, c)))
            
    columns.append(FloatColumn('HourlyAltimeterSetting'))
    columns.append(IntColumn('HourlyDewPointTemperature'))
    columns.append(IntColumn('HourlyDryBulbTemperature'))
    columns.append(FloatColumn('HourlyPrecipitation')
        .set_preprocess(lambda x: x.replace('s', '')))
    columns.append(IntColumn('HourlyRelativeHumidity'))
    columns.append(FloatColumn('HourlySeaLevelPressure'))
    columns.append(FloatColumn('HourlyStationPressure'))
    columns.append(FloatColumn('HourlyVisibility')
        .set_preprocess(lambda x: x.replace('V', '')))
    columns.append(IntColumn('HourlyWetBulbTemperature'))
    columns.append(IntColumn('HourlyWindDirection')
        .set_preprocess(lambda x: x.replace('VRB', '0')))
    columns.append(IntColumn('HourlyWindSpeed'))
    
    cond = Column('HourlySkyConditions')
    cond.set_filter(lambda c: condition_index(c) >= 0)
    cond.set_process(condition_index)
    columns.append(cond)
    
    DATASET = create_dataset(TRANSPOSED, columns)
    
    save_data('data/full.data', DATASET) 
    
def condition_index(c):
    def get_name(c):
        i = c.find(':')
        if i >= 0:
            name = c[(i-3):i]
            name2 = c[(i-2):i]
            if (name2 == 'VV'):
                return 'VV'
            else:
                return name if len(name) == 3 else ''
        else:
            return ''
    try:
        return CONDITIONS.index(get_name(c))
    except:
        return -1

def all_datetimes():
    return [d for d in daterange(datetime(2010, 11, 9, 0, 0), datetime(2019, 11, 9, 23, 45))]

main()
