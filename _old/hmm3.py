import pickle
from pprint import pprint
from pomegranate import State, BetaDistribution, HiddenMarkovModel, GeneralMixtureModel

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

names = open_data('data/hourly.names')
data = open_data('data/hourly.data')

data['HourlySkyConditions'] = [c[:c.find(':')] for c in data['HourlySkyConditions']]
conditions = list(set([x for x in data['HourlySkyConditions']]))

def canparse(i):
    try:
        int(i)
        return True
    except:
        return False

data = [(int(t), data['HourlySkyConditions'][i])
    for i, t in enumerate(data['HourlyDewPointTemperature']) if canparse(t)]

X = [a for a, b in data]
Y = [b for a, b in data]


# https://github.com/jmschrei/pomegranate/issues/561
