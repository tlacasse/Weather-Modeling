from weather.source import get_full_dataset
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data, length = get_full_dataset()

del data['DateTime']

# ignore datetime
data_array = [[data[k][i] for k in data.keys()] for i in range(length)]

A = np.array(data_array, dtype='double')
A = np.swapaxes(A, 0, 1)

cA = np.corrcoef(A)

ax = sns.heatmap(cA,
                 xticklabels=data.keys(), 
                 yticklabels=data.keys())
ax.invert_yaxis()
plt.show()

print(cA)

with open('data/correlation_names.txt', 'w') as file:
    file.write(','.join(data.keys()))
    
with open('data/correlation_matrix.txt', 'w') as file:
    for i in range(cA.shape[0]):
        file.write(','.join([str(x) for x in cA[i]]) + '\n')
