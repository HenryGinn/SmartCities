"""
This script takes in a dataframe and plots it sensibly.

The form of the plot is determined from the dataframe by the presence or
lack of presence of certain features. For example, if the dataframe only
contains data about each borough then it will not draw in the LSOA regions.
"""


import os

from hgutilities import defaults
from hgutilities import utils
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.wkt import loads
from mpl_toolkits.axes_grid1 import make_axes_locatable
from hgutilities.utils import print_dict_aligned
from matplotlib.colors import LogNorm


plt.rcParams["font.family"] = "Times New Roman"

class Plot():

    def __init__(self, data, **kwargs):
        defaults.kwargs(self, kwargs)
        self.data = data
        self.columns = list(data.columns.values)
        self.determine_settings()

    def determine_settings(self):
        self.determine_spatial_scope()
        self.determine_plot_column()
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
    

    def determine_plot_column(self):
        if not hasattr(self, "plot_column"):
            self.set_plot_column()

    def set_plot_column(self):
        non_plot_columns = set([
            "LSOA", "Borough", "Minor Category", "Major Category"])
        self.plottable_columns = list(set(self.columns) - non_plot_columns)
        self.process_plottable_columns()

    def process_plottable_columns(self):
        plottable_column_count = len(self.plottable_columns)
        match plottable_column_count:
            case 1: self.plot_column = self.plottable_columns[0]
            case 0: self.non_extractable_plottable_column_empty()
            case _: self.non_extractable_plottable_column_multiple()

    def non_extractable_plottable_column_empty(self):
        raise Exception("No plottable columns could be found\n"
                        f"Columns: {', '.join(self.columns)}")

    def non_extractable_plottable_column_multiple(self):
        raise Exception("Multiple columns could potentially be plotted\n"
                        "Specify one with the plot_column kwarg or drop all other columns\n"
                        f"Plottable columns: {', '.join(self.plottable_columns)}")

    def print_spatial(self):
        if hasattr(self, "spatial_lower") and hasattr(self, "spatial_upper"):
            properties = {"Spatial lower": self.spatial_lower,
                          "Spatial upper": self.spatial_upper}
            utils.print_dict_aligned(properties)
    

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
    

    def plot(self):
        self.fig, self.ax = plt.subplots(1)
        self.set_colorbar_kwargs()
        self.plot_values()
        self.plot_peripheries()
        self.save_figure()
        
    def plot_peripheries(self):
        self.ax.set_axis_off()
        self.ax.set_title(self.name, fontsize=self.fontsize_title)
        self.fig.axes[1].tick_params(labelsize=self.fontsize_colorbar)

    def set_colorbar_kwargs(self):
        divider = make_axes_locatable(self.ax)
        self.cax = divider.append_axes("right", size="5%", pad=0.1)
        self.set_norm()
        self.colorbar_kwargs = {"cax": self.cax, "norm": self.norm}

    def set_norm(self):
        if self.log:
            self.norm=LogNorm()
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
        #self.city = gpd.GeoDataFrame(self.data.iloc[0], geometry=city["geometry"])
        self.city = pd.concat((city, self.data), join="inner", axis=1)
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

    def save_figure(self):
        if self.save:
            self.set_path_output()
            plt.savefig(self.path_output, format=self.format, bbox_inches="tight")
        else:
            plt.show()

    def set_path_output(self):
        if not hasattr(self, "path_output"):
            self.path_output = path_output_base
        self.path_output = os.path.join(
            self.path_output, f"{self.name}.{self.format}")

defaults.load(Plot)

path_cwd = os.getcwd()
path_base = os.path.dirname(path_cwd)
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














