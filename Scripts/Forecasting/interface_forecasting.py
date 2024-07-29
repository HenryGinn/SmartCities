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
model = "Default"
model = "ARIMA"
model = "LSTM"


def run_default():
    global default
    default = Model(case=case)
    default.preprocess()
    default.predict()
    default.post_predict()
    default.postprocess()
    default.output_results(plot_type="Data")
    default.output_results(plot_type="Residuals")
    default.create_correlograms()

def run_arima():
    global arima
    arima = ARIMA(case=case)
    arima.preprocess()
    arima.determine_hyperparameters()
    #arima.fit()
    #arima.save()
    arima.load()
    arima.predict()
    arima.postprocess()
    #arima.create_correlograms()
    #arima.compare_residuals()
    arima.output_results(plot_type="Data")
    arima.output_results(plot_type="Residuals")
    arima.create_correlograms()
    arima.create_histogram()

def run_lstm():
    global lstm
    lstm = LSTM(name="Linear", case=5, look_back=1)
    lstm.preprocess()
    lstm.set_inputs_and_labels()
    model = True
    #model = False
    if model:
        load = True
        #load = False
        if load:
            lstm.load()
        else:
            lstm.create_model()
            lstm.fit(epochs=1, verbose=2)
            lstm.save()
        lstm.predict()
    else:
        lstm.modelled = np.zeros(lstm.length_forecast)

    lstm.postprocess()
    lstm.output_results(stage="Normalised")
    lstm.output_results(title="Modelling Test Data with LSTM")


match model:
    case "Default": run_default()
    case "ARIMA"  : run_arima()
    case "LSTM"   : run_lstm()
