from os.path import join
from os.path import dirname
import warnings

import pandas as pd
import numpy as np
from hgutilities import defaults, utils
import matplotlib.pyplot as plt

from utils import get_base_path


warnings.simplefilter(action='ignore', category=FutureWarning)

plt.rcParams["font.family"] = "Times New Roman"

class Forecast():

    def __init__(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.load_time_series()
        self.set_splits()
        self.extend_dataframe()

    def load_time_series(self):
        self.set_main_paths()
        path = join(self.path_data, f"Case_{self.case}.csv")
        self.read_data(path)
        self.read_metadata(path)

    def set_main_paths(self):
        self.path_base = get_base_path(self)
        self.path_data = join(self.path_base, "Data", "Forecast")
        self.path_output_base = join(self.path_base, "Output")

    def read_data(self, path):
        self.time_series = pd.read_csv(
            path, skiprows=3, index_col="Time",
            date_format="%Y-%m-%d", parse_dates=True)
        self.data = self.time_series["Original"].values

    def read_metadata(self, path):
        with open(path) as file:
            self.borough = self.extract_from_line(file)
            self.major   = self.extract_from_line(file)
            self.lsoa    = self.extract_from_line(file)

    def extract_from_line(self, file):
        metadata = file.readline().strip("\n").split(",")[1]

    def extend_dataframe(self):
        original_end = self.time_series.index[self.length - 1]
        forecast_dates = pd.date_range(start=original_end, freq='MS',
                                       periods=self.forecast_length + 1)[1:]
        new_data = {"Original": np.array([None] * self.forecast_length)}
        extended = pd.DataFrame(new_data, index=forecast_dates)
        self.time_series = pd.concat([self.time_series, extended])


    # Defining the train, validate, and test data
    def set_splits(self):
        self.length = len(self.data)
        self.set_split_index_points()
        self.set_split_indices()
        self.set_data_splits()

    def set_split_index_points(self):
        self.index_train    = int(self.length * self.train)
        self.index_validate = int(self.length * self.validate) + self.index_train
        self.length_forecast = int(self.length * self.forecast) + self.length
        self.forecast_length = self.length_forecast - self.length

    def set_split_indices(self):
        self.indices_train    = np.arange(0, self.index_train)
        self.indices_validate = np.arange(self.index_train, self.index_validate)
        self.indices_test     = np.arange(self.index_validate, self.length)
        self.indices_forecast = np.arange(self.length, self.length_forecast)

    def set_data_splits(self):
        self.data_train    = self.data[self.indices_train]
        self.data_validate = self.data[self.indices_validate]
        self.data_test     = self.data[self.indices_test]


    def create_forecast(self):
        self.modelled = (np.ones(self.length_forecast)*self.data.mean() +
            (np.random.rand(self.length_forecast)-0.5)*1*self.data.std())
        

    # Plotting
    def create_plot(self, fig, ax, **kwargs):
        self.initiate_plot(fig, ax, **kwargs)
        self.add_data_to_plot()
        self.plot_peripherals()
        self.output_figure()

    def initiate_plot(self, fig, ax, **kwargs):
        self.fig, self.ax = fig, ax
        defaults.kwargs(self, kwargs)
        self.construct_dataframe()
        
    def construct_dataframe(self):
        self.time_series.loc[:, "Modelled"] = self.modelled
        self.time_series.loc[:, "Purpose"] = self.get_purpose_indicator()

    def get_purpose_indicator(self):
        purpose_indicator = np.array(["ABCDEFGH"] * self.length_forecast)
        purpose_indicator[self.indices_train]    = "Train"
        purpose_indicator[self.indices_validate] = "Validate"
        purpose_indicator[self.indices_test]     = "Test"
        purpose_indicator[self.indices_forecast] = "Forecast"
        return purpose_indicator

    def add_data_to_plot(self):
        self.add_original_to_plot()
        self.add_modelled_to_plot()

    def add_original_to_plot(self):
        self.ax.plot(self.time_series["Original"],
                     label=self.label_original,
                     color=self.color_original)
    
    def add_modelled_to_plot(self):
        self.ax.plot(self.time_series["Modelled"],
                     label=self.label_modelled,
                     color=self.color_modelled)
        

    def plot_peripherals(self):
        self.plot_peripherals_axes()
        self.set_title()
        self.add_legend()
        self.add_interval_annotations_to_plot()

    def plot_peripherals_axes(self):
        self.extend_axes()
        self.set_axis_labels()
        self.set_ticks()

    def extend_axes(self):
        data = self.time_series[["Original", "Modelled"]].values.reshape(-1)
        self.data_max = np.nanmax(data)
        self.ax.set_ylim(0, 1.1*self.data_max)

    def set_axis_labels(self):
        self.ax.set_xlabel("Date", fontsize=self.fontsize_labels)
        self.ax.set_ylabel(self.y_label, fontsize=self.fontsize_labels)

    def set_ticks(self):
        self.ax.xaxis.set_tick_params(labelsize=self.fontsize_ticks)
        self.ax.yaxis.set_tick_params(labelsize=self.fontsize_ticks)

    def set_title(self):
        self.ax.set_title(self.title, pad=self.title_pad,
                          fontsize=self.fontsize_title)

    def add_legend(self):
        self.ax.legend(loc=self.loc, fontsize=self.fontsize_legend,
                       bbox_to_anchor=self.legend_bbox_to_anchor)

    def add_interval_annotations_to_plot(self):
        self.line_limit = self.data_max
        self.text_height = self.line_limit * 1.03
        self.add_interval_lines_to_plot()
        self.add_interval_labels_to_plot()

    def add_interval_lines_to_plot(self):
        self.add_interval_line_to_plot(self.index_train)
        self.add_interval_line_to_plot(self.index_validate)
        self.add_interval_line_to_plot(self.length)

    def add_interval_line_to_plot(self, index):
        indices = np.array([self.time_series.index[index] for i in range(25)])
        points = np.linspace(0, self.line_limit+1, 25)
        self.ax.plot(indices, points, color=self.color_divider,
                dashes=(3, 3), markersize=self.markersize, linestyle="--")

    def add_interval_labels_to_plot(self):
        self.add_interval_label_to_plot("Training", 0, self.index_train)
        self.add_interval_label_to_plot("Validation", self.index_train, self.index_validate)
        self.add_interval_label_to_plot("Testing", self.index_validate, self.length)
        self.add_interval_label_to_plot("Forecast", self.length, self.length_forecast)

    def add_interval_label_to_plot(self, label, start, end):
        index = self.time_series.index[int((start + end)/2)]
        self.ax.text(index, self.text_height, label, ha="center",
                     fontsize=self.fontsize_interval_label)

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
        self.figure_name = utils.get_file_name({"Case": self.case}, timestamp=False)

    def save_figure(self):
        self.set_path_output()
        plt.savefig(self.path_output, format=self.format)

    def set_path_output(self):
        self.path_output = join(self.path_output_base, "Forecasting",
                f"Case {self.case}", f"{self.figure_name}.{self.format}")
        utils.make_folder(dirname(self.path_output))

defaults.load(Forecast)



























