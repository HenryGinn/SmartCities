"""
There are two preprocessing scripts, and this one focuses on crime.
This script should be run after the crime preprocesser.

The following preprocessing steps are done:

- Omit geometry data on non-London areas
- Rename LSOA code columns to LSOA
- Get rid of all columns other than LSOA and geometry
- Handles discepency between LSOA regions for Brent

This dataframe is not merged with the geography dataframe.
The geography data is large, and merging the dataframes would mean
the polygon data for each LSOA would be repeated for every minor crime,
increasing the file size for geographical data by around a factor of 30.
The polygonal data is only needed for plotting however, and so this can
be added right before it is needed with the following line:

df_with_polygons = pd.merge(
    df_original, df_geography.loc[df_original["LSOA"]], on="LSOA")
"""


import os

import pandas as pd
import geopandas as gpd
from shapely.ops import unary_union


class PreProcess():

    def __init__(self):
        self.set_paths()

    def set_paths(self):
        self.path_cwd = os.getcwd()
        self.path_base = os.path.dirname(self.path_cwd)
        self.set_paths_data()
        
    def set_paths_data(self):
        self.path_data = os.path.join(self.path_base, "Data")
        self.path_crime = os.path.join(self.path_data, "Crime.csv")
        self.path_source = os.path.join(self.path_data, "Original",
                                        "LSOA_2021_EW_BGC_V3.shp")
        self.set_paths_geography()

    def set_paths_geography(self):
        self.path_city = os.path.join(self.path_data, "City.csv")
        self.path_borough = os.path.join(self.path_data, "Borough.csv")
        self.path_lsoa = os.path.join(self.path_data, "LSOA.csv")

    def preprocess(self):
        self.read_geography()
        self.manipulate_geography()
        self.write_geography()

    def read_geography(self):
        self.lsoa = gpd.read_file(self.path_source)

    def write_geography(self):
        self.lsoa.to_csv(self.path_lsoa, index=False)
        self.borough.to_csv(self.path_borough, index=False)
        self.city.to_csv(self.path_city, index=False)

    def manipulate_geography(self):
        self.rename_lsoa_column()
        self.remove_non_london_areas()
        self.add_borough_column()
        self.remove_unnecessary_columns()
        self.group_by_regions()

    def rename_lsoa_column(self):
        self.lsoa = self.lsoa.rename(columns={"LSOA21CD": "LSOA"})

    def remove_non_london_areas(self):
        self.set_lsoa_IDs()
        london_rows = self.lsoa["LSOA"].isin(self.lsoa_IDs)
        self.lsoa = self.lsoa[london_rows]

    def set_lsoa_IDs(self):
        crime = pd.read_csv(self.path_crime)
        self.lsoa_IDs = list(crime["LSOA"])

    def add_borough_column(self):
        borough = list(self.lsoa["LSOA21NM"])
        borough = [name[:-5] for name in borough]
        self.lsoa["Borough"] = borough

    def remove_unnecessary_columns(self):
        columns = ["LSOA", "Borough", "geometry"]
        self.lsoa = self.lsoa[columns]

    def group_by_regions(self):
        self.create_borough()
        self.create_city()

    def create_borough(self):
        agg_functions = {"LSOA": "first",
                         "geometry": self.merge_polygons}
        self.borough = self.lsoa.groupby("Borough").aggregate(agg_functions)
        self.borough = self.borough.drop(columns="LSOA").reset_index()

    def create_city(self):
        polygons = list(self.lsoa["geometry"])
        polygon = self.merge_polygons(polygons)
        self.city = pd.DataFrame({"geometry": polygon})

    def merge_polygons(self, polygons):
        merged_polygon = gpd.GeoSeries(unary_union(polygons))
        return merged_polygon


preprocess = PreProcess()
preprocess.preprocess()


















