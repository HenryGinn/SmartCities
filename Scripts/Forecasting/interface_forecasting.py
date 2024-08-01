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

def load(model, fit_category):
    model.set_fit_category("train")
    model.load()
    output(model)

def fit(model, fit_category):
    model.set_fit_category("train")
    model.create_model()
    model.fit(verbose=0, epochs=2)
    model.save()
    model.plot_history()
    output(model)

def output(model):
    model.predict()
    model.postprocess()
    model.output_results(plot_type="Data", stage="Normalised")


case = 1
model_type = "Default"
model_type = "ARIMA"
model_type = "LSTM"

match model_type:
    case "Default": model = Model(case=case)
    case "ARIMA"  : model = ARIMA(case=case)
    case "LSTM"   : model = LSTM(case=case, look_back=10, output="save")

#model.order = (6, 1, 4)
#model.seasonal_order = (3, 0, 3, 12)

model.preprocess()

fit(model, "train")
model.create_correlograms()
model.create_histogram()
model.add_to_results_summary()
#fit(model, "validate")
#model.create_correlograms()
#model.create_histogram()
#model.results_summary()
model.save_results_summary()
#fit(model, "test")

#load(model, "train")
#load(model, "validate")
#load(model, "test")
