"""
This is used to iterate through combinations of settings for geographic
figures, plot the data, and save it to files in an organised way.
The information is organised in a dictionary according to the following:

- Absolute: if false then plot crime per 100k people
- Region: either "City" or "Borough"
- Resolution: either "Borough" or "LSOA"
- Crime Type: either "Minor", "Major", or "Total"
- Time: either "Month", "Year", or "Total"
"""


import os
from math import ceil, floor

from hgutilities import defaults, utils
import numpy as np
import imageio

from crime import Crime
from animate import Animate
from utils import get_time_columns, get_base_path


class Plotter():

    def __init__(self):
        self.set_paths()

    def set_paths(self):
        self.path_base = get_base_path(self)
        self.path_output_base = os.path.join(self.path_base, "Output")

    def generate(self, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.crime = Crime(absolute=self.absolute)
        self.set_path_absolute()
        self.process_region()

    def set_path_absolute(self):
        if self.absolute:
            self.path_absolute = os.path.join(self.path_output_base, "Absolute")
        else:
            self.path_absolute = os.path.join(self.path_output_base,
                f"Per {self.per_n_people.replace(',000', 'k')}")

    def process_region(self):
        match self.region:
            case "City": self.process_region_city()
            case "Borough": self.process_region_boroughs()

    def process_region_city(self):
        self.path_region = os.path.join(
            self.path_absolute, "Whole City")
        self.process_resolution()

    def process_region_boroughs(self):
        boroughs = sorted(set(list(self.crime.crime["Borough"])))
        if self.boroughs is None:
            self.boroughs = boroughs
        for borough in self.boroughs:
            self.generate_borough(borough)

    def generate_borough(self, borough):
        self.path_region = os.path.join(
            self.path_absolute, "Boroughs", borough)
        self.crime.borough = borough
        self.process_resolution()

    def process_resolution(self):
        self.set_crime_resolution()
        self.set_path_resolution()
        self.process_crime()

    def set_crime_resolution(self):
        match self.resolution:
            case "Borough": self.crime.agg_spatial = "Borough"
            case "LSOA": self.crime.agg_spatial = "LSOA"

    def set_path_resolution(self):
        match self.region:
            case "City": self.path_resolution = (
                os.path.join(self.path_region, f"{self.resolution} Resolution"))
            case "Borough": self.path_resolution = self.path_region

    def process_crime(self):
        match self.crime_type:
            case "Minor": self.process_crime_minor()
            case "Major": self.process_crime_major()
            case "Total": self.process_crime_total()

    def process_crime_minor(self):
        categories = self.get_minor_categories()
        for category in categories:
            self.process_crime_minor_category(category)

    def get_minor_categories(self):
        categories = self.crime.crime[["Major Category", "Minor Category"]].values
        categories = sorted(list(set([tuple(pair) for pair in categories])))
        categories = [pair[1] for pair in categories]
        return categories

    def process_crime_minor_category(self, category):
        self.path_crime = os.path.join(
            self.path_resolution, "Crime Minor Categories", category)
        self.crime.minor = category
        self.process_time()

    def process_crime_major(self):
        if self.categories_major is None:
            self.categories_major = sorted(list(set(self.crime.crime["Major Category"].values)))
        for category in self.categories_major:
            self.process_crime_major_category(category)

    def process_crime_major_category(self, category):
        self.path_crime = os.path.join(
            self.path_resolution, f"Major Categories  {self.time}", category)
        self.crime.major = category
        self.crime.agg_crime = "Major"
        self.process_time()

    def process_crime_total(self):
        self.path_crime = os.path.join(self.path_resolution, "Crime Total")
        self.crime.agg_crime = "Total"
        self.process_time()

    def process_time(self):
        self.print_progress()
        self.populate_terminal_folder()
        self.crime.read_data()

    def print_progress(self):
        if self.progress:
            print(utils.get_dict_string({
                "Borough": self.crime.borough,
                "Crime": os.path.split(self.path_crime)[1]}))
            print("")

    def populate_terminal_folder(self):
        self.set_time_properties()
        self.crime.process()
        self.time_columns = get_time_columns(self.crime.crime)
        self.filter_time_interval()
        self.process_time_columns()

    def set_time_properties(self):
        match self.time:
            case "Full": self.set_time_properties_full()
            case "Month": self.set_time_properties_month()
            case "Year": self.set_time_properties_year()
            case "Total": self.set_time_properties_total()

    def set_time_properties_full(self):
        self.path_time = self.path_crime
        self.filter_time_needed = True

    def set_time_properties_month(self):
        self.crime.agg_time = "Month"
        self.path_time = self.path_crime
        self.filter_time_needed = False

    def set_time_properties_year(self):
        self.crime.agg_time = "Year"
        self.path_time = self.path_crime
        self.filter_time_needed = True

    def set_time_properties_total(self):
        self.crime.agg_time = "Total"
        self.path_time = self.path_resolution
        self.filter_time_needed = False

    def filter_time_interval(self):
        if self.filter_time_needed:
            self.set_valid_years()
            self.time_columns = sorted(
                [column for column in self.time_columns
                 if int(column[:4]) in self.valid_years])

    def set_valid_years(self):
        self.valid_years = list(range(
            2010 if self.start is None else self.start,
            2025 if self.end is None else self.end+1))

    def process_time_columns(self):
        if self.crime.agg_time == "Total":
            self.process_time_total()
        else:
            self.process_time_non_total()

    def process_time_total(self):
        utils.make_folder(self.path_time)
        self.path_output = self.path_time
        self.plot(year=None, month=None)
        self.crime.read_data()

    def process_time_non_total(self):
        self.path_output = self.path_time
        self.set_vmin_and_vmax()
        self.animate_or_not()

    def animate_or_not(self):
        if self.animate:
            self.create_animation()
        else:
            self.create_plots_time()

    def set_vmin_and_vmax(self):
        values = self.crime.crime[self.time_columns].values
        if values.size != 0:
            self.vmin = max(1, floor(values.min()))
            self.vmax = ceil(values.max())

    def create_plots_time(self):
        utils.make_folder(self.path_time)
        for time in self.time_columns:
            self.create_plot_time(time)

    def create_plot_time(self, time, **kwargs):
        self.set_time_attributes(time)
        self.plot(month=self.month, year=self.year,
                  vmin=self.vmin, vmax=self.vmax, **kwargs)

    def set_time_attributes(self, time):
        if self.crime.agg_time not in [None, "Total"]:
            setattr(self, self.crime.agg_time.lower(), time)
        else:
            self.year, self.month = time.split(" ")

    def plot(self, **additional_kwargs):
        self.crime.plot(path_output=self.path_output,
                        **self.kwargs, **additional_kwargs)

    def create_animation(self):
        self.animate_obj = Animate(self)
        if np.max(self.crime.crime[self.time_columns].values) != 0:
            self.animate_obj.create_animation()

defaults.load(Plotter)


















