from weather.source import get_full_dataset
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data, length = get_full_dataset()

for k in data.keys():
    if k == 'DateTime':
        continue
    plt.figure()
    plt.title(k)
    column = np.array(data[k])
    print(k)
    print('count: {}'.format(len(data[k])))
    print('max: {}'.format(max(column)))
    print('min: {}'.format(min(column)))
    sns.countplot(column)
