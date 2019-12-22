from weather import DATASET
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

A = np.array(DATASET.data, dtype='double')
A = np.swapaxes(A, 0, 1)

ax = sns.heatmap(np.corrcoef(A),
                 xticklabels=DATASET.get_column_names(), 
                 yticklabels=DATASET.get_column_names())
ax.invert_yaxis()
plt.show()
