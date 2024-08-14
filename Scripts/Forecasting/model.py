from os.path import join
from json import dump

from hgutilities import defaults, utils
import numpy as np

from plot import Plot
from process import Process


class Model(Plot, Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_model_paths()
        self.results_summary = []

    def set_model_paths(self):
        self.path_model = join(self.path_output_base,
                               "Forecasting", f"Case_{self.case}",
                               self.folder_name)
        utils.make_folder(self.path_model)
        self.set_model_files_paths()

    def set_model_files_paths(self):
        pass
    

    # Correlograms
    def create_correlograms(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_correlations()
        self.create_acf()
        self.create_pacf()

    def create_acf(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.create_cf(self.acf, "ACF")

    def create_pacf(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.create_cf(self.pacf, "PACF")

    def create_cf(self, cf, plot_type, **kwargs):
        defaults.kwargs(self, kwargs)
        self.plot_cf(cf)
        self.plot_peripherals(plot_type=plot_type)
        self.output_figure()

    def plot_cf(self, cf):
        self.initiate_figure()
        x_axis = np.arange(self.acf.size)
        self.ax.bar(x_axis, cf, width=self.cf_bar_width, color=self.purple)
        self.ax.plot([-0.5, x_axis[-1]+1], self.cf_confidence,
                     color=self.grey, dashes=self.dashes)


    def plot_residuals(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_residuals()
        self.create_figure(plot_type="Residuals")

    def set_residuals(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.residuals = (self.time_series[f"Data{self.stage}"]
                          - self.time_series[f"Modelled{self.stage}"])
        self.time_series[f"Residuals{self.stage}"] = self.residuals.copy()

    def predict(self):
        match self.fit_category:
            case "train"   : self.predict_values(self.index_train, self.index_validate)
            case "validate": self.predict_values(self.index_validate, self.index_test)
            case "test"    : self.predict_values(self.index_test, self.index_forecast)
        self.add_modelled_to_time_series("Normalised")

    def print_time_series(self):
        columns = self.time_series.columns.values
        for column in columns:
            print(f"{column}\n{self.time_series[column].values}")
        print(f"\n{columns}")

    def add_to_results_summary(self):
        self.results_summary.append({"Fit Category": self.fit_category,
                                     "Training Time": self.training_time,
                                     "MSE": np.mean(self.no_nan("Residuals")**2)})

    def save_results_summary(self):
        path = join(self.path_model, "Summary.json")
        with open(path, "w+") as file:
            dump(self.results_summary, file, indent=2)
    
    def save_time_series(self):
        path = join(self.path_model, f"TimeSeries_{self.fit_category}")
        self.time_series.to_csv(path)


defaults.load(Model)
