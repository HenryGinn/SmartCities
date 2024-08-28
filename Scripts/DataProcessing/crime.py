"""
This script is used for creating geographic plots.

Data can be aggregated over the following:
- City, borough, or LSOA region
- Total, major category, or minor category
- Total, year, or month
"""


import os
import warnings
import textwrap

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from hgutilities import defaults
from hgutilities.utils import get_dict_string

from DataProcessing.plot import Plot
from DataProcessing.timeseries import Time
from utils import get_time_columns, get_base_path


class Crime():

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.set_paths()
        self.read_data()
        self.set_property_values()

    def read_data(self):
        self.crime = pd.read_csv(self.path_crime, index_col="index")

    def set_paths(self):
        self.path_base = get_base_path(self)
        self.path_output_base = os.path.join(self.path_base, "Output")
        self.path_data = os.path.join(self.path_base, "Data")
        self.path_crime = os.path.join(self.path_data, "Crime.csv")
        
    def process(self):
        self.set_property_values()
        self.filter()
        self.aggregate()
        self.population_weight_data()
        self.sort()

    def set_property_values(self):
        self.region = self.get_region()
        self.crime_type = self.get_crime_type()

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
        agg_functions = {"LSOA": "first", "Borough": "first", "Population": "sum"}
        group_columns = ["Major Category", "Minor Category"]
        self.aggregate_and_group(agg_functions, group_columns)
        agg_functions = {"Crime": "sum", "Population": "first"}
        group_columns = ["Borough"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_spatial_city(self):
        agg_functions = {"LSOA": "first",
                         "Borough": "first",
                         "Population": "sum"}
        group_columns = ["Major Category", "Minor Category"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_time(self):
        match self.agg_time:
            case "Month": self.aggregate_time_month()
            case "Year":  self.aggregate_time_year()
            case "Total": self.aggregate_time_total()

    def aggregate_time_month(self):
        original_time_columns = get_time_columns(self.crime)
        column_groups = self.get_column_groups_month(original_time_columns)
        for month, values in column_groups.items():
            self.crime[month] = self.crime[values].mean(axis=1)
        self.crime = self.crime.drop(original_time_columns, axis=1)

    def get_column_groups_month(self, columns):
        months = sorted(list(set(column[-2:] for column in columns)))
        column_groups = {month: [] for month in months}
        for column in columns:
            column_groups[column.split(" ")[1]].append(column)
        return column_groups

    def aggregate_time_year(self):
        original_time_columns = get_time_columns(self.crime)
        column_groups = self.get_column_groups_year(original_time_columns)
        for year, values in column_groups.items():
            self.crime[year] = self.crime[values].mean(axis=1)
        self.crime = self.crime.drop(original_time_columns, axis=1)

    def get_column_groups_year(self, columns):
        column_groups = {year: [] for year in sorted(
            list(set([column.split(" ")[0] for column in columns])))}
        for column in columns:
            column_groups[column.split(" ")[0]].append(column)
        return column_groups

    def aggregate_time_total(self):
        original_time_columns = get_time_columns(self.crime)
        self.crime["Crime"] = self.crime[original_time_columns].sum(axis=1)
        self.crime = self.crime.drop(original_time_columns, axis=1)

    def aggregate_crime(self):
        match self.agg_crime:
            case "Minor": pass
            case "Major": self.aggregate_crime_major()
            case "Total": self.aggregate_crime_total()

    def aggregate_crime_major(self):
        agg_functions = {"Minor Category": "first", "Population": "first"}
        group_columns = ["LSOA", "Borough", "Major Category"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_crime_total(self):
        agg_functions = {"Major Category": "first",
                         "Minor Category": "first",
                         "Population": "first"}
        group_columns = ["LSOA", "Borough"]
        self.aggregate_and_group(agg_functions, group_columns)

    def aggregate_and_group(self, agg_functions, group_columns):
        if "Population" in self.crime.columns.values:
            self.do_aggregate_and_group(agg_functions, group_columns)
        else:
            self.aggregating_weighted_data_warning()

    def do_aggregate_and_group(self, agg_functions, group_columns):
        agg_functions.update(self.get_aggregation_functions_time())
        group_by_columns = self.get_groupby_columns(group_columns)
        self.crime = self.crime.groupby(group_by_columns)
        self.crime = self.crime.aggregate(agg_functions).reset_index()
        columns_to_drop = [column for column in agg_functions
                           if agg_functions[column] == "first"
                           and column != "Population"]
        self.crime = self.crime.drop(columns_to_drop, axis=1)

    def aggregating_weighted_data_warning(self):
        warnings.warn("Population column missing, the data may have been"
                      "population weighted, and should not be aggregated",
                      UserWarning)

    def get_aggregation_functions_time(self):
        months = get_time_columns(self.crime)
        agg_functions_time = {month: "sum" for month in months}
        return agg_functions_time

    def agg_population(self, x):
        if len(x) > 1:
            return x.sum()
        else:
            return x.iloc[0]

    def get_groupby_columns(self, group_columns):
        all_columns = set(self.crime.columns.values)
        group_columns = list(set(group_columns).intersection(all_columns))
        return group_columns

    def filter(self):
        self.filter_property("borough", "Borough")
        self.filter_property("lsoa", "LSOA")
        self.filter_property("minor", "Minor Category")
        self.filter_property("major", "Major Category")

    def filter_property(self, attribute, property_name):
        if hasattr(self, attribute) and getattr(self, attribute) is not None:
            self.crime = self.crime.loc[
                self.crime[property_name] == getattr(self, attribute)]

    def population_weight_data(self):
        if self.population_weighted:
            self.per_n_people_int = int(str(self.per_n_people).replace(",", ""))
            self.weight_time_columns_by_population()
            self.remove_population_column()

    def remove_population_column(self):
        if not self.keep_population_column:
            self.crime = self.crime.drop(columns="Population")

    def weight_time_columns_by_population(self):
        time_columns = get_time_columns(self.crime)
        self.crime[time_columns] = (self.per_n_people_int
            * self.crime[time_columns].values / self.crime["Population"].values[:, None])

    def sort(self):
            self.crime = self.crime.sort_values(
                self.crime.columns[-1], ascending=False)

    def remove_major(self, category="Fraud and Forgery"):
        self.crime = self.crime.loc[self.crime["Major Category"] != category]

    def plot(self, **kwargs):
        print(kwargs)
        self.plot_obj = Plot(self, **kwargs)
        self.plot_obj.plot(**kwargs)

    def time(self, **kwargs):
        self.time_obj = Time(self.crime, **kwargs)

    def time_plot(self, **kwargs):
        self.time_obj.kwargs.update(kwargs)
        defaults.kwargs(self.time_obj, self.time_obj.kwargs)
        self.time_obj.create_figure()

    def __str__(self):
        attributes = ["agg_spatial", "agg_time", "agg_crime", "borough", "lsoa",
                      "major", "minor", "month", "year"]
        string_dict = {attribute: getattr(self, attribute)
                       for attribute in attributes}
        return get_dict_string(string_dict)

defaults.load(Crime)
