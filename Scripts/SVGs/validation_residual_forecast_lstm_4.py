import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

from os.path import join
from os import listdir

from hgutilities.utils import json, make_folder
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils import get_base_path


plt.rcParams.update({"font.family": "Century Gothic"})
purple = "#6c17b9"
blue = "#1db8f7"
grey = "#6d6d6d"

base_path = get_base_path(__file__)
data_path = join(
    base_path, "Output", "LSTM", f"Case_4",
    "D0_32__L0_False__L1_False__L2_32__D1_False",
    "TimeSeries_train.csv")

df = pd.read_csv(data_path)
df = df.rename(columns={"Unnamed: 0": "Date"})
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df = df.set_index("Date", drop=True)
df = df.loc[df["Purpose"].isin(["Train", "Validate"])]

fig = plt.figure(figsize=(5, 3.8))
ax = fig.add_axes([0.12, 0.14, 0.84, 0.67])

ax.plot(df["DataNormalised"], label="Original", color=purple)
ax.plot(df["ModelledNormalised"], label="Modelled", color=blue)

i1 = df.index[0]
i2 = df.loc[df["Purpose"] == "Train"].index[-1]
i3 = df.index[-1]
I1 = i1 + (i2 - i1) / 2
I2 = i2 + (i3 - i2) / 2 + pd.DateOffset(months=3)

ax.plot([i2, i2], [-5.3, 6.4], color=grey, dashes=(3, 3))
ax.text(I1, 5.55, "Training", ha="center", fontsize=14)
ax.text(I2, 5.55, "Validation", ha="center", fontsize=14)

ax.set_xlabel("Date", fontsize=14, labelpad=5)
ax.set_ylabel("Residuals", fontsize=14)
fig.suptitle("Modelling Residual Series\nFor Case 4 Using LSTM", fontsize=20, y=0.97)
ax.legend(fontsize=14, loc="lower left")

ax.set_ylim((-6, 7))
ax.set_yticks([-6, -4, -2, 0, 2, 4, 6])
ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
even_years = pd.date_range(start="2010", end="2022", freq="2YE")
ax.set_xticks(even_years)
ax.set_xticklabels(even_years.year, fontsize=12)
odd_years = pd.date_range(start="2011", end="2021", freq="2YE")
ax.set_xticks(odd_years, minor=True)
ax.tick_params(axis='x', which='minor')


output_path = join(base_path, "Output", "Results", "Forecasting",
                   "ResidualForecast_LSTM_Case_4.svg")
plt.savefig(output_path, format="svg")
