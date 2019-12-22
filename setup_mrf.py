from weather.source import build_dataset
from weather.models.mrf import MarkovRandomField, data_convert

def build_models(roundto=5):
    data, length = build_dataset()
    
    for k in data.keys():
        data[k] = [data_convert(x, roundto) for x in data[k]]
        print(k)
        print(len(set(data[k])))
        print(set(data[k]))
    
    # list(list(dict()))
    # X is list of "sequences", which is a list of given information in
    # the form of a dictionary per node
    
    # list(list())
    # Y is list of "sequences" but is a list of the output of the nodes
    
    for k in data.keys():
        all_keys = list(data.keys())
        all_keys.pop(all_keys.index(k))
        def to_point(i):
            features = {}
            for r in all_keys:
                features[r] = data[r][i]
            return features, data[k][i]
        
        X = []
        Y = []
        
        for i in range(length):
            x, y = to_point(i)
            X.append(x)
            Y.append(y)
            
        print(X[:10])
        print()
        print(Y[:10])
            
        X = [X]
        Y = [Y]
        
        f = MarkovRandomField(X, Y, verbose=True, c1=1.0, c2=0.5)
        f.save('data/model_{}.mrf'.format(k))
        
build_models()
