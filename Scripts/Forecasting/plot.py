from os.path import join
from os.path import dirname
import warnings

from hgutilities import defaults
import numpy as np
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

    def create_figure(self):
        self.initiate_figure()
        self.create_plot(self.fig, self.ax, loc=0, title=self.title)
        self.output_figure()
    
    def create_plot(self, fig, ax, **kwargs):
        self.add_modelled_results_to_plot()
        self.plot_peripherals()

    def initiate_figure(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        self.ax = self.fig.add_axes(self.axis_size)


    # Plotting modelled data
    def add_modelled_results_to_plot(self):
        self.set_purpose_indicator()
        self.add_original_to_plot()
        self.add_modelled_to_plot()
        self.add_interval_annotations_to_plot()

    def set_purpose_indicator(self):
        purpose_indicator = np.array(["ABCDEFGH"] * self.length_forecast)
        purpose_indicator[self.slice_train]    = "Train"
        purpose_indicator[self.slice_validate] = "Validate"
        purpose_indicator[self.slice_test]     = "Test"
        purpose_indicator[self.slice_forecast] = "Forecast"
        self.time_series["Purpose"] = purpose_indicator

    def add_original_to_plot(self):
        self.ax.plot(self.time_series[f"Residuals{self.stage}"],
                     label=self.label_original,
                     color=self.purple)
    
    def add_modelled_to_plot(self):
        self.ax.plot(self.time_series[f"Modelled{self.stage}"],
                     label=self.label_modelled,
                     color=self.blue)

    def plot_array(self, array, label, color=None):
        self.time_series.loc[:, label] = array
        self.ax.plot(self.time_series[label], label=label, color=color)
        

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
            case "Crime": self.do_set_axis_labels("Date", self.y_label_crime)
            case "ACF"  : self.do_set_axis_labels("Lag (Months)", self.y_label_acf)
            case "PACF" : self.do_set_axis_labels("Lag (Months)", self.y_label_pacf)

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
        if not self.ax.get_legend_handles_labels() == ([], []):
            self.ax.legend(loc=self.loc, fontsize=self.fontsize_legend,
                           bbox_to_anchor=self.legend_bbox_to_anchor)


    # Annotating different data zones

    def add_interval_annotations_to_plot(self):
        self.extend_axes()
        self.line_limit = self.data_max
        self.text_height = self.line_limit * 1.03
        self.add_interval_lines_to_plot()
        self.add_interval_labels_to_plot()

    def extend_axes(self):
        columns = [f"Residuals{self.stage}", f"Modelled{self.stage}"]
        data = self.time_series[columns].values.reshape(-1)
        self.data_max = np.nanmax(data)
        self.ax.set_ylim(np.nanmin(data), 1.1*self.data_max)

    def add_interval_lines_to_plot(self):
        self.add_interval_line_to_plot(self.index_train)
        self.add_interval_line_to_plot(self.index_validate)
        self.add_interval_line_to_plot(self.length)

    def add_interval_line_to_plot(self, index):
        indices = np.array([self.time_series.index[index] for i in range(25)])
        points = np.linspace(0, self.line_limit+1, 25)
        self.ax.plot(indices, points, color=self.grey,
                dashes=self.dashes, markersize=self.markersize)

    def add_interval_labels_to_plot(self):
        self.add_interval_label_to_plot("Training", 0, self.index_train)
        self.add_interval_label_to_plot("Validation", self.index_train, self.index_validate)
        self.add_interval_label_to_plot("Testing", self.index_validate, self.length)
        self.add_interval_label_to_plot("Forecast", self.length, self.length_forecast-1)

    def add_interval_label_to_plot(self, label, start, end):
        time_start = self.time_series.index[start]
        time_end = self.time_series.index[end]
        time = time_start + (time_end - time_start) / 2
        self.ax.text(time, self.text_height, label, ha="center",
                     fontsize=self.fontsize_interval_label)


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
