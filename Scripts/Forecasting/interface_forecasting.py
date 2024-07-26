import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os

import matplotlib.pyplot as plt
import numpy as np

from lstm import LSTM
from arima import ARIMA


plt.close("all")


arima = ARIMA(case=5, output="show")
arima.preprocess()
#arima.determine_hyperparameters()
#arima.fit()
#arima.save()
arima.load()
arima.predict()
arima.post_predict()
arima.create_correlograms()
#arima.compare_residuals()
#arima.postprocess()
#arima.output_results(title="Modelling Via Simple Determinative Processes")



"""
arima.plot_residuals(title="Residuals After Subtracting\nMonthly Averages")
arima.generate_figure_name()
arima.output_figure()

arima.normalise_residuals()

arima.plot_residuals(title="Normalised Residuals After\nSubtracting Monthly Averages")
arima.generate_figure_name()
arima.output_figure()
"""

"""
lstm = LSTM(name="Linear", case=5, look_back=1)

lstm.preprocess()
lstm.set_inputs_and_labels()
lstm.set_splits()

model = True
#model = False

if model:
    load = True
    load = False

    if load:
        lstm.load()
    else:
        lstm.create_model()
        lstm.fit(epochs=100, verbose=2)
        lstm.save()
    lstm.predict()
else:
    lstm.modelled = np.zeros(lstm.length_forecast)

lstm.extend_dataframe()
lstm.postprocess()
lstm.output_results(stage="Normalised")
lstm.output_results(title="Modelling Test Data with LSTM")
"""
