import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from hgutilities import defaults, utils

from utils import (get_time_columns, get_capitalised,
                   add_line_breaks)

plt.rcParams["font.family"] = "Times New Roman"


class Time():

    def __init__(self, data, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.data = data.copy()
        self.transpose()

    def transpose(self):
        self.set_columns()
        self.population_weight_data()
        self.data = self.data.set_index(self.columns_non_time, drop=True)
        self.data = self.data.transpose()
        self.convert_to_date_datatype()

    def set_columns(self):
        self.columns = self.data.columns.values
        self.columns_time = get_time_columns(self.data)
        self.columns_non_time = list(set(self.columns) - set(self.columns_time))

    def population_weight_data(self):
        if self.population_weighted and "Population" in self.data.columns.values:
            per_n_people_int = int(str(self.per_n_people).replace(",", ""))
            self.data[self.columns_time] = (per_n_people_int * 
                self.data[self.columns_time].T / self.data["Population"].values).T
            self.data = self.data.drop(columns="Population")
            self.columns_non_time.remove("Population")

    def convert_to_date_datatype(self):
        self.set_date_format()
        self.data = self.data.reset_index()
        self.data = self.data.rename(columns={"index": "Time"})
        self.data["Time"] = pd.to_datetime(self.data["Time"], format=self.date_format)
        self.data = self.data.sort_values("Time")
        self.data = self.data.set_index("Time", drop=True)

    def set_date_format(self):
        match len(self.columns_time[0]):
            case 2: self.date_format = "%m"
            case 4: self.date_format = "%Y"
            case 7: self.date_format = "%Y %m"

    def create_figure(self):
        self.setup_figure()
        self.create_plot()

    def create_plot(self):
        self.set_plotting_function()
        self.set_labels()
        self.plot_values()
        self.plot_peripherals()
        self.output_figure()

    def setup_figure(self):
        plt.close('all')
        self.fig, self.ax = plt.subplots(1)

    def set_plotting_function(self):
        if self.log:
            self.plot_function = self.ax.semilogy
        else:
            self.plot_function = self.ax.plot

    def set_labels(self):
        self.set_labels_crime()
        self.set_labels_borough()
        self.set_labels_lsoa()
        self.set_labels_rank()
        self.combine_labels()

    def set_labels_crime(self):
        if "Minor Category" in self.data.columns.names:
            self.labels_crime = self.data.columns.to_frame()["Minor Category"].values
        elif "Major Category" in self.data.columns.names:
            self.labels_crime = self.data.columns.to_frame()["Major Category"].values
        else:
            self.labels_crime = None

    def set_labels_borough(self):
        self.labels_borough = [""] * len(self.data.columns.values)
        if "Borough" in self.data.columns.names:
            self.labels_borough = self.data.columns.to_frame()["Borough"].values

    def set_labels_lsoa(self):
        self.labels_lsoa = [""] * len(self.data.columns.values)
        if "LSOA" in self.data.columns.names:
            self.labels_lsoa = self.data.columns.to_frame()["LSOA"].values

    def set_labels_rank(self):
        self.labels_rank = np.arange(len(self.data.columns)) + 1

    def combine_labels(self):
        formatting_string = self.label_format.replace("{", "{")
        self.labels = [eval(formatting_string) for crime, borough, lsoa, rank in
                       zip(self.labels_crime, self.labels_borough,
                           self.labels_lsoa, self.labels_rank)]

    def plot_values(self):
        self.plot_function(self.data, label=self.labels)
        
    def plot_peripherals(self):
        self.set_axis_labels()
        self.set_ticks()
        self.set_title()
        self.add_legend()

    def set_axis_labels(self):
        self.ax.set_xlabel("Date", fontsize=self.fontsize_labels)
        self.ax.set_ylabel(self.y_label, fontsize=self.fontsize_labels)

    def set_ticks(self):
        self.ax.xaxis.set_tick_params(labelsize=self.fontsize_ticks)
        self.ax.yaxis.set_tick_params(labelsize=self.fontsize_ticks)

    def set_title(self):
        self.ax.set_title(self.title, fontsize=self.fontsize_title)

    def add_legend(self):
        self.set_legend()
        if self.legend:
            self.do_add_legend()

    # User specifies legend=True if they want
    # the legend applied when appropriate
    def set_legend(self):
        if self.labels is None and self.legend:
            self.legend = False

    def do_add_legend(self):
        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0 + box.height * self.squish_vertical,
                              box.width, box.height * (1-self.squish_vertical)])
        self.ax.legend(ncols=self.ncol, loc=self.loc, fontsize=self.fontsize_legend,
                       bbox_to_anchor=self.bbox_to_anchor)

    def output_figure(self):
        match self.output:
            case "Save": self.save_figure()
            case "Show": plt.show()
            case _: pass

    def save_figure(self):
        self.set_path_output()
        plt.savefig(self.path_output, format=self.format, bbox_inches="tight")

    def set_path_output(self):
        if not hasattr(self, "path_output"):
            self.path_output = path_output_base
        self.path_output = os.path.join(
            self.path_output, f"{self.name}.{self.format}")


defaults.load(Time)
