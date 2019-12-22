from weather.dataset import open_data

fails = open_data('data/full.fails')

for k in fails.keys():
    print(k)
    print(list(set(fails[k])))
