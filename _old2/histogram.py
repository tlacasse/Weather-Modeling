from weather import DATASET, CONDITIONS
from dataset import columns_to_dict
import numpy as np
import matplotlib.pyplot as plt

counts_humidity = columns_to_dict(DATASET.get_column('HourlySkyConditions'), 
                                  DATASET.get_column('HourlyRelativeHumidity'))

counts_dewpoint = columns_to_dict(DATASET.get_column('HourlySkyConditions'), 
                                  DATASET.get_column('HourlyDewPointTemperature'))

print(counts_humidity.keys())
print(counts_dewpoint.keys())
print(CONDITIONS)

for counts, title in zip([counts_humidity, counts_dewpoint], ['humidity', 'dew point temperature']):
    for k, c in enumerate(CONDITIONS):
        plt.figure()
        plt.title('{} - {}'.format(title, c))
        x = np.array(counts[k])
        plt.hist(x, bins=25)
