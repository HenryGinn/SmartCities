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
    model.predict()
    model.postprocess()
    model.output_results(plot_type="Data")

def fit(model, fit_category):
    model.set_fit_category("train")
    model.create_model()
    model.fit(verbose=0, epochs=50)
    model.save()
    #model.plot_history()
    model.save()
    model.add_column(model.data, "DataNormalised")
    model.predict()
    model.add_column(model.modelled, "ModelledNormalised")
    #model.postprocess()
    model.output_results(plot_type="Data")


case = 0
model_type = "Default"
model_type = "ARIMA"
model_type = "LSTM"

match model_type:
    case "Default": model = Model(case=case)
    case "ARIMA"  : model = ARIMA(case=case)
    case "LSTM"   : model = LSTM(case=case, look_back=3, train=0.8, units=20)

model.stage="Normalised"
#model.preprocess()
model.set_inputs_and_labels()
model.order = (6, 1, 4)
model.seasonal_order = (3, 0, 3, 12)

#fit(model, "train")
fit(model, "validate")
#fit(model, "test")


#model.create_correlograms()
#model.compare_residuals()
#model.create_correlograms()
#model.create_histogram()
