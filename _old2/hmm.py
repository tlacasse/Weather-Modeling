from weather import DATASET_CONDITION_HUMIDITY as data, CONDITIONS, BIN_SIZE
from dataset import columns_to_dict
from pomegranate import DiscreteDistribution, HiddenMarkovModel
from pprint import pprint
from sklearn.metrics import confusion_matrix, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

values = columns_to_dict(data.get_column('HourlySkyConditions'), 
                         data.get_column('HourlyRelativeHumidity'))

# get emission distributions

dists = []

for c, name in enumerate(CONDITIONS):
    counts = {x: 1 for x in range(0, 101, BIN_SIZE)}
    for x in values[c]:
        counts[x] += 1
    total = len(values[c])
    dists.append(DiscreteDistribution({k: v / total for k, v in counts.items()}))
  
conditions = data.get_column('HourlySkyConditions')

# create transition matrix

pseudocount = 1
num_conditions = len(CONDITIONS)
transition = np.full((num_conditions, num_conditions), pseudocount, dtype='int32')
totals = np.full((num_conditions,), pseudocount * num_conditions, dtype='int32')
   
for i, j in zip(conditions, conditions[1:]):
    transition[i][j] += 1
    totals[i] += 1
    
transition = transition.astype('double')

for i in range(num_conditions):
    transition[i][:] /= totals[i]
    
totals = totals.astype('double')
total = sum(totals)

for i in range(num_conditions):
    totals[i] /= total

# create model

model = HiddenMarkovModel.from_matrix(transition, dists, totals, 
                                      state_names=CONDITIONS, name='weather')

pprint(model.states)

STATE_NAMES = [s.name for s in model.states][:-2] # ignore start and end
pprint(STATE_NAMES)
STATE_MAP = [CONDITIONS.index(s) for s in STATE_NAMES]
pprint(STATE_MAP)

# test model

COUNT_START = 100
COUNT_END = 800

sequence = data.get_column('HourlyRelativeHumidity')[COUNT_START:COUNT_END]

print(sequence)
print(model.log_probability(sequence))

prediction = [(i, state.name) for i, state in model.viterbi(sequence)[1]][1:]

results = [name for i, name in prediction]
actual = [CONDITIONS[i] for i in conditions][COUNT_START:COUNT_END]

iactual = conditions[COUNT_START:COUNT_END]
iresults = [CONDITIONS.index(c) for c in results]

print(results)

X = np.array([i for i in range(len(iresults))])
Y = np.array([CONDITIONS.index(c) for c in results])

plt.figure()
plt.plot(X,Y)
plt.figure()
plt.hist(Y)

X = np.array([i for i in range(len(actual))])
Y = np.array([CONDITIONS.index(c) for c in actual]) 

plt.figure()
plt.plot(X,Y)
plt.figure()
plt.hist(Y)

all_prob = model.predict_proba(sequence)

new_results = [np.random.choice(STATE_MAP, p=all_prob[i]) for i in range(len(all_prob))]

X = np.array([i for i in range(len(new_results))])
Y = np.array(new_results)

plt.figure()
plt.plot(X,Y)
plt.figure()
plt.hist(Y)

""""
print()
print()

T, E = model.forward_backward(sequence)

pprint(E)
pprint(T)

pprint(E.shape)
pprint(T.shape)

print()

print(model.forward(sequence))

print(model.backward(sequence))

print()
print()
print(model.predict_proba(sequence).shape)
"""




#norm_E = E[0] / np.linalg.norm(E[0])

#E[0] = norm_E * np.linalg.norm(E[0])

#print(E[0])
#print(norm_E)
#print(sum(np.exp(i) for i in E[0]))

#print([np.random.choice([0, 1, 2, 3, 4, 5], p=E[i]) for i in range(10)])

#print(mean_squared_error(iresults, iactual))

#plt.figure()
#plt.hist(np.array(iactual))

#plt.figure()
#plt.hist(np.array(iresults))

#print(', '.join(results))

# notes
# np.random.choice
# permutation sampling

#for i, j in zip(actual, results):
#    print('{} =?= {}\t{}'.format(i, j, ))

#print(confusion_matrix(actual, results))
