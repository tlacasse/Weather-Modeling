from weather.dataset import parse_data_csv
from weather.source import get_selected_river_sites

sites = get_selected_river_sites()

print('SAVE DATA OF SELECTED SITES')
for s, v in sites:
    print(s.name)
    print('request data')
    d = s.get_data(begin_date='2010-11-9', end_date='2019-11-9', var_code=v.code)
    d = d.replace('\t', ',')
    
    print('save to file')
    d = d.split('\n')
    print(len(d))
    cleaned = []
    since_comments = 0
    for line in d:
        if line.strip() and line[0] != '#':
            since_comments += 1
            # ignore datatype line after header
            if since_comments != 2:
                cleaned.append(line)
    print(len(cleaned))    
    d = '\n'.join(cleaned)
    with open('data/usgs/sites/{}.csv'.format(s.key), 'w') as file:
        file.write(d)
    print('parse data')
    parse_data_csv('usgs/sites/{}'.format(s.key))
