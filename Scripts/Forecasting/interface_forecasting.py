import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os

import matplotlib.pyplot as plt
import numpy as np

from lstm import LSTM
from arima import ARIMA
from model import Model
from architecture import Architecture


plt.close("all")

def load(model, fit_category):
    model.set_fit_category(fit_category)
    model.load()
    output(model)

def fit(model, fit_category):
    model.set_fit_category(fit_category)
    model.create_model()
    model.fit(verbose=0, epochs=2)
    model.save()
    model.plot_history()
    output(model)

def fit_manual_model(model, fit_category):
    model.set_fit_category(fit_category)
    model.fit()
    model.save()
    model.plot_history()
    output(model)

def output(model):
    model.plot_history()
    model.predict()
    model.postprocess()
    model.output_results(plot_type="Data", stage="Normalised")
    model.create_correlograms()
    model.create_histogram()
    model.output_results(plot_type="Data", stage="Original")
    model.add_to_results_summary()


#case = 1
model_type = "Default"
model_type = "ARIMA"
model_type = "LSTM"

"""
match model_type:
    case "Default": model = Model(case=case)
    case "ARIMA"  : model = ARIMA(case=case)
    case "LSTM"   : model = LSTM(case=case, look_back=10,
                                 verbose=0, epochs=300, output="save")
"""

#model.order = (6, 1, 4)
#model.seasonal_order = (3, 0, 3, 12)

architectures = [
    Architecture(False, False, False, 8,  False),
    Architecture(False, False, False, 16, False),
    Architecture(False, False, False, 32, False),
    Architecture(False, False, False, 64, False),
    Architecture(32,    False, False, 8,  False),
    Architecture(32,    False, False, 16, False),
    Architecture(32,    False, False, 32, False),
    Architecture(32,    False, False, 64, False),
    Architecture(False, False, False, 8,  False),
    Architecture(False, False, False, 16, False),
    Architecture(False, False, False, 32, False),
    Architecture(False, False, False, 64, False),
    Architecture(False, False, 8,     8,  False),
    Architecture(False, False, 8,     16, False),
    Architecture(False, False, 8,     32, False),
    Architecture(False, False, 8,     64, False),
    Architecture(False, False, 16,    8,  False),
    Architecture(False, False, 16,    16, False),
    Architecture(False, False, 16,    32, False),
    Architecture(False, False, 16,    64, False),
    Architecture(False, False, 32,    8,  False),
    Architecture(False, False, 32,    16, False),
    Architecture(False, False, 32,    32, False),
    Architecture(False, False, 32,    64, False),
    Architecture(32,    False, 8,     8,  False),
    Architecture(32,    False, 8,     16, False),
    Architecture(32,    False, 8,     32, False),
    Architecture(32,    False, 8,     64, False),
    Architecture(32,    False, 16,    8,  False),
    Architecture(32,    False, 16,    16, False),
    Architecture(32,    False, 16,    32, False),
    Architecture(32,    False, 16,    64, False),
    Architecture(32,    False, 32,    8,  False),
    Architecture(32,    False, 32,    16, False),
    Architecture(32,    False, 32,    32, False),
    Architecture(32,    False, 32,    64, False),
    Architecture(32,    False, 8,     8,  32   ),
    Architecture(32,    False, 8,     16, 32   ),
    Architecture(32,    False, 8,     32, 32   ),
    Architecture(32,    False, 8,     64, 32   ),
    Architecture(32,    False, 16,    8,  32   ),
    Architecture(32,    False, 16,    16, 32   ),
    Architecture(32,    False, 16,    32, 32   ),
    Architecture(32,    False, 16,    64, 32   ),
    Architecture(32,    False, 32,    8,  32   ),
    Architecture(32,    False, 32,    16, 32   ),
    Architecture(32,    False, 32,    32, 32   ),
    Architecture(32,    False, 32,    64, 32   ),
    Architecture(32,    8,     8,     8,  32   ),
    Architecture(32,    8,     8,     16, 32   ),
    Architecture(32,    8,     8,     32, 32   ),
    Architecture(32,    8,     16,    8,  32   ),
    Architecture(32,    8,     16,    16, 32   ),
    Architecture(32,    8,     16,    32, 32   ),
    Architecture(32,    8,     32,    8,  32   ),
    Architecture(32,    8,     32,    16, 32   ),
    Architecture(32,    8,     32,    32, 32   ),
    Architecture(32,    16,    8,     8,  32   ),
    Architecture(32,    16,    8,     16, 32   ),
    Architecture(32,    16,    8,     32, 32   ),
    Architecture(32,    16,    16,    8,  32   ),
    Architecture(32,    16,    16,    16, 32   ),
    Architecture(32,    16,    16,    32, 32   ),
    Architecture(32,    16,    32,    8,  32   ),
    Architecture(32,    16,    32,    16, 32   ),
    Architecture(32,    16,    32,    32, 32   ),
    Architecture(32,    32,    32,    32, 32   )]

for case in range(1, 5):
    model = LSTM(case=case, look_back=10, verbose=0, epochs=300, output="save")
    model.preprocess()
    for architecture in architectures:
        architecture.model = model
        architecture.reset_model()
        fit_manual_model(model, "train")
        fit_manual_model(model, "validate")
        fit_manual_model(model, "test")
        model.save_results_summary()


#fit(model, "train")
#fit(model, "validate")
#fit(model, "test")
#model.save_results_summary()

#load(model, "train")
#load(model, "validate")
#load(model, "test")
