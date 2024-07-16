from hgutilities import defaults, utils
import numpy as np
import pandas as pd
from scipy.stats import linregress
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
        self.residuals = self.processed_log - self.linear_approximation

    def subtract_seasonal(self):
        dataframe = pd.DataFrame({"Data": self.residuals},
                                 index=self.time_series.index)
        self.monthly_averages = dataframe.groupby(dataframe.index.month).mean()
        self.residuals = (dataframe["Data"] - dataframe.index.month.map(
                self.monthly_averages["Data"])).values

    def normalise_residuals(self):
        self.scaler_linear = MinMaxScaler(feature_range=(-1, 1))
        self.residuals = (self.scaler_linear.fit_transform(
            self.residuals.reshape(-1, 1)))


    # Plotting
    def plot_linear_approximation(self, **kwargs):
        self.title = self.title_linear_approximation
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.processed_log, "Log", color=self.color_original)
        self.plot_array(self.linear_approximation, "Trend", color=self.color_modelled)
        self.plot_peripherals_base()

    def plot_residuals(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.residuals, None, color=self.color_original)
        self.plot_peripherals_base()


defaults.load(ARIMA)
