from os.path import join
import pickle

from hgutilities import defaults
import numpy as np
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA as Arima

from model import Model


class ARIMA(Model):

    model_type = "ARIMA"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_model_files_paths(self):
        self.set_path_model_weights("train")
        self.set_path_model_weights("validate")
        self.set_path_model_weights("test")

    def set_path_model_weights(self, fit_category):
        attribute = f"path_model_arima_{fit_category}"
        name = f"ARIMA_{fit_category}.pkl"
        setattr(self, attribute, join(self.path_model, name))

    def plot_linear_approximation(self, **kwargs):
        self.title = self.title_linear_approximation
        defaults.kwargs(self, kwargs)
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.processed_log, "Log", color=self.color_original)
        self.plot_array(self.linear_approximation, "Trend", color=self.color_modelled)
        self.plot_peripherals_base()

    def determine_hyperparameters(self, **kwargs):
        self.hyperparameter_obj = auto_arima(self.data[self.i(stop="test")])
        self.order = self.hyperparameter_obj.order
        self.seasonal_order = self.hyperparameter_obj.seasonal_order
        self.order = (4, 3, 4)
        self.seasonal_order = (2, 0, 0, 12)

    def fit(self):
        fitting_data = self.data[self.slice]
        self.forecaster = Arima(fitting_data, order=self.order,
                                seasonal_order=self.seasonal_order)
        self.forecaster = self.forecaster.fit()

    def load(self):
        path = getattr(self, f"path_model_arima_{self.fit_category}")
        with open(path, "rb") as file:
            self.forecaster = pickle.load(file)
        self.order = self.forecaster.specification["order"]
        self.seasonal_order = self.forecaster.specification["seasonal_order"]

    def save(self):
        path = getattr(self, f"path_model_arima_{self.fit_category}")
        with open(path, "wb") as file:
            pickle.dump(self.forecaster, file)

    def predict_train(self):
        start = self.order[2]
        self.modelled = np.zeros(self.length)
        self.modelled[:start] = self.data[:start]
        self.modelled[start:] = self.forecaster.predict(
                start=start, end=self.index_forecast)


defaults.load(ARIMA)
