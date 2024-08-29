import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

from hgutilities.utils import make_folder
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

from utils import get_base_path, purple, blue, grey
from DataProcessing.crime import Crime
from DataProcessing.timeseries import Time


crime = Crime(lsoa="E01034220", agg_crime="Major", major="Public Order Offences")
crime.process()

data = crime.crime.iloc[0, 3:]
data = data.transpose()
data.index = pd.to_datetime(data.index, format="%Y %m")
moving_average = data.rolling(window=13, center=True, min_periods=1).mean()

fig = plt.figure(figsize=(5, 4))
ax = fig.add_axes([0.15, 0.15, 0.8, 0.7])

data.plot(ax=ax, color=purple, label="Original values")
moving_average.plot(ax=ax, color=blue, label="Moving average")

fig.suptitle("Public Order Offences in E01034220", fontsize=20)
ax.set_xlabel("Date", fontsize=16, labelpad=10)
ax.set_ylabel("Recorded Crimes Per 100,000 People",
              fontsize=16, labelpad=10)
ax.legend(fontsize=14)
ax.set_ylim(0, 1600)

ax.set_yticks(ax.get_yticks())
ax.set_yticklabels(ax.get_yticklabels(), fontsize=10)
even_years = pd.date_range(start="2010", end="2024", freq="2YE")
ax.set_xticks(even_years)
ax.set_xticklabels(even_years.year, fontsize=10)
odd_years = pd.date_range(start="2011", end="2023", freq="2YE")
ax.set_xticks(odd_years, minor=True)
ax.tick_params(axis='x', which='minor')

path = join(get_base_path(__file__),
            "Output", "Results", "Spatial Temporal",
            "Results_PublicOrderOffences_Newham.pdf")
make_folder(dirname(path))
plt.savefig(path, format="pdf")
