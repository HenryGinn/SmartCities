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
        self.length = len(self.data)
        self.set_split_points()

    def load_time_series(self):
        self.set_main_paths()
        path = join(self.path_data, f"Case_{self.case}.csv")
        self.read_data(path)
        self.read_metadata(path)

    def set_main_paths(self):
        self.path_base = get_base_path(self)
        self.path_data = join(self.path_base, "Data", "Forecast")
        self.path_output_base = join(self.path_base, "Output")
        self.path_output_forecast = join(
            self.path_output_base, "Forecasting", f"Case_{self.case}")
        utils.make_folder(self.path_output_forecast)

    def read_data(self, path):
        self.time_series = pd.read_csv(
            path, skiprows=3, index_col="Time", dtype=np.float32,
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
        if len(self.time_series) == self.length:
            forecast_dates = self.get_forecast_dates()
            new_data = {"Original": np.array([None] * self.forecast_length)}
            extended = pd.DataFrame(new_data, index=forecast_dates)
            self.time_series = pd.concat([self.time_series, extended])

    def get_forecast_dates(self):
        original_end = self.time_series.index[self.length - 1]
        forecast_dates = pd.date_range(start=original_end, freq='MS',
                                       periods=self.forecast_length + 1)[1:]
        return forecast_dates


    # Defining the train, validate, and test data
    def set_split_points(self):
        self.set_split_index_points()
        self.set_split_indices()

    def set_split_index_points(self):
        self.index_train    = int(self.length * self.train)
        self.index_validate = int(self.length * self.validate) + self.index_train
        self.length_forecast = int(self.length * self.forecast) + self.length
        self.forecast_length = self.length_forecast - self.length

    def set_split_indices(self):
        self.slice_train    = slice(0, self.index_train)
        self.slice_validate = slice(self.index_train, self.index_validate)
        self.slice_test     = slice(self.index_validate, self.length)
        self.slice_forecast = slice(self.length, self.length_forecast)

    def set_iterable_splits(self, attribute, look_back=False):
        self.set_iterable_split(attribute, "train", look_back)
        self.set_iterable_split(attribute, "validate", look_back)
        self.set_iterable_split(attribute, "test", look_back)

    def set_iterable_split(self, attribute, split, look_back):
        iterable = getattr(self, attribute)
        other_dimensions = ((len(iterable.shape) - 1) * [slice(None)])
        slice_first = self.get_slice_first(split, look_back)
        slice_all = [slice_first, *other_dimensions]
        setattr(self, f"{attribute}_{split}", iterable[*slice_all])

    def get_slice_first(self, split, look_back):
        base_slice = getattr(self, f"slice_{split}")
        if look_back:
            return self.get_slice_first_look_back(base_slice, split)
        else:
            return base_slice

    def get_slice_first_look_back(self, base_slice, split):
        if split == "train":
            return slice(base_slice.start,
                         base_slice.stop - self.look_back + 1)
        else:
            return slice(base_slice.start - self.look_back + 1,
                         base_slice.stop - self.look_back + 1)

    def predict(self):
        self.modelled = np.zeros((self.length_forecast))
        

    # Plotting
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
        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_axes(self.axis_size)

    def add_modelled_results_to_plot(self):
        self.construct_dataframe()
        self.extend_axes()
        self.add_original_to_plot()
        self.add_modelled_to_plot()
        
    def construct_dataframe(self):
        self.time_series.loc[:, "Modelled"] = self.modelled
        self.time_series.loc[:, "Purpose"] = self.get_purpose_indicator()

    def get_purpose_indicator(self):
        purpose_indicator = np.array(["ABCDEFGH"] * self.length_forecast)
        purpose_indicator[self.slice_train]    = "Train"
        purpose_indicator[self.slice_validate] = "Validate"
        purpose_indicator[self.slice_test]     = "Test"
        purpose_indicator[self.slice_forecast] = "Forecast"
        return purpose_indicator

    def add_original_to_plot(self):
        self.ax.plot(self.time_series["Original"],
                     label=self.label_original,
                     color=self.color_original)
    
    def add_modelled_to_plot(self):
        self.ax.plot(self.time_series["Modelled"],
                     label=self.label_modelled,
                     color=self.color_modelled)

    def plot_array(self, array, label, color=None):
        self.time_series.loc[:, label] = array
        self.ax.plot(self.time_series[label], label=label, color=color)
        

    def plot_peripherals(self):
        self.plot_peripherals_base()
        self.add_interval_annotations_to_plot()
        self.extend_axes()

    def plot_peripherals_base(self):
        self.plot_peripherals_axes()
        self.set_title()
        self.add_legend()

    def plot_peripherals_axes(self):
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
        if not self.ax.get_legend_handles_labels() == ([], []):
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
        self.add_interval_label_to_plot("Forecast", self.length, self.length_forecast-1)

    def add_interval_label_to_plot(self, label, start, end):
        time_start = self.time_series.index[start]
        time_end = self.time_series.index[end]
        time = time_start + (time_end - time_start) / 2
        self.ax.text(time, self.text_height, label, ha="center",
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
        self.figure_name = utils.get_file_name(
            {"Case": self.case, "Title": self.title}, timestamp=False)

    def save_figure(self):
        self.set_path_output()
        plt.savefig(self.path_output, format=self.format)

    def set_path_output(self):
        self.path_output = join(self.path_output_forecast,
                                f"{self.figure_name}.{self.format}")
        utils.make_folder(dirname(self.path_output))

defaults.load(Forecast)



























