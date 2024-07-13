import os
from os.path import join

import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


path_cwd = os.getcwd()
path_base = os.path.dirname(path_cwd)
path_output_base = join(path_base, "Output")
path_data = join(path_base, "Data")
path_lsoa = join(path_data, "LSOA.csv")

lsoa = gpd.GeoDataFrame(pd.read_csv(path_lsoa))
lsoa = lsoa.set_geometry(loads(lsoa["geometry"].values))

path_scores = join(path_output_base, "Interesting", "Text", "Theft: Mean.csv")
scores = pd.read_csv(path_scores)
scores = scores.drop(columns=[
    "Standard Deviation", "Normalised Deviation",
    "Test", "Major Category", "Major Category"])

merged = pd.merge(lsoa, scores, how="right", on="LSOA")
merged = merged

fig, ax = plt.subplots(1)
p = merged.plot(ax=ax, column="Mean", cmap="viridis", legend=True, norm=LogNorm())
plt.show()

