from os.path import join

from hgutilities import defaults, utils
import numpy as np

from plot import Plot
from process import Process


class Model(Plot, Process):

    model_type = "Curve Fitting"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_model_paths()

    def set_model_paths(self):
        self.path_model = join(
            self.path_output_base, "Models", f"Case_{self.case}")
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
        self.modelled = np.zeros(self.length_forecast)

    def post_predict(self):
        self.extend_dataframe()
        self.add_modelled_to_time_series("Normalised")

    def print_time_series(self):
        columns = self.time_series.columns.values
        for column in columns:
            print(f"{column}\n{self.time_series[column].values}")
        print(f"\n{columns}")


defaults.load(Model)
