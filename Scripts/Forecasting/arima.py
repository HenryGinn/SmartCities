from os.path import join
from warnings import filterwarnings
from time import time
import pickle

from hgutilities import defaults
import numpy as np
from statsmodels.tsa.arima.model import ARIMA as Arima

from model import Model


filterwarnings("ignore", module="statsmodels")


class ARIMA(Model):

    model_type = "ARIMA"

    def __init__(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_folder_name()
        super().__init__(**kwargs)
    
    def set_folder_name(self):
        p, d, q = self.order
        P, D, Q, _ = self.seasonal_order
        self.folder_name = (f"{p}_{d}_{q}__{P}_{D}_{Q}")

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

    def fit(self):
        fitting_data = self.data[self.slice_data]
        self.forecaster = Arima(fitting_data, order=self.order,
                                seasonal_order=self.seasonal_order)
        start = time()
        self.forecaster = self.forecaster.fit()
        self.training_time = time() - start

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

    def predict_values(self, _, index):
        start = self.order[2]
        self.modelled = np.zeros(self.length)
        self.modelled[:start] = self.data[:start]
        self.modelled[start:index + 1] = self.forecaster.predict(
            start=start, end=index, information_set="predicted")


defaults.load(ARIMA)
