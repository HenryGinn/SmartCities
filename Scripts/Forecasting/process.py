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
        self.normalise_data()

    def preprocess_logs(self):
        if self.log:
            self.preprocess_logs_true()
        else:
            self.preprocess_logs_false()
        self.time_series["DataLog"] = self.data.copy()

    def preprocess_logs_true(self):
        self.data = np.log(self.data)
        self.y_label_processed = "Log(Crimes per Person per 100,000 People)"

    def preprocess_logs_false(self):
        self.y_label_processed = "Crimes per 100,000 People"

    def subtract_trend(self):
        (self.slope, self.intercept, self.r_value, self.p_value,
         self.standard_error) = linregress(np.arange(self.length), self.data)
        self.set_linear_approximation(self.length)
        self.data = self.data - self.time_series["Linear"].values
        self.time_series["DataLinear"] = self.data.copy()

    def set_linear_approximation(self, length):
        self.time_series.loc[:, "Linear"] = (
            np.arange(length)*self.slope + self.intercept)

    def subtract_seasonal(self):
        if self.seasonal:
            self.set_monthly_averages()
            self.add_monthly_averages_to_time_series()
            self.data -= self.time_series["MonthlyAverage"].values
            self.time_series["DataSeasons"] = self.data.copy()

    def set_monthly_averages(self):
        self.monthly_averages = (
            self.time_series["DataLinear"].groupby(
            self.time_series.index.month).mean())

    def add_monthly_averages_to_time_series(self):
        self.time_series.loc[:, "MonthlyAverage"] = (
            self.time_series.index.month.map(
            self.monthly_averages))

    def normalise_data(self):
        self.data, self.transform_data = (
            self.transform_forward(self.data))
        self.time_series["DataNormalised"] = self.data.copy()

    def transform_forward(self, data):
        mean, std = np.mean(data[:]), np.std(data[:])
        transformed = (data - mean) / std 
        return transformed, (mean, std)

    def transform_backward(self, transformed):
        mean, std = self.transform_data
        data = transformed * std + mean
        return data


    # Reversing transformations
    def postprocess(self):
        self.unnormalise_modelled()
        self.add_seasonal()
        self.add_trend()
        self.postprocess_logs()
        
    def unnormalise_modelled(self):
        self.modelled = self.transform_backward(self.modelled)
        self.add_modelled_to_time_series("Seasons")
        
    def add_seasonal(self):
        if self.seasonal:
            self.add_monthly_averages_to_time_series()
            self.modelled += self.time_series["MonthlyAverage"].values
        self.add_modelled_to_time_series("Linear")

    def add_trend(self):
        self.set_linear_approximation(self.modelled.size)
        self.modelled += self.time_series["Linear"].values
        self.add_modelled_to_time_series("Log")

    def postprocess_logs(self):
        if self.log:
            self.set_correction_faction()
            self.modelled = np.exp(self.modelled) * self.correction_factor
        self.add_modelled_to_time_series("Original")

    def set_correction_faction(self):
        residuals = self.no_nan("Residuals", stage="Log")
        self.correction_factor = np.mean(np.exp(residuals))

    def add_modelled_to_time_series(self, stage):
        self.time_series[f"Modelled{stage}"] = self.modelled.copy()
        self.set_residuals(stage=stage)


    # Analysis
    def set_correlations(self, **kwargs):
        defaults.kwargs(self, kwargs)
        residuals = self.no_nan("Residuals")
        self.acf = sm.tsa.acf(residuals, nlags=24)
        self.pacf = sm.tsa.pacf(residuals, nlags=24)
        self.set_confidence_intervals(residuals)

    def set_confidence_intervals(self, residuals):
        const = -1/np.sqrt(residuals.size)
        self.cf_confidence = -const**2 + 2*np.array([-const, const])
        self.cf_confidence = np.tile(self.cf_confidence, (2, 1))
    

defaults.load(Process)
