from weather.usgs import BRADLEY_RIVERS_DATA
from weather.dataset import DataSet
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ignore datetime
dataset = DataSet([r[1:] for r in BRADLEY_RIVERS_DATA.data], BRADLEY_RIVERS_DATA.get_column_names()[1:])

A = np.array(dataset.data, dtype='double')
A = np.swapaxes(A, 0, 1)

cA = np.corrcoef(A)

ax = sns.heatmap(np.corrcoef(A), annot=True,
                 xticklabels=dataset.get_column_names(), 
                 yticklabels=dataset.get_column_names())
ax.invert_yaxis()
plt.show()

for i, c in enumerate(dataset.get_column_names()):
    print(c)
    print(sum(cA[i]))
    