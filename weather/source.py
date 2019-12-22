from weather.dataset import open_data
from weather.visuals import Projection, RiverMapper
from datetime import datetime, timedelta

def all_datetimes():
    # https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
    def daterange(start_date, end_date):
        for d in range(int((end_date - start_date).days) + 1):
            for h in range(24):
                yield start_date + timedelta(days=d, hours=h, minutes=45)
    return [d for d in daterange(datetime(2010, 11, 9, 0, 0), datetime(2019, 11, 9, 23, 45))]

def get_selected_river_sites():
    return open_data('data/usgs/selected.sites')

def get_airports():
    return open_data('data/noaa/all.airports')

def get_full_dataset():
    data = open_data('data/full.data')
    return data, len(data[list(data.keys())[0]])

def build_projection(sites):
    return Projection(get_latlong_list(sites), width=16, padding=0.1)

def get_latlong_list(sites):
    return [(s.latitude, s.longitude) for s, v in sites]

def build_rivermapper(proj):
    h, w = proj.get_dim()
    return RiverMapper((h, w), 7, 10)

def round_to_bin(x, bin_size=2):
    return str(int(round( x / bin_size ) * bin_size))
