from weather.dataset import parse_data_csv, save_data

airports = ['OXFORD']
save_data('data/noaa/all.airports', airports)

for a in airports:
    parse_data_csv('noaa/airports/{}'.format(a))
