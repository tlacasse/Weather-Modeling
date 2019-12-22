from weather.dataset import open_data, create_dataset, FloatColumn, Column
from weather.dates import usgs_dates
from datetime import datetime

class RiverLocation:
    
    def __init__(self, lat, long, col_map, data_file):
        self.lat = lat
        self.long = long
        self.col_map = col_map
        self.names = open_data('data/{}.names'.format(data_file))
        self.data = open_data('data/{}.data'.format(data_file))
        
    def __getitem__(self, key):
        return self.col_map[key]
    
    def lat_coord(self):
        return int(self.lat[3:5])
    
    def long_coord(self):
        return int(self.long[3:5])

BROAD_BROOK_BROAD_BROOK = RiverLocation('41.54.50.03', '72.32.58.92', {
          'Discharge': '66854_00060'  # Discharge, cubic feet per second
        , 'GageHeight': '66855_00065' # Gage height, feet
        }, 'USGS_broadbrook_broadbrook')
   
CT_HARTFORD = RiverLocation('41.46.08.74', '72.40.03.18', {
          'GageHeight': '66895_00065' # Gage height, feet
        }, 'USGS_ct_hartford')
         
HOCKANUM_EAST_HARTFORD = RiverLocation('41.46.59', '72.35.16', {
          'SpecificConductance': '210285_00095'    # Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius
        , 'DissolvedOxygen': '210286_00300'        # Dissolved oxygen, water, unfiltered, milligrams per liter
        , 'Temperature': '210287_00010'            #Temperature, water, degrees Celsius
        , 'PH': '210288_00400'                     # pH, water, unfiltered, field, standard units
        , 'Chloro': '210289_32318'                 # Chlorophylls, water, in situ, fluorometric method, excitation at 470 +-15 nm, emission at 685 +-20 nm, micrograms per liter
        , 'ChloroFluor': '210292_32320'            # Chlorophyll fluorescence (fChl), water, in situ, fluorometric method, excitation at 470 +-15 nm, emission at 685 +-20 nm, relative fluorescence units (RFU)
        , 'DissolvedOxygenPercent': '220586_00301' #  Dissolved oxygen, water, unfiltered, percent of saturation
        , 'Discharge': '66908_00060'               # Discharge, cubic feet per second
        , 'GageHeight': '66910_00065'              # Gage height, feet
        }, 'USGS_hockanum_east_hartford')

PARK_HARTFORD = RiverLocation('41.47.03.98', '72.42.29.00', {
          'Discharge': '66897_00060'           # Discharge, cubic feet per second
        , 'GageHeight': '66898_00065'          # Gage height, feet
        , 'SpecificConductance': '66899_00095' # Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius
        , 'Temperature': '66901_00010'         # Temperature, water, degrees Celsius
        , 'DissolvedOxygen': '66902_00300'     # Dissolved oxygen, water, unfiltered, milligrams per liter
        , 'PH': '66904_00400'                  # pH, water, unfiltered, field, standard units
        , 'Turbidity': '66905_63680'           # Turbidity, water, unfiltered, monochrome near infra-red LED light, 780-900 nm, detection angle 90 +-2.5 degrees, formazin nephelometric units (FNU)
        }, 'USGS_park_hartford')
    
FARMINGTON_TARIFFVILLE = RiverLocation('41.54.29.82', '72.45.33.67', {
          'DissolvedOxygenPercent': '200197_00301' # Dissolved oxygen, water, unfiltered, percent of saturation, [Manta]
        , 'PH': '201203_00400'                     # pH, water, unfiltered, field, standard units, [Manta]
        , 'SpecificConductance': '201204_00095'    # Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius, [Manta]
        , 'Temperature': '201246_00010'            # Temperature, water, degrees Celsius, [Manta]
        , 'Turbidity': '201248_63680'              # Turbidity, water, unfiltered, monochrome near infra-red LED light, 780-900 nm, detection angle 90 +-2.5 degrees, formazin nephelometric units (FNU), [Manta]
        , 'UVFluor': '201249_32291'                # UV fluorescence, water, in situ, single band, 370 nm excitation, 460 nm emission, relative fluorescence units (RFU), [Manta]
        , 'UVFlour2': '201250_32291'               # UV fluorescence, water, in situ, single band, 370 nm excitation, 460 nm emission, relative fluorescence units (RFU), [Manta(2)]
        , 'DissolvedOxygen': '201302_00300'        # Dissolved oxygen, water, unfiltered, milligrams per liter, [Manta]
        , 'Discharge': '66892_00060'               # Discharge, cubic feet per second
        , 'GageHeight': '66893_00065'              # Gage height, feet
        }, 'USGS_farmington_tariffville')

STONY_BROOK_WEST_SUFFIELD = RiverLocation('41.57.39.02', '72.42.37.75', {
          'Discharge': '66849_00060'     # Discharge, cubic feet per second
        , 'GageHeight': '66850_00065'    # Gage height, feet
        , 'Precipitation': '66853_00045' # Precipitation, total, inches
        }, 'USGS_stony_brook_west_suffield')

CT_THOMPSONVILLE = RiverLocation('41.59.14', '72.36.21', {
          'DOMFluore': '256024_32295'                # Dissolved organic matter fluorescence (fDOM), water, in situ, concentration estimated from reference material, micrograms per liter as quinine sulfate equivalents (QSE)
        , 'DissolvedOxygenPercent': '256026_00301'   # Dissolved oxygen, water, unfiltered, percent of saturation
        , 'Discharge': '66838_00060'                 # Discharge, cubic feet per second
        , 'GageHeight': '66839_00065'                # Gage height, feet
        , 'DissolvedOxygen': '66840_00300'           # Dissolved oxygen, water, unfiltered, milligrams per liter
        , 'Temperature': '66842_00010'               # Temperature, water, degrees Celsius
        , 'SpecificConductance': '66843_00095'       # Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius
        , 'DissolvedOxygenDownstream': '66844_00301' # Dissolved oxygen, water, unfiltered, percent of saturation, Downstream, [Manta]
        , 'PH': '66845_00400'                        # pH, water, unfiltered, field, standard units
        , 'Turbidity': '66846_63680'                 # Turbidity, water, unfiltered, monochrome near infra-red LED light, 780-900 nm, detection angle 90 +-2.5 degrees, formazin nephelometric units (FNU)
        }, 'USGS_ct_thomsonville')

BRADLEY_RIVERS_CODES = ['FATV', 'SBWS', 'CTTV', 'BBBB']
BRADLEY_RIVERS = [FARMINGTON_TARIFFVILLE, STONY_BROOK_WEST_SUFFIELD, 
                  CT_THOMPSONVILLE, BROAD_BROOK_BROAD_BROOK]

class DateIncrementor:
    
    def __init__(self, data):
        self.data = data
        self.i = 0
        self._move_to_next_correct_minute()
        
    def has_next(self):
        return self.i + 1 < len(self.data.data['datetime']) - 1
        
    def next_date(self):
        return self.data.data['datetime'][self.i]
    
    def next_values(self):
        a, b = (self._get(self.data, 'Discharge')[self.i], self._get(self.data, 'GageHeight')[self.i])
        self.i += 1
        self._move_to_next_correct_minute()
        return a, b
                
    def _get(self, r, c):
        return r.data[r[c]]
    
    def _is_correct_minute(self, ds):
        return ds[-2:] == '45' # NOAA data is at hh:51
    
    def _move_to_next_correct_minute(self):
        while self.has_next() and not self._is_correct_minute(self.next_date()):
            self.i += 1

def _match_bradley_rivers_dates():
    data = {}
    data['DateTime'] = usgs_dates()
    for c, ds in zip(BRADLEY_RIVERS_CODES, BRADLEY_RIVERS):
        inc = DateIncrementor(ds)
        data['{}_Discharge'.format(c)] = []
        data['{}_GageHeight'.format(c)] = []
        date = inc.next_date()
        for d in data['DateTime']:
            if date == '' or d != datetime.strptime(date, '%m/%d/%Y %H:%M'):
                data['{}_Discharge'.format(c)].append('x')
                data['{}_GageHeight'.format(c)].append('x')
            else:
                discharge, gage_height = inc.next_values()
                data['{}_Discharge'.format(c)].append(discharge)
                data['{}_GageHeight'.format(c)].append(gage_height)   
                if inc.has_next():
                    date = inc.next_date()
                else:
                    date = ''
    return data

def _create_bradley_rivers_data():
    data = _match_bradley_rivers_dates()
    columns = []
    columns.append(Column('DateTime'))
    for c in ['Discharge', 'GageHeight']:
        for r in BRADLEY_RIVERS_CODES:
            columns.append(FloatColumn('{}_{}'.format(r, c)))
    ds = create_dataset(data, columns)
    return ds

BRADLEY_RIVERS_DATA = _create_bradley_rivers_data()
