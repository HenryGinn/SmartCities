"""
This script preprocesses the crime dataset
It should be run before the geography preprocesser

The following preprocessing steps are done:

- Rename LSOA identifier to LSOA
- Change the borough code to the name of the borough
- Orders the crime data chronologically
- Changes crime categories to title case
- Adds a column for the population of each LSOA region
- Handles discepency between LSOA regions for Brent

This dataframe is not merged with the geography dataframe.
The geography data is large, and merging the dataframes would mean
the polygon data for each LSOA would be repeated for every minor crime,
increasing the file size for geographical data by around a factor of 30.
The polygonal data is only needed for plotting however, and so this can
be added right before it is needed with the following line:

df_with_polygons = pd.merge(
    df_original, df_polygons.loc[df_original["LSOA"]], on="LSOA")
"""


import os

import pandas as pd

from utils import get_capitalised
from hgutilities.utils import get_dict_string


months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


class PreProcess():

    def __init__(self):
        self.set_paths()

    def set_paths(self):
        self.path_cwd = os.getcwd()
        self.path_base = os.path.dirname(self.path_cwd)
        self.set_paths_data()
        
    def set_paths_data(self):
        self.path_data = os.path.join(self.path_base, "Data")
        self.path_original_data = os.path.join(self.path_data, "Original")
        self.path_crime = os.path.join(self.path_data, "Crime.csv")

    def preprocess(self):
        self.read_crime()
        self.manipulate_crime()
        self.write_crime()

    def read_crime(self):
        crime_1 = self.get_crime("Historical")
        crime_2 = self.get_crime("most recent 24 months")
        crime_2 = crime_2.drop(columns=["Borough", "LSOA Name"])
        self.crime = pd.merge(crime_1, crime_2, on=[
            "LSOA Code", "Minor Category", "Major Category"])

    def get_crime(self, subtitle):
            crime = pd.read_csv(os.path.join(self.path_original_data,
                        f"MPS LSOA Level Crime ({subtitle}).csv"))
            return crime

    def write_crime(self):
        self.crime.to_csv(self.path_crime, index=False)

    def manipulate_crime(self):
        self.human_readable_borough()
        self.process_LSOA_columns()
        self.crime_categories_title_case()
        self.add_population_column()
        self.process_time_columns()

    def human_readable_borough(self):
        lsoa_names = list(self.crime["LSOA Name"])
        borough = [lsoa_name[:-5] for lsoa_name in lsoa_names]
        self.crime["Borough"] = borough

    def process_LSOA_columns(self):
        self.crime = self.crime.drop(columns="LSOA Name")
        self.crime = self.crime.rename(columns={"LSOA Code": "LSOA"})

    def crime_categories_title_case(self):
        self.crime["Minor Category"] = [
            get_capitalised(name) for name in self.crime["Minor Category"].values]
        self.crime["Major Category"] = [
            get_capitalised(name) for name in self.crime["Major Category"].values]

    def add_population_column(self):
        self.read_population_data()
        self.population = self.population[["LSOA 2021 Code", "Mid-2021 population"]]
        self.population = self.population.rename(
            columns={"LSOA 2021 Code": "LSOA", "Mid-2021 population": "Population"})
        self.crime = pd.merge(self.crime, self.population, on="LSOA").reset_index()

    def read_population_data(self):
        path = os.path.join(self.path_original_data, "sapelsoapopdensitytablefinal.xlsx")
        self.population = pd.read_excel(path, sheet_name="Mid-2021 LSOA 2021", header=3)

    def process_time_columns(self):
        self.sort_columns()
        self.rename_time_columns()

    def sort_columns(self):
        columns = list(self.crime.columns.values)
        columns = columns[:5] + [columns[-1]] + sorted(columns[5:-1])
        self.crime = self.crime[columns]

    def rename_time_columns(self):
        time_columns = list(self.crime.columns.values[6:])
        new_time_columns = [self.get_time_column(name) for name in time_columns]
        time_columns_dict = dict(zip(time_columns, new_time_columns))
        self.crime = self.crime.rename(columns=time_columns_dict)

    def get_time_column(self, name):
        year, month = int(name[:4]), months[int(name[4:])-1]
        new_name = f"{year} {month}"
        return new_name

preprocess = PreProcess()
preprocess.preprocess()
