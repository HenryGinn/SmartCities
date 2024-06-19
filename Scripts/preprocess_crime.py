"""
There are two preprocessing scripts, and this one focuses on crime.
This script should be run before the geography preprocesser

The following preprocessing steps are done:

- Rename LSOA identifier to LSOA
- Change the borough code to the name of the borough
- Orders the crime data chronologically
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
        self.remove_lsoa_name()
        self.rename_lsoa_column()
        self.sort_columns()

    def human_readable_borough(self):
        lsoa_names = list(self.crime["LSOA Name"])
        borough = [lsoa_name[:-5] for lsoa_name in lsoa_names]
        self.crime["Borough"] = borough

    def remove_lsoa_name(self):
        self.crime = self.crime.drop(columns="LSOA Name")

    def rename_lsoa_column(self):
        self.crime = self.crime.rename(columns={"LSOA Code": "LSOA"})

    def sort_columns(self):
        columns = list(self.crime.columns.values)
        columns = columns[:4] + sorted(columns[4:])
        self.crime = self.crime[columns]

preprocess = PreProcess()
preprocess.preprocess()
