from pomegranate import DiscreteDistribution, ConditionalProbabilityTable

# https://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html

from weather.dataset import save_data, load_data
from weather.source import build_dataset
from sklearn_crfsuite import CRF, scorers, metrics

# FTTV, SBWS, CTTV, BBBB
data = build_dataset()

# list(list(dict()))
# X is list of "sequences", which is a list of given information in
# the form of a dictionary per node

# list(list())
# Y is list of "sequences" but is a list of the output of the nodes

def round_to(x, n):
    return round(x / n) * n

def convert(x):
    return str(round_to(round(x * 10), 5) / 10)

for k in data.keys():
    data[k] = [convert(x) for x in data[k]]
    print(k)
    print(len(set(data[k])))
    print(set(data[k]))

def to_point(i):
    features = {}
    for r in ['FTTV', 'SBWS', 'BBBB']:
        features[r] = data[r][i]
    return features, data['CTTV'][i]

X = []
Y = []

for i in range(len(data['CTTV'])):
    x, y = to_point(i)
    X.append(x)
    Y.append(y)
    
print(X[:100])
    
X = [X]
Y = [Y]



crf = CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=150,
    all_possible_transitions=True,
    verbose=True
)
crf.fit(X, Y)

Y_pred = crf.predict(X)


