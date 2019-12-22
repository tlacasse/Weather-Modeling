"""
import numpy as np
from pomegranate import NormalDistribution, HiddenMarkovModel

dists = [NormalDistribution(5, 1), NormalDistribution(1, 7), NormalDistribution(8,2)]
trans_mat = np.array([[0.7, 0.3, 0.0],
                             [0.0, 0.8, 0.2],
                             [0.0, 0.0, 0.9]])
starts = np.array([1.0, 0.0, 0.0])
ends = np.array([0.0, 0.0, 0.1])
model = HiddenMarkovModel.from_matrix(trans_mat, dists, starts, ends)

print(dir(model))

#print(model.viterbi(np.array([1, 2, 1])))
print(", ".join(state.name for i, state in model.viterbi([2, 1, 0])[1]))
"""

import pickle
from pprint import pprint
from pomegranate import State, DiscreteDistribution

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

names = open_data('data/hourly.names')
data = open_data('data/hourly.data')

condition_names = set()
for condition in data['HourlySkyConditions']:
    condition_names.add(condition[:condition.find(':')])

count_lessthan30 = {}
count_morethan30 = {}
for name in condition_names:
    count_lessthan30[name] = 0
    count_morethan30[name] = 0

for i, condition in enumerate(data['HourlySkyConditions']):
    val = data['HourlyDewPointTemperature'][i]
    name = condition[:condition.find(':')]
    try:
        if (int(val) <= 30):
            count_lessthan30[name] += 1
        else:
            count_morethan30[name] += 1
    except:
        pass

states = []
for name in condition_names:
    probs = {}
    total = max(count_lessthan30[name] + count_morethan30[name], 1)
    probs['l'] = count_lessthan30[name] / total
    probs['m'] = count_morethan30[name] / total
    pprint(probs)
    dist = DiscreteDistribution(probs)
    states.append(State(dist, name=(name if name != '' else ' ')))

pprint(states)

#s1 = State(NormalDistribution(5, 1))
#s2 = State(NormalDistribution(1, 7))
#s3 = State(NormalDistribution(8, 2))
