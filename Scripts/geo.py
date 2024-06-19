"""
This script is used for creating geographic plots.

Data can be aggregated over the following:
- City, borough, or LSOA region
- Total, major category, or minor category
- Total, year, or month
"""


import os

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from hgutilities import defaults
from hgutilities.utils import print_dict_aligned

from plot import Plot


class Geo():

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.read_data()

    def read_data(self):
        self.set_paths()
        self.crime = pd.read_csv(self.path_crime)

    def set_paths(self):
        self.path_cwd = os.getcwd()
        self.path_base = os.path.dirname(self.path_cwd)
        self.path_output_base = os.path.join(self.path_base, "Output")
        self.path_data = os.path.join(self.path_base, "Data")
        self.path_crime = os.path.join(self.path_data, "Crime.csv")
        
    def print_paths(self):
        paths_dict = {
            "Current working directory": self.path_cwd,
            "Base directory": self.path_base,
            "Data directory": self.path_data,
            "Geographic data directory": self.path_geography,
            "Crime data directory": self.path_crime,
            "Base output directory": self.path_output_base}
        print_dict_aligned(paths_dict)

    def process(self):
        self.aggregate()
        self.filter()

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
        months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
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
        agg_functions = {
            "LSOA": "first", "Borough": "first", "Minor Category": "first"}
        group_columns = ["Major Category"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_crime_total(self):
        agg_functions = {"Major Category": "first", "Minor Category": "first"}
        group_columns = ["LSOA", "Borough"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_and_group(self, agg_functions, group_columns):
        agg_functions.update(self.get_aggregation_functions_time())
        group_by_functions = self.get_groupby_functions(group_columns)
        self.crime = self.crime.groupby(group_by_functions)
        self.crime = self.crime.aggregate(agg_functions).reset_index()
        columns_to_drop = [column for column in agg_functions
                           if agg_functions[column] == "first"]
        self.crime = self.crime.drop(columns_to_drop, axis=1)

    def get_aggregation_functions_time(self):
        months = self.get_time_columns(self.crime)
        agg_functions_time = {month: "sum" for month in months}
        return agg_functions_time

    def get_groupby_functions(self, group_columns):
        all_columns = set(self.crime.columns.values)
        group_columns = list(set(group_columns).intersection(all_columns))
        return group_columns

    def filter(self):
        self.filter_borough()
        self.filter_lsoa()

    def filter_borough(self):
        if self.borough is not None:
            self.crime = self.crime.loc[self.crime["Borough"] == self.borough]

    def filter_lsoa(self):
        if self.lsoa is not None:
            self.crime = self.crime.loc[self.crime["LSOA"] == self.lsoa]

    def plot(self, **kwargs):
        kwargs.update(self.kwargs)
        self.plot = Plot(self.crime, **kwargs)
        self.plot.plot()

defaults.load(Geo)

#geo = Geo(agg_time="Total", agg_spatial="Borough", agg_crime="Total", name="Total Crime in London")
#geo = Geo(agg_time="Total", agg_crime="Total", name="Total Crime in London\nby LSOA Region")
#geo = Geo(agg_time="Total", agg_crime="Total", borough="Croydon", name="Total Crime in Croydon")
#geo = Geo(agg_time="Total", agg_crime="Total", borough="Westminster", name="Total Crime in Westminster")
#geo = Geo(agg_time="Total", lsoa="E01035716", name="Total Crime around Regents Street")
geo = Geo(agg_time="Total", agg_crime="Total", name="Log Total Crime in London\nby LSOA Region")

geo.process()
geo.plot(save=True, log=True)
