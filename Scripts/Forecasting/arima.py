from hgutilities import defaults, utils
from scipy.stats import linregress
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from forecast import Forecast


class ARIMA(Forecast):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.indices = np.arange(self.length)
        self.preprocess_data()

    def preprocess_data(self):
        self.preprocess_logs()
        self.subtract_trend()

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
         self.standard_error) = linregress(self.indices, self.processed_log)
        self.linear_approximation = self.indices*self.slope + self.intercept
        self.residuals_linear_raw = self.processed_log - self.linear_approximation
        self.normalise_linear_residuals()

    def normalise_linear_residuals(self):
        self.scaler_linear = MinMaxScaler(feature_range=(-1, 1))
        self.residuals_linear = (self.scaler_linear.fit_transform(
            self.residuals_linear_raw.reshape(-1, 1)))

    def plot_linear_approximation(self, **kwargs):
        self.title = self.title_linear_approximation
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.processed_log, "Log", color=self.color_original)
        self.plot_array(self.linear_approximation, "Trend", color=self.color_modelled)
        self.plot_peripherals_base()

    def plot_residuals_linear_raw(self, **kwargs):
        self.title = self.title_residuals_linear_raw
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.residuals_linear_raw, None, color=self.color_original)
        self.plot_peripherals_base()

    def plot_residuals_linear(self, **kwargs):
        self.title = self.title_residuals_linear
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.residuals_linear, None, color=self.color_original)
        self.plot_peripherals_base()


defaults.load(ARIMA)
