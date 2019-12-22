from weather.source import get_full_dataset
from weather.models import WeatherModel
from weather.noaa import CONDITIONS
import matplotlib.pyplot as plt
import numpy as np

data, length = get_full_dataset()

model = WeatherModel.build_hmm(data['OXFORD_HourlyRelativeHumidity'],
                               data['OXFORD_HourlySkyConditions'], 'test',
                               em_min=0, em_max=100, bin_size=2)

sequence = data['OXFORD_HourlyRelativeHumidity'][30000:30200]
actual = data['OXFORD_HourlySkyConditions'][30000:30200]

print('SEQUENCE')
print(sequence)

prediction = model.predict(sequence)

print('PREDICTION')
print([CONDITIONS[x] for x in prediction])

X = np.array([i for i in range(len(actual))])
Y = np.array(actual)

plt.figure()
plt.title('Actual')
plt.plot(X, Y)

X = np.array([i for i in range(len(prediction))])
Y = np.array(prediction)
plt.figure()
plt.title('Predicted')
plt.plot(X, Y)
