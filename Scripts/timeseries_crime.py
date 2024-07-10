import os

import matplotlib.pyplot as plt
import pandas as pd
from hgutilities import defaults
from hgutilities import utils
from hgutilities.utils import get_dict_string

from utils import get_time_columns
from utils import get_capitalised
from utils import add_line_breaks


plt.rcParams["font.family"] = "Times New Roman"


class TimeCrime():

    def __init__(self, crime, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.crime = crime
        self.data = crime.crime.copy()

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
        if self.population_weighted:
            per_n_people_int = int(str(self.per_n_people).replace(",", ""))
            self.data[self.columns_time] = (per_n_people_int * 
                self.data[self.columns_time].T / self.data["Population"].values).T
        self.data = self.data.drop(columns="Population")
        self.columns_non_time.remove("Population")

    def convert_to_date_datatype(self):
        self.data = self.data.reset_index()
        self.data = self.data.rename(columns={"index": "Time"})
        self.data["Time"] = pd.to_datetime(self.data["Time"], format="%Y %B")
        self.data = self.data.sort_values("Time")
        self.data = self.data.set_index("Time", drop=True)

    def create_figure(self):
        self.setup_figure()
        self.plot_values()
        self.plot_peripheries()
        self.output_figure()

    def setup_figure(self):
        plt.close('all')
        self.fig, self.ax = plt.subplots(1)
        self.set_plotting_function()

    def set_plotting_function(self):
        if self.log:
            self.plot_function = self.ax.semilogy
        else:
            self.plot_function = self.ax.plot

    def plot_values(self):
        self.set_labels()
        self.plot_function(self.data, label=self.labels)

    def set_labels(self):
        if "Minor Category" in self.data.columns.names:
            self.labels = self.data.columns.to_frame()["Minor Category"].values
        elif "Major Category" in self.data.columns.names:
            self.labels = self.data.columns.to_frame()["Major Category"].values
        else:
            self.labels = None
        
    def plot_peripheries(self):
        self.set_y_label()
        self.ax.set_xlabel("Time", fontsize=self.fontsize_axis_labels)
        self.ax.set_ylabel(self.y_label, fontsize=self.fontsize_axis_labels)
        self.set_title()
        self.add_legend()

    def set_y_label(self):
        if self.population_weighted:
            self.y_label_weighted_population = self.get_y_label_weighted_population()
        else:
            self.y_label_weighted_population = ""
        self.y_label = f"Reported Crimes{self.y_label_weighted_population}"

    def get_y_label_weighted_population(self):
        if str(self.per_n_people) == "1":
            return " per Person"
        else:
            return f" per {self.per_n_people} People"

    def set_title(self):
        if self.title is None:
            self.generate_title()
        self.ax.set_title(self.title, fontsize=self.fontsize_title,
                          pad=self.title_pad)

    def generate_title(self):
        self.set_title_base()
        self.title_flat = get_capitalised(self.title)
        self.title = add_line_breaks(self.title_flat, length=50)

    def set_title_base(self):
        self.title = (f"{self.get_title_time()} "
                      f"{self.get_title_crime()}"
                      f"{self.get_title_rate()} in "
                      f"{self.get_title_location()}")

    def get_title_crime(self):
        match self.crime.agg_crime:
            case "Minor": return self.crime.minor
            case "Major": return self.get_title_crime_major()
            case "Total": return "Total Crime"

    def get_title_crime_major(self):
        if isinstance(self.crime.major, str):
            return self.crime.major
        else:
            return "Crime"

    def get_title_rate(self):
        if self.population_weighted:
            return " Rate"
        else:
            return ""

    def get_title_location(self):
        if self.crime.borough is not None:
            return self.crime.borough
        else:
            return "London"

    def get_title_time(self):
        if self.crime.agg_time == "Month":
            return "Seasonal "
        else:
            return ""

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
        self.ax.legend(ncols=self.ncol, loc=self.loc,
                       bbox_to_anchor=self.bbox_to_anchor)

    def output_figure(self):
        if self.save:
            self.save_figure()
        else:
            plt.show()

    def save_figure(self):
        self.set_name()
        self.set_path_output()
        plt.savefig(self.path_output, format=self.format, bbox_inches="tight")

    def set_name(self):
        if self.crime.name is None:
            self.do_set_name()
        else:
            self.name = self.crime.name

    def do_set_name(self):
        self.name = utils.get_file_name({
            "Region": self.crime.region, "Crime": self.crime.crime_type,
            "Year": self.crime.time_year, "Month": self.crime.time_month,
            "Resolution": self.crime.agg_spatial, "Log": self.log})

    def set_path_output(self):
        if not hasattr(self, "path_output"):
            self.path_output = path_output_base
        self.path_output = os.path.join(
            self.path_output, f"{self.name}.{self.format}")


defaults.load(TimeSeries)
