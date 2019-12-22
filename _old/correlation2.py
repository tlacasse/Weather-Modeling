import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint
import sys

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    
def canparse(i):
    try:
        int(i)
        return True
    except:
        return False
    
def cancondition(c):
    return c.find(':') >= 0
    
def condition(c):
    return c[:c.find(':')] 

def listindex(l, v):
    try:
        return l.index(v)
    except:
        return -1;
    
names = open_data('data/hourly.names')
data = open_data('data/hourly.data')

DEW = 'HourlyDewPointTemperature'
TEMP = 'HourlyDryBulbTemperature'
COND = 'HourlySkyConditions'

rows = len(data[TEMP])

data = [(data[DEW][i], data[TEMP][i], data[COND][i]) for i in range(rows)]

data = [(int(a), int(b), condition(c)) for a, b, c in data if canparse(a) and canparse(b) and cancondition(c)]

conditions = set([c for a, b, c in data])
conditions.remove('34 BKN')
print(conditions)
conditions = ['CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'VV']
print(conditions)

data = [[a, b, listindex(conditions, c)] for a, b, c in data]


X = np.array([a for a, b, c in data])
Y = np.array([b for a, b, c in data])
Z = np.array([c for a, b, c in data])

A = np.stack((X, Y, Z), axis=0)

corr = np.cov(A)

ax = sns.heatmap(corr, linewidth=0.5)
plt.show()
