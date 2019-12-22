import pickle
from pprint import pprint
from pomegranate import State, ExponentialDistribution, HiddenMarkovModel

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

names = open_data('data/hourly.names')
data = open_data('data/hourly.data')

def name(c):
    return c[:c.find(':')]

HourlySkyConditions = [name(c) for c in data['HourlySkyConditions']]

condition_names = set(HourlySkyConditions)

probs = {}
for i in range(len(data['HourlyDewPointTemperature'])):
    key = name(data['HourlySkyConditions'][i])
    if not key in probs:
        probs[key] = []
    try:
        probs[key].append(int(data['HourlyDewPointTemperature'][i]))
    except:
        pass

states = {}

for k, v in probs.items():
    states[k] = State(ExponentialDistribution.from_samples(v), name=(k if k != '' else ' '))
    
counts = {}
initials = {}
prev = None
for x in [name(c) for c in data['HourlySkyConditions']]:
    if (prev is not None):
        if not prev in counts:
            counts[prev] = {}
        if not x in counts[prev]:
            counts[prev][x] = 1 # start at one to guarantee all possible transitions
        counts[prev][x] += 1
    if not x in initials:
        initials[x] = 0
    initials[x] += 1
    prev = x
    
for n in counts:
    total = sum([v for k, v in counts[n].items()])
    counts[n] = {k: v / total for k, v in counts[n].items()}
    
model = HiddenMarkovModel('example')
model.add_states([v for k, v in states.items()])

for x, y in initials.items():
    model.add_transition(model.start, states[x], y)
for x0, y0 in counts.items():
    for x1, y1 in y0.items():
        model.add_transition(states[x0], states[x1], y1)
model.bake()

pprint([s for s in states])

#print(len(states))
arr = model.forward_backward([20, 24, 22, 20])[1]
#print(arr.shape)

result = []
for i in range(arr.shape[0]):
    result.append([])
    for j in range(arr.shape[1]):
        result[i].append(2.71828 ** arr[i][j])

pprint(result)

sequence = list(map(int, data['HourlyDewPointTemperature'][:10]))
print('\n\n\n')  
print(model.predict(sequence))
print('\n\n\n') 
pprint(model.predict_proba(sequence))
print('\n\n\n') 
trans, ems = model.forward_backward(sequence)

print(trans)
print('\n\n\n') 
print(ems)

#https://github.com/jmschrei/pomegranate/blob/master/tutorials/B_Model_Tutorial_3_Hidden_Markov_Models.ipynb