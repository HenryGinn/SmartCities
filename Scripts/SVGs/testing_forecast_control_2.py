import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

from os.path import join
from os import listdir

from hgutilities.utils import json, make_folder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from utils import get_base_path


plt.rcParams.update({"font.family": "Century Gothic"})
purple = "#6c17b9"
blue = "#1db8f7"
grey = "#6d6d6d"

base_path = get_base_path(__file__)
data_path = join(
    base_path, "Output", "Results", "Data",
    "Case_2", "Control", "TimeSeries_validate.csv")

df = pd.read_csv(data_path)
df = df.rename(columns={"Unnamed: 0": "Date"})
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df = df.set_index("Date", drop=True)
df = df.loc[df["Purpose"].isin(["Train", "Validate", "Test"])]

fig = plt.figure(figsize=(5, 3.8))
ax = fig.add_axes([0.16, 0.14, 0.8, 0.67])

ax.plot(df["DataOriginal"], label="Original", color=purple)
ax.plot(df["ModelledOriginal"], label="Modelled", color=blue)

month = pd.DateOffset(months=1)
i1 = df.index[0]
i2 = df.loc[df["Purpose"] == "Test"].index[0] - month
i3 = df.index[-1]
I1 = i1 + (i2 - i1) / 2
I2 = i2 + (i3 - i2) / 2 + month*5

ax.set_ylim((0, 4500))
ax.plot([i2, i2], [230, 4280], color=grey, dashes=(3, 3))
ax.text(I1, 4000, "Training", ha="center", fontsize=14)
ax.text(I2, 4000, "Testing", ha="center", fontsize=14)

ax.set_xlabel("Date", fontsize=14, labelpad=5)
ax.set_ylabel("Crimes Per 100,000 People", fontsize=14, labelpad=10)
fig.suptitle("Forecasting Crime Count For\nCase 2 Using Control Model",
             fontsize=20, y=0.97)
ax.legend(fontsize=14, loc="center left",
          bbox_to_anchor=[0, 0.7])

ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
even_years = pd.date_range(start="2010", end="2025", freq="2YE")
ax.set_xticks(even_years)
ax.set_xticklabels(even_years.year, fontsize=12)
odd_years = pd.date_range(start="2011", end="2024", freq="2YE")
ax.set_xticks(odd_years, minor=True)
ax.tick_params(axis='x', which='minor')
ax.set_xlim(left=df.index[0]-month, right=df.index[-1]+month*9)

output_path = join(
    base_path, "Output", "Results", "Forecasting",
    "Forecast_Control_Case_2.svg")
plt.savefig(output_path, format="svg")
