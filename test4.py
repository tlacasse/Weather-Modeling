from weather.dataset import save_data
from weather.models import WeatherModel
from weather.usgs import GAGEHEIGHT_TEMPLATE
import weather.source as wsrc
import numpy as np

data, length = wsrc.get_full_dataset()

emmissions = np.random.choice([33, 34, 35, 36, 37, 38, 39, 40, 60], length)
states = data['OXFORD_HourlySkyConditions']
model = WeatherModel.build_hmm(emmissions, states, 'test')

print(model.predict([33, 34, 34, 60, 60, 60, 60, 60, 60]))
