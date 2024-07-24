from os.path import join
from os.path import dirname
import warnings

import numpy as np
from scipy.stats import norm
from hgutilities import defaults, utils
import matplotlib.pyplot as plt

from series import Series


plt.rcParams["font.family"] = "Times New Roman"
#plt.rcParams["font.family"] = "Wensleydale"


class Plot(Series):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Plot creation commands
    
    def update_figure(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.predict()
        self.extend_dataframe()
        self.create_figure()
        
    def output_results(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.extend_dataframe()
        self.create_figure()

    def create_figure(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.initiate_figure()
        self.create_plot(loc=0, title=self.title)
        self.output_figure()

    def initiate_figure(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        self.ax = self.fig.add_axes(self.axis_size)
    
    def create_plot(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_purpose_indicator()
        self.add_interval_annotations_to_plot()
        self.add_lines_to_plot()
        self.plot_peripherals()

    def add_lines_to_plot(self):
        match self.plot_type:
            case "Data"     : self.add_modelled_results_to_plot()
            case "Residuals": self.add_residuals_results_to_plot()
            case _: pass

    def create_histogram(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.initiate_figure()
        self.plot_histogram()
        self.plot_histogram_features()
        self.output_figure()


    # Plotting data
    
    def add_modelled_results_to_plot(self):
        self.add_original_to_plot()
        self.add_modelled_to_plot()

    def add_residuals_results_to_plot(self):
        self.add_residuals_to_plot()
        zeros = np.zeros(self.length_forecast)
        zeros[self.length:self.length_forecast] = np.nan
        self.plot_array(zeros, label=None, color=self.blue)

    def set_purpose_indicator(self):
        purpose_indicator = np.array(["ABCDEFGH"] * self.length_forecast)
        purpose_indicator[self.slice_train]    = "Train"
        purpose_indicator[self.slice_validate] = "Validate"
        purpose_indicator[self.slice_test]     = "Test"
        purpose_indicator[self.slice_forecast] = "Forecast"
        self.time_series["Purpose"] = purpose_indicator

    def add_original_to_plot(self):
        self.ax.plot(self.time_series[f"Data{self.stage}"],
                     label=self.label_original,
                     color=self.purple)
    
    def add_modelled_to_plot(self):
        self.ax.plot(self.time_series[f"Modelled{self.stage}"],
                     label=self.label_modelled,
                     color=self.blue)

    def add_residuals_to_plot(self):
        self.ax.plot(self.time_series[f"Residuals{self.stage}"],
                     label=self.label_original,
                     color=self.purple)

    def plot_array(self, array, label, color=None, **kwargs):
        self.time_series.loc[:, label] = array
        self.ax.plot(self.time_series[label], label=label,
                     color=color, **kwargs)
        
    def plot_histogram(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.histogram = self.ax.hist(self.no_nan("Residuals"), bins=self.bins,
                                      color=self.purple, density=True)
        self.plot_peripherals(plot_type="Histogram")

    def plot_histogram_features(self):
        self.plot_histogram_centreline()
        if self.draw_normal_dist:
            self.plot_histogram_normal()

    def plot_histogram_centreline(self):
        maximum_height = np.max(self.histogram[0])
        values = ([0, 0], [0, maximum_height*1.1])
        self.ax.plot(*values, linewidth=2, color=self.blue, dashes=self.dashes)

    def plot_histogram_normal(self):
        mean, std_dev = norm.fit(self.no_nan("Residuals"))
        x_values = np.linspace(*plt.xlim(), 100)
        y_values = norm.pdf(x_values, mean, std_dev)
        self.ax.plot(x_values, y_values, color=self.blue)
        

    # Peripherals
    
    def plot_peripherals(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.plot_peripherals_axes()
        self.set_title()
        self.add_legend()

    def plot_peripherals_axes(self):
        self.set_axis_labels()
        self.set_ticks()

    def set_axis_labels(self):
        match self.plot_type:
            case "Data"     : self.do_set_axis_labels("Date", self.y_label_crime)
            case "Residuals": self.do_set_axis_labels("Date", self.y_label_residuals)
            case "Histogram": self.do_set_axis_labels("Residuals", self.y_label_histogram)
            case "ACF"      : self.do_set_axis_labels("Lag (Months)", self.y_label_acf)
            case "PACF"     : self.do_set_axis_labels("Lag (Months)", self.y_label_pacf)

    def do_set_axis_labels(self, x_axis_label, y_axis_label):
        self.ax.set_xlabel(x_axis_label, fontsize=self.fontsize_labels)
        self.ax.set_ylabel(y_axis_label, fontsize=self.fontsize_labels)

    def set_ticks(self):
        self.ax.xaxis.set_tick_params(labelsize=self.fontsize_ticks)
        self.ax.yaxis.set_tick_params(labelsize=self.fontsize_ticks)

    def set_title(self):
        self.ax.set_title(self.title, pad=self.title_pad,
                          fontsize=self.fontsize_title)

    def add_legend(self):
        if self.legend_non_trivial():
            self.ax.legend(loc=self.loc, fontsize=self.fontsize_legend,
                           bbox_to_anchor=self.legend_bbox_to_anchor)

    def legend_non_trivial(self):
        handles, labels = self.ax.get_legend_handles_labels()
        non_trivial = (len(labels) > 1)
        return non_trivial


    # Annotating different data zones

    def add_interval_annotations_to_plot(self):
        self.extend_axes()
        self.text_height = self.values_max + 0.05*self.values_range
        self.add_interval_lines_to_plot()
        self.add_interval_labels_to_plot()

    def extend_axes(self):
        values = self.get_plotted_values()
        self.values_min = np.nanmin(values)
        self.values_max = np.nanmax(values)
        self.values_range = self.values_max - self.values_min
        upper_limit = self.values_max + 0.15*self.values_range
        self.ax.set_ylim(self.values_min, upper_limit)

    def get_plotted_values(self):
        match self.plot_type:
            case "Data"     : data = self.get_plotted_values_data()
            case "Residuals": data = self.get_plotted_values_residuals()
            case _          : data = None
        return data

    def get_plotted_values_data(self):
        columns = [f"Data{self.stage}", f"Modelled{self.stage}"]
        data = self.time_series[columns].values.reshape(-1)
        return data

    def get_plotted_values_residuals(self):
        data = self.time_series[f"Residuals{self.stage}"].values
        return data

    def add_interval_lines_to_plot(self):
        self.add_interval_line_to_plot(self.index_train)
        self.add_interval_line_to_plot(self.index_validate)
        self.add_interval_line_to_plot(self.length)

    def add_interval_line_to_plot(self, index):
        indices = np.array([self.time_series.index[index] for i in range(25)])
        points = np.linspace(self.values_min, self.values_max, 25)
        self.ax.plot(indices, points, color=self.grey,
                dashes=self.dashes, markersize=self.markersize)

    def add_interval_labels_to_plot(self):
        self.add_interval_label_to_plot("Training", 0, self.index_train)
        self.add_interval_label_to_plot("Validation", self.index_train, self.index_validate)
        self.add_interval_label_to_plot("Testing", self.index_validate, self.length)
        self.add_interval_labels_to_plot_forecast()

    def add_interval_label_to_plot(self, label, start, end):
        time_start = self.time_series.index[start]
        time_end = self.time_series.index[end]
        time = time_start + (time_end - time_start) / 2
        self.ax.text(time, self.text_height, label, ha="center",
                     fontsize=self.fontsize_interval_label)

    def add_interval_labels_to_plot_forecast(self):
        if self.plot_type == "Data":
            self.add_interval_label_to_plot(
                "Forecast", self.length, self.length_forecast-1)

    # Output
    def output_figure(self):
        self.set_figure_name()
        match self.output:
            case "save": self.save_figure()
            case "show": plt.show()
            case _: pass

    def set_figure_name(self):
        if not hasattr(self, "figure_name") or self.figure_name is None:
            self.generate_figure_name()
        self.fig.canvas.manager.set_window_title(self.figure_name)

    def generate_figure_name(self):
        self.figure_name = utils.get_file_name(
            {"Case": self.case, "Title": self.title}, timestamp=False)

    def save_figure(self):
        self.set_path_output()
        plt.savefig(self.path_output, format=self.format)
        self.figure_name = None

    def set_path_output(self):
        self.path_output = join(self.path_output_forecast,
                                f"{self.figure_name}.{self.format}")
        utils.make_folder(dirname(self.path_output))

defaults.load(Plot)
