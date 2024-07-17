from os.path import join

from hgutilities import defaults, utils
import numpy as np

from plot import Plot
from process import Process


class Model(Plot, Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_model_paths()

    def set_model_paths(self):
        self.path_model = join(
            self.path_output_base, "Models", f"Case_{self.case}")
        utils.make_folder(self.path_model)
        self.set_model_files_paths()
    

    # Correlograms
    def create_correlograms(self):
        self.set_correlations()
        self.create_acf()
        self.create_pacf()

    def create_acf(self, **kwargs):
        self.title = f"Autocorrelation Function for Case {self.case}"
        defaults.kwargs(self, kwargs)
        self.create_cf(self.acf, "ACF")

    def create_pacf(self, **kwargs):
        self.title = f"Partial Autocorrelation Function for Case {self.case}"
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
        self.initiate_figure(y_label=self.y_label_processed)
        self.plot_array(self.residuals, None, color=self.color_original)
        self.plot_peripherals_base()

    def ensure_residuals(self):
        if not hasattr(self, "residuals"):
            raise AttributeError("Residuals has not been set.\n"
                "Either assign this manually or call the 'preprocess' method")


defaults.load(Model)
