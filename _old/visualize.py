import pickle
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    
names = open_data('data/hourly.names')
data = open_data('data/hourly.data')

data['HourlySkyConditions'] = [c[:c.find(':')] for c in data['HourlySkyConditions']]
conditions = set([x for x in data['HourlySkyConditions']])

counts = {}
for i in range(len(data['HourlyDryBulbTemperature'])):
    key = data['HourlySkyConditions'][i]
    if not key in counts:
        counts[key] = []
    try:
        counts[key].append(int(data['HourlyDryBulbTemperature'][i]))
    except:
        pass

for c in conditions:
    plt.figure()
    plt.title(c)
    x = np.array(counts[c])
    plt.hist(x, bins=25)

