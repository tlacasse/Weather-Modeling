import pickle
from pprint import pprint
from pomegranate import State, NormalDistribution, HiddenMarkovModel

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

names = open_data('data/hourly.names')
data = open_data('data/hourly.data')

data['HourlySkyConditions'] = [c[:c.find(':')] for c in data['HourlySkyConditions']]
conditions = list(set([x for x in data['HourlySkyConditions']]))

def tryparse(i):
    try:
        int(i)
        return True
    except:
        return False

data = [(int(t), data['HourlySkyConditions'][i])
    for i, t in enumerate(data['HourlyDewPointTemperature']) if tryparse(t)]

X = [a for a, b in data]
Y = [b for a, b in data]

seq1 = X[:1000]
seq2 = X[1000:2000]
seq3 = X[2000:3000]

dist = NormalDistribution.from_samples(X[:1000])

clear = State(dist, name='CLEAR')
cloud = State(dist, name='CLOUD')

model = HiddenMarkovModel('Weather')
model.add_states(clear, cloud)
model.add_transition(model.start, clear, 0.3)
model.add_transition(model.start, cloud, 0.7)
model.add_transition(clear, clear, 0.7)
model.add_transition(cloud, clear, 0.5)
model.add_transition(clear, cloud, 0.3)
model.add_transition(cloud, cloud, 0.5)
#model.fit()
model.bake()

def to_name(num):
    return 'CLEAR' if num == 0 else 'CLOUD'

sequence = X[:100]
"""
logp, path = model.viterbi(sequence)
print("Sequence: '{}'  -- Log Probability: {} -- Path: {}".format(
        ''.join(sequence), logp, " ".join( state.name for idx, state in path[1:-1] ) ))
"""

logp, path = model.viterbi(sequence)
print('Sequence: ' + ', '.join([str(x) for x in sequence]))
print('Log Probability: ' + str(logp))
print('Path: ' + ', '.join(map(to_name, [state.name for i, state in path[1:-1]])))

"""
hmm = HiddenMarkovModel.from_samples(ExponentialDistribution, 
                                     n_components=7, X=[X], labels=[Y], algorithm='labeled')




hmm = HiddenMarkovModel.from_samples(ExponentialDistribution, 7 la)

hmm = HiddenMarkovModel.from_samples(ExponentialDistribution, n_components=7, X=X)

logp, path = model.viterbi( sequence )
    print "Sequence: '{}'  -- Log Probability: {} -- Path: {}".format(
        ''.join( sequence ), logp, " ".join( state.name for idx, state in path[1:-1] ) )
"""