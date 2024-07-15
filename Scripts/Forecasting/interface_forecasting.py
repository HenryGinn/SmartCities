import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os

import matplotlib.pyplot as plt

from forecast import Forecast
from lstm import LSTM
from arima import ARIMA

lstm = LSTM()

lstm.preprocess_data()
lstm.set_splits()
lstm.create_model()

load = True
#load = False

if load:
    lstm.load()
else:
    lstm.fit_model(epochs=2500, verbose=2)
    lstm.save()

lstm.predict()

lstm.set_splits()
lstm.extend_dataframe()

lstm.create_forecast()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_axes([0.12, 0.12, 0.8, 0.72])
lstm.create_plot(fig, ax, output="save", legend_bbox_to_anchor=(0.13, 0.8), loc=10,
                 title="Modelling Test Data with LSTM")
