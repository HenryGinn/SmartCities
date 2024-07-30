import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os

import matplotlib.pyplot as plt
import numpy as np

from lstm import LSTM
from arima import ARIMA
from model import Model


plt.close("all")

case = 1
model_type = "Default"
model_type = "ARIMA"
model_type = "LSTM"

match model_type:
    case "Default": model = Model(case=case)
    case "ARIMA"  : model = ARIMA(case=case)
    case "LSTM"   : model = LSTM(case=case)

# Setup

model.preprocess()
model.order = (6, 1, 4)
model.seasonal_order = (3, 0, 3, 12)


# Validating

model.set_fit_category("train")
#model.load()
model.fit()
model.save()
model.predict()
model.postprocess()
model.output_results(plot_type="Data")


# Testing

model.set_fit_category("validate")
#model.load()
model.fit()
model.save()
model.predict()
model.postprocess()
model.output_results(plot_type="Data")


# Forecasting

model.set_fit_category("test")
#model.load()
model.fit()
model.save()
model.predict()
model.postprocess()
model.output_results(plot_type="Data")

#model.create_correlograms()
#model.compare_residuals()
#model.create_correlograms()
#model.create_histogram()
