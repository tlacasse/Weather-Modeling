from weather.dataset import Column, IntColumn, FloatColumn, create_dataset, DataSet, open_data

# Want FM-15 Report Type: METAR Aviation routine weather report

def round_to(x, n):
    return int(round( x / n ) * n)
    
CONDITIONS = ['CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'VV']
    
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
    
def _create_weather_dataset(data):
    columns = []
    
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
    
    return create_dataset(data, columns)
 
NAMES = open_data('data/hourly.names')
ALL_DATA = open_data('data/hourly.data')

DATASET = _create_weather_dataset(ALL_DATA)

BIN_SIZE = 5

def _create_humidity_condition_dataset():
    both = zip(DATASET.get_column('HourlyRelativeHumidity'),
               DATASET.get_column('HourlyDewPointTemperature'),
               DATASET.get_column('HourlySkyConditions'))
    return DataSet([[round_to(h, BIN_SIZE), round_to(h, BIN_SIZE), c] for h, t, c in both], 
                     ['HourlyRelativeHumidity', 'HourlyDewPointTemperature', 'HourlySkyConditions'])

DATASET_CONDITION_HUMIDITY = _create_humidity_condition_dataset()
