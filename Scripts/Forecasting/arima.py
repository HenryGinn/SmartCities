from os.path import join

from hgutilities import defaults
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA

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
        self.forecaster = ARIMA(self.residuals.reshape(-1), order=self.order, seasonal_order=self.seasonal_order)
        self.forecaster = self.forecaster.fit()

    def predict(self):
        start = self.order[2]
        self.modelled = np.zeros(self.length_forecast)
        self.modelled[:start] = self.residuals[:start]
        self.modelled[start:] = self.forecaster.predict(start=start, end=self.length_forecast)
        self.postprocess()


defaults.load(ARIMA)
