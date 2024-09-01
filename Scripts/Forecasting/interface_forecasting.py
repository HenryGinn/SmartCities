import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
import os
import datetime

import matplotlib.pyplot as plt
import numpy as np

from lstm import LSTM
from arima import ARIMA
from model import Model
from architecture import Architecture


plt.close("all")

def load(model, fit_category, predict_function="predict"):
    print(f"     {fit_category}", datetime.datetime.now())
    model.set_fit_category(fit_category)
    model.preprocess()
    model.load()
    #output(model, predict_function)

def fit(model, fit_category, predict_function="predict"):
    print(f"     {fit_category}", datetime.datetime.now())
    model.set_fit_category(fit_category)
    model.preprocess()
    model.fit()
    model.save()
    output(model, predict_function)

def fit_manual_model(model, fit_category, predict_function="predict"):
    print(f"     {fit_category}", datetime.datetime.now())
    model.set_fit_category(fit_category)
    model.preprocess()
    model.fit()
    #model.save()
    model.plot_history()
    output(model, predict_function)

def output(model, predict_function="predict"):
    getattr(model, predict_function)()
    model.postprocess()
    model.output_results(plot_type="Crime Count", stage="Normalised")
    model.create_correlograms()
    model.create_histogram()
    model.output_results(plot_type="Crime Count", stage="Original")
    model.add_to_results_summary()
    model.save_time_series()


def run():
    match method:
        case "LSTM"  : model = run_LSTM()
        case "SARIMA": model = run_SARIMA()

def run_LSTM():
    model = LSTM(case=case_number, look_back=24, output_folder="Results",
                 verbose=0, epochs=25, output="save", folder_name="LSTM")
    architecture = architectures[case_number]
    architecture.model = model
    architecture.create_model()
    fit_manual_model(model, "validate", "predict_test")
    fit_manual_model(model, "test", "predict_test")
    return model

def run_SARIMA():
    order, seasonal = orders[case_number]
    model = ARIMA(case=case_number, order=order, output_folder="Results",
                  seasonal_order=seasonal, output="save", folder_name="SARIMA")
    fit(model, "validate", "predict_test")
    fit(model, "test", "predict_test")
    return model


architectures = {
    1: Architecture(False, False, 32,    64, False),
    2: Architecture(32   , False, False, 64, False),
    3: Architecture(32   , False, False, 32, False),
    4: Architecture(32   , False, False, 32, False),}

orders = {
    1: ((5, 1, 1), (0, 0, 0, 0)),
    2: ((2, 0, 1), (2, 1, 2, 12)),
    3: ((5, 0, 1), (0, 0, 0, 0)),
    4: ((7, 0, 3), (2, 1, 2, 12))}


methods = ["LSTM", "SARIMA"]
for method in methods[:1]:
    for case_number in range(1, 5):
        print(method, case_number)
        run()


# Defining different architectures for validation

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

orders = [(p, d, q) for p in range(9) for d in range(2) for q in range(4)]
seasonals = [(0, 0, 0, 12), (2, 1, 2, 12)]


# Testing a range of architectures

"""
# LSTM
for case_number in range(1, 5):
    model = LSTM(case=case_number, look_back=24, verbose=0, epochs=25, output="save")
    for architecture in architectures:
        architecture.model = model
        architecture.reset_model()
        print("")
        print(case_number, model.folder_name)
        fit_manual_model(model, "train")
        fit_manual_model(model, "validate")
        fit_manual_model(model, "test")
        model.save_results_summary()
"""

"""
# ARIMA
for case_number in range(1, 5):
    for seasonal in seasonals:
        for order in orders:      
            try:
                model = ARIMA(case=case_number, order=order, 
                              seasonal_order=seasonal, output="save")
                print("")
                print(case_number, model.folder_name)
                fit(model, "train")
                fit(model, "validate")
                fit(model, "test")
                model.save_results_summary()
            except:
                print("Fail")
"""
