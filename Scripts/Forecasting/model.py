from hgutilities import defaults
import numpy as np

from plot import Plot
from process import Process


class Model(Plot, Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


defaults.load(Model)
