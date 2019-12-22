from weather import DATASET_CONDITION_HUMIDITY as data, CONDITIONS, BIN_SIZE
from dataset import columns_to_dict
from pomegranate import DiscreteDistribution, HiddenMarkovModel, IndependentComponentsDistribution, NormalDistribution
from pprint import pprint
from sklearn.metrics import confusion_matrix, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

values_humidity = columns_to_dict(data.get_column('HourlySkyConditions'), 
                                  data.get_column('HourlyRelativeHumidity'))

values_dewpoint = columns_to_dict(data.get_column('HourlySkyConditions'), 
                                  data.get_column('HourlyDewPointTemperature'))

# get emission distributions
 

dists = []

for c, name in enumerate(CONDITIONS):
    counts = {x: 1 for x in range(0, 101, BIN_SIZE)}
    for x in values_humidity[c]:
        counts[x] += 1
    total = len(values_humidity[c])
    humidity = DiscreteDistribution({k: v / total for k, v in counts.items()})
    
    counts = {x: 1 for x in range(0, 101, BIN_SIZE)}
    for x in values_dewpoint[c]:
        counts[x] += 1
    total = len(values_dewpoint[c])
    dewpoint = DiscreteDistribution({k: v / total for k, v in counts.items()})
    
    print(humidity)
    
    print(dewpoint)
    print()
    print()
    
    dists.append(IndependentComponentsDistribution([humidity, dewpoint]))
  
conditions = data.get_column('HourlySkyConditions')
 
#pprint(dists)