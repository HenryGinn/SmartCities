from hgutilities import defaults

from plot import Plot
from process import Process


class ARIMA(Plot, Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
