"""
This script takes in a dataframe and plots it sensibly.

The form of the plot is determined from the dataframe by the presence or
lack of presence of certain features. For example, if the dataframe only
contains data about each borough then it will not draw in the LSOA regions.
"""


import os
from copy import deepcopy

from hgutilities import defaults, utils
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.wkt import loads
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm

from utils import (get_capitalised, add_line_breaks,
                   get_time_columns, get_base_path)


plt.rcParams["font.family"] = "Times New Roman"

class Plot():

    def __init__(self, crime, **kwargs):
        defaults.kwargs(self, kwargs)
        self.crime = crime
        self.data = self.crime.crime
        self.columns = list(self.data.columns.values)
        self.determine_settings()

    def determine_settings(self):
        self.determine_spatial_scope()
        self.determine_edge_data()
        self.determine_spatial_plot_types()

    def determine_spatial_scope(self):
        self.spatial_upper = "City"
        self.set_spatial_lower()
        self.set_spatial_upper()

    def set_spatial_lower(self):
        if "LSOA" in self.columns:
            self.spatial_lower = "LSOA"
        elif "Borough" in self.columns:
            self.spatial_lower = "Borough"
        else:
            self.spatial_lower = "City"

    def set_spatial_upper(self):
        self.determine_spatial_upper_borough()
        if self.spatial_upper == "Borough":
            self.determine_spatial_upper_lsoa()

    def determine_spatial_upper_borough(self):
        if "Borough" in self.columns:
            boroughs = list(set(self.data["Borough"]))
            if len(boroughs) == 1:
                self.spatial_upper = "Borough"

    def determine_spatial_upper_lsoa(self):
        if "LSOA" in self.columns:
            lsoas = list(set(self.data["LSOA"]))
            if len(lsoas) == 1:
                self.spatial_upper = "LSOA"
    

    # The upper values for the edge properties are used
    # for the most significant structure being plotted
    def determine_edge_data(self):
        match self.spatial_upper:
            case "City": self.set_edge_data_city()
            case "Borough": self.set_edge_data_borough()
            case "LSOA": self.edge_data_lsoa()
            case _: self.invalid_spatial_scope()

    def set_edge_data_city(self):
        self.edge_kwargs_city = {"edgecolor": self.edgecolor_upper,
                                 "linewidth": self.linewidth_upper}
        self.edge_kwargs_borough = {"edgecolor": self.edgecolor_middle,
                                    "linewidth": self.linewidth_middle}
        self.edge_kwargs_lsoa = {"edgecolor": self.edgecolor_lower,
                                 "linewidth": self.linewidth_lower}

    def set_edge_data_borough(self):
        self.edge_kwargs_borough = {"edgecolor": self.edgecolor_upper,
                                    "linewidth": self.linewidth_upper}
        self.edge_kwargs_lsoa = {"edgecolor": self.edgecolor_lower,
                                 "linewidth": self.linewidth_lower}

    def edge_data_lsoa(self):
        self.edge_kwargs_lsoa = {"edgecolor": self.edgecolor_upper,
                                 "linewidth": self.linewidth_upper}

    def invalid_spatial_scope(self):
        raise Exception(
            "The spatial scope is not set properly\n"
            "Whether to plot the city, boroughs, or LSOAs is unclear")

    def determine_spatial_plot_types(self):
        (self.city_plot_type, self.borough_plot_type, self.lsoa_plot_type) = {
            ("City",    "City"):    ("Values",  "Blank",   "Blank"),
            ("Borough", "City"): ("Outline", "Values",  "Blank"),
            ("LSOA",    "City"):    ("Outline", "Outline", "Values"),
            ("Borough", "Borough"): ("Blank",   "Values",  "Blank"),
            ("LSOA",    "Borough"):    ("Blank",   "Outline", "Values"),
            ("LSOA",    "LSOA"):    ("Blank",   "Blank",   "Values")
            }[(self.spatial_lower, self.spatial_upper)]


    def set_plot_column(self):
        if self.plot_column is None:
            self.do_set_plot_column()

    def do_set_plot_column(self):
        non_plot_columns = set([
            "LSOA", "Borough", "Minor Category", "Major Category"])
        self.plottable_columns = list(set(self.columns) - non_plot_columns)
        self.filter_plottable_columns_by_time()
        self.process_plottable_columns()

    def filter_plottable_columns_by_time(self):
        self.filter_plottable_columns_by_time_month()
        self.filter_plottable_columns_by_time_year()

    def filter_plottable_columns_by_time_month(self):
        if hasattr(self, "month") and self.month is not None:
            self.plottable_columns = sorted(
                [column for column in self.plottable_columns
                 if str(self.month) in column[-2:]])

    def filter_plottable_columns_by_time_year(self):
        if hasattr(self, "year") and self.year is not None:
            self.plottable_columns = sorted(
                [column for column in self.plottable_columns
                 if str(self.year) in column[:4]])

    def process_plottable_columns(self):
        plottable_column_count = len(self.plottable_columns)
        match plottable_column_count:
            case 1: self.set_unique_plot_column()
            case 0: self.non_extractable_plottable_column_empty()
            case _: self.non_extractable_plottable_column_multiple()

    def set_unique_plot_column(self):
        self.plot_column = self.plottable_columns[0]
        self.population_weighted = False

    def non_extractable_plottable_column_empty(self):
        raise Exception("No plottable columns could be found\n"
                        f"Columns: {', '.join(self.columns)}")

    def non_extractable_plottable_column_multiple(self):
        raise Exception("Multiple columns could potentially be plotted\n"
                        "Specify one with the plot_column kwarg or month and year kwargs\n"
                        f"Plottable columns: {', '.join(self.plottable_columns)}")

    def print_spatial(self):
        if hasattr(self, "spatial_lower") and hasattr(self, "spatial_upper"):
            properties = {"Spatial lower": self.spatial_lower,
                          "Spatial upper": self.spatial_upper}
            print(utils.get_dict_string(properties))
    

    def plot(self, **kwargs):
        self.preplot_checks_and_settings(**kwargs)
        self.setup_figure()
        self.plot_values()
        self.plot_peripheries()
        self.output_figure()

    def preplot_checks_and_settings(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_plot_column()
        self.check_crime_category("Major")
        self.check_crime_category("Minor")

    def check_crime_category(self, crime_type):
        if f"{crime_type} Category" in self.data.columns.values:
            crime_types = set(self.data[f"{crime_type} Category"].values)
            if len(crime_types) > 1:
                raise self.crime_category_not_defined(crime_types)

    def crime_category_not_defined(self, crime_types):
        raise ValueError("Crime category is not defined.\n"
                         "Either aggregate or filter to a unique crime\n"
                         f"Categories: {', '.join(crime_types)}")

    def setup_figure(self):
        plt.close('all')
        self.fig, self.ax = plt.subplots(1, figsize=self.figsize)
        self.set_colorbar_kwargs()
        
    def plot_peripheries(self):
        self.ax.set_axis_off()
        self.adjust_colorbar()
        self.set_title()

    def adjust_colorbar(self):
        cbar_fig = self.fig.axes[1]
        cbar_fig.tick_params(labelsize=self.fontsize_colorbar_ticks)
        cbar_fig.set_ylabel(cbar_fig.get_ylabel(),
                            fontsize=self.fontsize_colorbar_label,
                            labelpad=self.colorbar_label_pad)

    def set_title(self):
        self.generate_title()
        self.ax.set_title(self.title, fontsize=self.fontsize_title)

    def generate_title(self):
        if self.title is None and self.no_title is False:
            self.do_generate_title()

    def do_generate_title(self):
        self.set_title_base()
        self.title_flat = get_capitalised(self.title)
        self.title = add_line_breaks(self.title_flat, length=35)

    def set_title_base(self):
        self.title = (f"{self.get_title_crime()} in "
                      f"{self.get_title_location()} "
                      f"{self.get_title_time()}")

    def get_title_crime(self):
        match self.crime.agg_crime:
            case "Minor": return self.crime.minor
            case "Major": return self.crime.major
            case "Total": return "Total Crime"

    def get_title_location(self):
        if self.crime.borough is not None:
            return self.crime.borough
        else:
            return "London"

    def get_title_time(self):
        match self.crime.agg_time:
            case "Month": return f"in {self.month}"
            case "Year": return f"in {self.year}"
            case "Total": return "Since 2010"
            case _: return self.get_title_time_full()

    def get_title_time_full(self):
        if self.animate:
            return f"in {self.year}"
        else:
            return f"in {self.month} {self.year}"

    def set_colorbar_kwargs(self):
        self.setup_colorbar()
        self.colorbar_kwargs = {
            "cax": self.cax, "cmap": self.cmap, "norm": self.norm,
            "vmin": self.vmin, "vmax": self.vmax,
            "legend_kwds": {"label": self.colorbar_label}}

    def setup_colorbar(self):
        divider = make_axes_locatable(self.ax)
        self.cax = divider.append_axes("right", size="5%", pad=0.1)
        self.set_norm()
        self.set_colorbar_label()

    def set_colorbar_label(self):
        if self.colorbar_label is None:
            if self.crime.population_weighted:
                self.set_colorbar_label_weighted()
            else:
                self.colorbar_label = "Reported Crimes"

    def set_colorbar_label_weighted(self):
        if str(self.crime.per_n_people) == "1":
            self.colorbar_label = "Reported Crimes Per Person"
        else:
            self.colorbar_label = f"Reported Crimes Per {self.crime.per_n_people} People"

    def set_norm(self):
        if self.log:
            self.norm=LogNorm(vmin=self.vmin, vmax=self.vmax)
        else:
            self.norm = None

    def plot_values(self):
        self.plot_lsoa()
        self.plot_borough()
        self.plot_city()

    def plot_city(self):
        match self.city_plot_type:
            case "Blank":   return
            case "Outline": self.setup_city_outline()
            case "Values":  self.setup_city_values()
        self.city = pd.concat((city, self.data.head(1)), axis=1)
        self.draw_city()

    def setup_city_outline(self):
        self.city_value_kwargs = {
            "color": "none",
            "legend": False}

    def setup_city_values(self):
        self.city_value_kwargs = {
            "column": self.plot_column,
            "legend": self.legend,}

    def draw_city(self):
        self.city_plot = self.city.plot(
            ax=self.ax, **self.city_value_kwargs,
            **self.edge_kwargs_city,
            **self.colorbar_kwargs)

    def plot_borough(self):
        match self.borough_plot_type:
            case "Blank":   return
            case "Outline": self.setup_borough_outline()
            case "Values":  self.setup_borough_values()
        self.borough = pd.merge(borough, self.data, how="right", on="Borough")
        self.draw_borough()

    def setup_borough_outline(self):
        self.borough_value_kwargs = {
            "color": "none",
            "legend": False}

    def setup_borough_values(self):
        self.borough_value_kwargs = {
            "column": self.plot_column,
            "legend": self.legend}

    def draw_borough(self):
        self.borough_plot = self.borough.plot(
            ax=self.ax, **self.borough_value_kwargs,
            **self.edge_kwargs_borough,
            **self.colorbar_kwargs)

    def plot_lsoa(self):
        match self.lsoa_plot_type:
            case "Blank":   return
            case "Outline": self.setup_lsoa_outline()
            case "Values":  self.setup_lsoa_values()
        self.lsoa = pd.merge(lsoa, self.data, how="right", on="LSOA")
        self.draw_lsoa()

    def setup_lsoa_outline(self):
        self.lsoa_value_kwargs = {
            "color": "none",
            "legend": False}

    def setup_lsoa_values(self):
        self.lsoa_value_kwargs = {
            "column": self.plot_column,
            "legend": self.legend}

    def draw_lsoa(self):
        self.lsoa_plot = self.lsoa.plot(
            ax=self.ax, **self.lsoa_value_kwargs,
            **self.edge_kwargs_lsoa,
            **self.colorbar_kwargs)

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
        self.figure_name = utils.get_file_name({
            "Region": self.crime.region, "Crime": self.crime.crime_type,
            "Year": self.year, "Month": self.month,
            "Resolution": self.crime.agg_spatial, "Log": self.log},
            timestamp=False)

    def save_figure(self):
        self.set_path_output()
        plt.savefig(self.path_output, format=self.format,
                    bbox_inches=self.bbox_inches)

    def set_path_output(self):
        if not hasattr(self, "path_output"):
            self.path_output = path_output_base
            print("Lol", self.path_output)
        self.path_output = os.path.join(
            self.path_output, f"{self.figure_name}.{self.format}")

defaults.load(Plot)

path_base = get_base_path(__file__)
path_output_base = os.path.join(path_base, "Output")
path_data = os.path.join(path_base, "Data")
path_city = os.path.join(path_data, "City.csv")
path_borough = os.path.join(path_data, "Borough.csv")
path_lsoa = os.path.join(path_data, "LSOA.csv")

city = gpd.GeoDataFrame(pd.read_csv(path_city))
borough = gpd.GeoDataFrame(pd.read_csv(path_borough))
lsoa = gpd.GeoDataFrame(pd.read_csv(path_lsoa))

city = city.set_geometry(loads(city["geometry"].values))
borough = borough.set_geometry(loads(borough["geometry"].values))
lsoa = lsoa.set_geometry(loads(lsoa["geometry"].values))
