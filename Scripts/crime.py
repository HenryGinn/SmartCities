"""
This script is used for creating geographic plots.

Data can be aggregated over the following:
- City, borough, or LSOA region
- Total, major category, or minor category
- Total, year, or month
"""


import os
import textwrap

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from hgutilities import defaults
from hgutilities.utils import get_dict_string

from plot import Plot

title_case_exceptions = [
    "and", "as", "but", "for", "if", "nor", "or", "so", "yet", "a", "an", "the",
    "as", "at", "by", "for", "in", "of", "off", "on", "per", "to", "up", "via"]

months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

class Crime():

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.set_paths()
        self.read_data()

    def read_data(self):
        self.crime = pd.read_csv(self.path_crime)

    def set_paths(self):
        self.path_cwd = os.getcwd()
        self.path_base = os.path.dirname(self.path_cwd)
        self.path_output_base = os.path.join(self.path_base, "Output")
        self.path_data = os.path.join(self.path_base, "Data")
        self.path_crime = os.path.join(self.path_data, "Crime.csv")
        
    def process(self):
        self.set_property_values()
        self.filter()
        self.aggregate()

    def set_property_values(self):
        self.region = self.get_region()
        self.crime_type = self.get_crime_type()
        self.set_time_month()
        self.set_time_year()

    def get_region(self):
        if self.lsoa is not None:
            return self.lsoa
        if self.borough is not None:
            return self.borough
        return "London"

    def get_crime_type(self):
        if self.minor is not None:
            return self.minor
        if self.major is not None:
            return self.major
        return "Total"

    def set_time_month(self):
        if self.month is not None:
            self.time_month = self.month
        else:
            self.time_month = "All"

    def set_time_year(self):
        if self.year is not None:
            self.time_year = self.year
        else:
            self.time_year = "All"

    def aggregate(self):
        self.aggregate_spatial()
        self.aggregate_time()
        self.aggregate_crime()

    def aggregate_spatial(self):
        match self.agg_spatial:
            case "LSOA":    pass
            case "Borough": self.aggregate_spatial_borough()
            case "City":    self.aggregate_spatial_city()

    def aggregate_spatial_borough(self):
        agg_functions = {"LSOA": "first"}
        group_columns = ["Borough", "Major Category", "Minor Category"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_spatial_city(self):
        agg_functions = {"LSOA": "first", "Borough": "first"}
        group_columns = ["Major Category", "Minor Category"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_time(self):
        match self.agg_time:
            case "Month": self.aggregate_time_month()
            case "Year":  self.aggregate_time_year()
            case "Total": self.aggregate_time_total()

    def aggregate_time_month(self):
        original_time_columns = self.get_time_columns(self.crime)
        column_groups = self.get_column_groups_month(original_time_columns)
        for month, values in column_groups.items():
            self.crime[month] = self.crime[values].sum(axis=1)
        self.crime = self.crime.drop(original_time_columns, axis=1)

    def get_time_columns(self, dataframe):
        columns = set(dataframe.columns.values)
        non_time_columns = set([
            "LSOA", "Borough", "Minor Category", "Major Category"])
        time_columns = sorted(list(columns - non_time_columns))
        return time_columns

    def get_column_groups_month(self, columns):
        column_groups = {month: [] for month in months}
        for column in columns:
            column_groups[months[int(column[-2:])-1]].append(column)
        return column_groups

    def aggregate_time_year(self):
        original_time_columns = self.get_time_columns(self.crime)
        column_groups = self.get_column_groups_year(original_time_columns)
        for year, values in column_groups.items():
            self.crime[year] = self.crime[values].sum(axis=1)
        self.crime = self.crime.drop(original_time_columns, axis=1)

    def get_column_groups_year(self, columns):
        column_groups = {year: [] for year in sorted(
            list(set([int(column[:4]) for column in columns])))}
        for column in columns:
            column_group[int(column[:4])].append(column)
        return column_groups

    def aggregate_time_total(self):
        original_time_columns = self.get_time_columns(self.crime)
        self.crime["Crime"] = self.crime[original_time_columns].sum(axis=1)
        self.crime = self.crime.drop(original_time_columns, axis=1)

    def aggregate_crime(self):
        match self.agg_crime:
            case "Minor": pass
            case "Major": self.aggregate_crime_major()
            case "Total": self.aggregate_crime_total()

    def aggregate_crime_major(self):
        agg_functions = {"Minor Category": "first"}
        group_columns = ["LSOA", "Borough", "Major Category"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_crime_total(self):
        agg_functions = {"Major Category": "first", "Minor Category": "first"}
        group_columns = ["LSOA", "Borough"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_and_group(self, agg_functions, group_columns):
        agg_functions.update(self.get_aggregation_functions_time())
        group_by_columns = self.get_groupby_columns(group_columns)
        self.crime = self.crime.groupby(group_by_columns)
        self.crime = self.crime.aggregate(agg_functions).reset_index()
        columns_to_drop = [column for column in agg_functions
                           if agg_functions[column] == "first"]
        self.crime = self.crime.drop(columns_to_drop, axis=1)

    def get_aggregation_functions_time(self):
        months = self.get_time_columns(self.crime)
        agg_functions_time = {month: "sum" for month in months}
        return agg_functions_time

    def get_groupby_columns(self, group_columns):
        all_columns = set(self.crime.columns.values)
        group_columns = list(set(group_columns).intersection(all_columns))
        return group_columns

    def filter(self):
        self.filter_property("borough", "Borough")
        self.filter_property("lsoa", "LSOA")
        self.filter_property("minor", "Minor Category")
        self.filter_property("major", "Major Category")
        self.filter_property("month", "Month")
        self.filter_property("year", "Year")

    def filter_property(self, attribute, property_name):
        if hasattr(self, attribute) and getattr(self, attribute) is not None:
            self.crime = self.crime.loc[self.crime[property_name] ==
                                        getattr(self, attribute)]

    def set_time_attributes(self, time):
        if self.agg_time not in [None, "Total"]:
            setattr(self, self.agg_time.lower(), time)
        else:
            self.month, self.year = months[int(time[4:])], int(time[:4])
        

    def generate_title(self):
        self.title = (f"{self.get_title_crime()} in "
                      f"{self.get_title_location()} "
                      f"{self.get_title_time()}")
        self.title_flat = self.get_capitalised(self.title)
        self.title = self.add_line_breaks(self.title_flat)
        print(self.title_flat)

    def get_title_crime(self):
        match self.agg_crime:
            case "Minor": return self.minor
            case "Major": return self.major
            case "Total": return "Total Crime"

    def get_title_location(self):
        if self.borough is not None:
            return self.borough
        else:
            return "London"

    def get_title_time(self):
        match self.agg_time:
            case "Month": return f"in {self.month}"
            case "Year": return f"in {self.year}"
            case "Total": return "Since 2010"
            case _: return f"in {self.month} {self.year}"

    # https://stackoverflow.com/questions/3728655/titlecasing-a-string-with-exceptions?rq=3
    def get_capitalised(self, string):
        word_list = string.lower().split(' ')
        capitalised = [word_list[0].capitalize()]
        for word in word_list[1:]:
            capitalised.append(word if word in title_case_exceptions else word.capitalize())
        capitalised = " ".join(capitalised)
        return capitalised

    def add_line_breaks(self, string):
        if len(string) > 25:
            splits = self.get_splits(string)
            differences = {abs(len(split[0]) - len(split[1])): split for split in splits}
            minimum_difference = min(list(differences.keys()))
            string = "\n".join(differences[minimum_difference])
        return string

    def get_splits(self, string):
        words = string.split(" ")
        splits = [[" ".join(word for word in words[:word_limit]),
                   " ".join(word for word in words[word_limit:])]
                  for word_limit in range(len(words))]
        return splits

    def plot(self, **kwargs):
        kwargs.update({**self.kwargs, "title": self.title})
        self.plot_obj = Plot(self, **kwargs)
        self.plot_obj.plot()

    def __str__(self):
        attributes = ["agg_spatial", "agg_time", "agg_crime", "borough",
                      "lsoa", "major", "minor", "month", "year"]
        string_dict = {attribute: getattr(self, attribute)
                       for attribute in attributes}
        return get_dict_string(string_dict)

defaults.load(Crime)
