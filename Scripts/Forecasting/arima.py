from os.path import join

from hgutilities import defaults
import numpy as np
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA as Arima

from model import Model


class ARIMA(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_model_files_paths(self):
        self.path_model_hyperparameters = join(
            self.path_model, f"ARIMA Hyperparameters.json")

    def plot_linear_approximation(self, **kwargs):
        self.title = self.title_linear_approximation
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.processed_log, "Log", color=self.color_original)
        self.plot_array(self.linear_approximation, "Trend", color=self.color_modelled)
        self.plot_peripherals_base()

    def determine_hyperparameters(self, **kwargs):
        self.ensure_residuals()
        hyperparameter_obj = auto_arima(self.residuals)
        self.order = hyperparameter_obj.order
        self.seasonal_order = hyperparameter_obj.seasonal_order

    def load(self):
        pass

    def fit(self):
        self.forecaster = Arima(self.residuals,
                                order=self.order,
                                seasonal_order=self.seasonal_order)
        self.forecaster = self.forecaster.fit()

    def predict(self):
        start = self.order[2]
        self.modelled = np.zeros(self.length_forecast)
        self.modelled[:start] = self.residuals[:start]
        self.modelled[start:] = self.forecaster.predict(
                start=start, end=self.length_forecast-1)
        self.predict_process()

    def predict_process(self):
        self.extend_dataframe()
        self.add_column(self.residuals, "Residuals Processed")
        self.residuals = self.modelled[:self.length] - self.residuals
        self.add_column(self.residuals, "Residuals ARIMA")

    def compare_residuals(self):
        self.initiate_figure()
        self.ax.plot(self.time_series["Residuals ARIMA"], label="ARIMA", color=self.purple)
        self.ax.plot(self.time_series["Residuals Processed"], label="Original", color=self.blue)
        self.plot_peripherals_residuals_comparison()

    def plot_peripherals_residuals_comparison(self):
        self.plot_peripherals(title="Comparing Residuals After Modelling With ARIMA",
                              plot_type="Crime")


defaults.load(ARIMA)
