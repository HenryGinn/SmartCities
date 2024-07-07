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

from hgutilities import defaults
from hgutilities import utils
import imageio

from crime import Crime
from plot import Plot
from utils import get_time_columns


class Plotter():

    def __init__(self):
        self.set_paths()

    def set_paths(self):
        self.path_cwd = os.getcwd()
        self.path_base = os.path.dirname(self.path_cwd)
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
            self.path_absolute = os.path.join(self.path_output_base, "Per 100k")

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
            self.path_resolution, "Crime: Minor Categories", category)
        self.crime.minor = category
        self.process_time()

    def process_crime_major(self):
        if self.categories_major is None:
            self.categories_major = sorted(list(set(self.crime.crime["Major Category"].values)))
        for category in self.categories_major:
            self.process_crime_major_category(category)

    def process_crime_major_category(self, category):
        self.path_crime = os.path.join(
            self.path_resolution, "Crime: Major Categories", category)
        self.crime.major = category
        self.crime.agg_crime = "Major"
        self.process_time()

    def process_crime_total(self):
        self.path_crime = os.path.join(self.path_resolution, "Crime: Total")
        self.crime_agg = "Total"
        self.process_time()

    def process_time(self):
        self.set_time_properties()
        utils.make_folder(self.path_time)
        self.time_columns = get_time_columns(self.crime.crime)
        self.process_time_columns()

    def set_time_properties(self):
        match self.time:
            case "Full": self.set_time_properties_full()
            case "Month": self.set_time_properties_month()
            case "Year": self.set_time_properties_year()
            case "Total": self.set_time_properties_total()

    def set_time_properties_full(self):
        self.path_time = os.path.join(self.path_crime, "All")

    def set_time_properties_month(self):
        self.crime.agg_time = "Month"
        self.path_time = os.path.join(self.path_crime, "Months")

    def set_time_properties_year(self):
        self.crime.agg_time = "Year"
        self.path_time = os.path.join(self.path_crime, "Years")

    def set_time_properties_total(self):
        self.crime.agg_time = "Total"
        self.path_time = self.path_resolution

    def process_time_columns(self):
        if self.crime.agg_time == "Total":
            self.process_time_total()
        else:
            self.process_time_non_total()

    def process_time_total(self):
        self.path_output = self.path_time
        self.plot()
        self.crime.read_data()

    def process_time_non_total(self):
        self.filenames = []
        self.create_plots_time()
        if self.animate:
            self.create_animation()

    def create_plots_time(self):
        for time in self.time_columns:
            self.crime.read_data()
            self.crime.set_time_attributes(time)
            self.path_output = self.path_time
            self.plot(plotting_column=time)
            self.filenames.append(self.path_time)

    def plot(self, **additional_kwargs):
        self.crime.process()
        self.crime.plot(path_output=self.path_output, **self.kwargs, **additional_kwargs)

defaults.load(Plotter)


















