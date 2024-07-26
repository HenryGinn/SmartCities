from os.path import join
import pickle

from hgutilities import defaults
import numpy as np
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA as Arima

from model import Model


class ARIMA(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_model_files_paths(self):
        self.path_model_arima = join(
            self.path_model, f"ARIMA.pkl")

    def plot_linear_approximation(self, **kwargs):
        self.title = self.title_linear_approximation
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.processed_log, "Log", color=self.color_original)
        self.plot_array(self.linear_approximation, "Trend", color=self.color_modelled)
        self.plot_peripherals_base()

    def determine_hyperparameters(self, **kwargs):
        hyperparameter_obj = auto_arima(self.data)
        self.order = hyperparameter_obj.order
        self.seasonal_order = hyperparameter_obj.seasonal_order

    def load(self):
        with open(self.path_model_arima, "rb") as file:
            self.forecaster = pickle.load(file)
        self.order = self.forecaster.specification["order"]
        self.seasonal_order = self.forecaster.specification["seasonal_order"]

    def save(self):
        with open(self.path_model_arima, "wb") as file:
            pickle.dump(self.forecaster, file)

    def fit(self):
        self.forecaster = Arima(self.data,
                                order=self.order,
                                seasonal_order=self.seasonal_order)
        self.forecaster = self.forecaster.fit()

    def predict(self):
        start = self.order[2]
        self.modelled = np.zeros(self.length_forecast)
        self.modelled[:start] = self.data[:start]
        self.modelled[start:] = self.forecaster.predict(
                start=start, end=self.length_forecast-1)

    def plot_peripherals_residuals_comparison(self):
        self.plot_peripherals(title="Comparing Residuals",
                              plot_type="Crime")


defaults.load(ARIMA)
