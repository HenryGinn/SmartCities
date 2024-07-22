from hgutilities import defaults
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import linregress
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

from series import Series


class Process(Series):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        defaults.kwargs(self, kwargs)

    # Preprocessing transformations
    def preprocess(self):
        self.preprocess_logs()
        self.subtract_trend()
        self.subtract_seasonal()
        self.normalise_residuals()

    def preprocess_logs(self):
        if self.log:
            self.preprocess_logs_true()
        else:
            self.preprocess_logs_false()

    def preprocess_logs_true(self):
        self.processed_log = np.log(self.data)
        self.y_label_processed = "Log(Crimes per Person per 100,000 People)"

    def preprocess_logs_false(self):
        self.processed_log = self.data.copy()
        self.y_label_processed = "Crimes per 100,000 People"

    def subtract_trend(self):
        (self.slope, self.intercept, self.r_value, self.p_value,
         self.standard_error) = linregress(np.arange(self.length),
                                           self.processed_log)
        self.set_linear_approximation(self.length)
        self.residuals = self.processed_log - self.time_series["Linear"].values

    def set_linear_approximation(self, length):
        self.time_series.loc[:, "Linear"] = (
            np.arange(length)*self.slope + self.intercept)

    def subtract_seasonal(self):
        if self.seasonal:
            self.time_series.loc[:, "Residuals Preseasonal"] = self.residuals
            self.set_monthly_averages()
            self.add_monthly_averages_to_time_series()
            self.residuals -= self.time_series["Monthly Average"].values

    def set_monthly_averages(self):
        self.monthly_averages = (
            self.time_series["Residuals Preseasonal"].groupby(
            self.time_series.index.month).mean())

    def add_monthly_averages_to_time_series(self):
        self.time_series.loc[:, "Monthly Average"] = (
            self.time_series.index.month.map(
            self.monthly_averages))

    def normalise_residuals(self):
        self.residuals, self.transform_data = (
            self.transform_forward(self.residuals))

    def transform_forward(self, data, **kwargs):
        defaults.kwargs(self, kwargs)
        a, b = self.feature_range
        c, d = np.min(data[:]), np.max(data[:])
        scale, offset = (b - a) / (d - c), (a*d - b*c) / (d - c)
        transformed = data * scale + offset
        return transformed, (offset, scale)

    def transform_backward(self, transformed, transform_data):
        offset, scale = transform_data
        data = (transformed - offset) / scale
        return data


    # Reversing transformations
    def postprocess(self):
        self.unnormalise_residuals()
        self.add_seasonal()
        self.add_trend()
        self.postprocess_logs()
        
    def unnormalise_residuals(self):
        self.modelled = self.transform_backward(
            self.residuals, self.transform_data)
        
    def add_seasonal(self):
        if self.seasonal:
            self.add_monthly_averages_to_time_series()
            self.modelled += self.time_series["Monthly Average"].values

    def add_trend(self):
        self.set_linear_approximation(self.length_forecast)
        self.modelled += self.time_series["Linear"].values

    def postprocess_logs(self):
        if self.log:
            self.modelled = np.exp(self.modelled)


    # Analysis
    def set_correlations(self):
        self.acf = sm.tsa.acf(self.residuals, nlags=24)
        self.pacf = sm.tsa.pacf(self.residuals, nlags=24)
        self.set_confidence_intervals()

    def set_confidence_intervals(self):
        const = -1/np.sqrt(self.residuals.size)
        self.cf_confidence = -const**2 + 2*np.array([-const, const])
        self.cf_confidence = np.tile(self.cf_confidence, (2, 1))
    

defaults.load(Process)
