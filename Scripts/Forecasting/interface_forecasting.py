import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os

import matplotlib.pyplot as plt
import numpy as np

from lstm import LSTM
from arima import ARIMA


plt.close("all")

"""
arima = ARIMA(case=5, output="show")
arima.residuals = arima.data
arima.create_correlograms()
arima.preprocess()
arima.create_correlograms()
arima.determine_hyperparameters()
arima.fit()
arima.predict()
arima.create_correlograms()
#arima.compare_residuals()
#arima.postprocess()
#arima.output_results(title="Modelling Via Simple Determinative Processes")
"""


"""
arima.plot_residuals(title="Residuals After Subtracting\nMonthly Averages")
arima.generate_figure_name()
arima.output_figure()

arima.normalise_residuals()

arima.plot_residuals(title="Normalised Residuals After\nSubtracting Monthly Averages")
arima.generate_figure_name()
arima.output_figure()
"""


lstm = LSTM(name="Linear", case=5, look_back=1)

lstm.preprocess()
lstm.set_inputs_and_labels()
lstm.set_splits()
#lstm.create_model()
lstm.modelled = np.zeros(lstm.length_forecast)
#lstm.modelled = lstm.residuals.copy() / 3
#lstm.modelled = -np.ones(lstm.length_forecast)
lstm.extend_dataframe()
lstm.postprocess()
lstm.time_series["Original"] = np.log(lstm.time_series["Original"].values)
lstm.time_series["Original"] -= lstm.time_series["Linear"]
lstm.time_series["Original"] -= lstm.time_series["MonthlyAverage"]
lstm.time_series["Original"] = lstm.transform_backward(lstm.time_series["Original"], lstm.transform_data)
#lstm.add_column(lstm.modelled, "Modelled")
#lstm.modelled = lstm.time_series["Modelled"].values
lstm.output_results()

"""
load = True
load = False

if load:
    lstm.load()
else:
    lstm.fit(epochs=100, verbose=0)
    lstm.save()

lstm.predict()
lstm.output_results(title="Modelling Test Data with LSTM")
"""

"""
lstm.set_splits()
lstm.extend_dataframe()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_axes([0.12, 0.12, 0.8, 0.72])
lstm.create_plot(fig, ax, output="show", legend_bbox_to_anchor=(0.13, 0.8), loc=10,
                 title="Modelling Test Data with LSTM")
"""
