import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os

import matplotlib.pyplot as plt

from forecast import Forecast
from lstm import LSTM
from arima import ARIMA


plt.close("all")

lstm = LSTM(name="Linear", case=1)

lstm.preprocess_data()
lstm.set_splits()
lstm.create_model()

load = True
load = False

if load:
    lstm.load()
else:
    lstm.fit(epochs=100, verbose=2)
    lstm.save()

lstm.output_results(title="Modelling Test Data with LSTM")

"""
lstm.set_splits()
lstm.extend_dataframe()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_axes([0.12, 0.12, 0.8, 0.72])
lstm.create_plot(fig, ax, output="show", legend_bbox_to_anchor=(0.13, 0.8), loc=10,
                 title="Modelling Test Data with LSTM")
"""
