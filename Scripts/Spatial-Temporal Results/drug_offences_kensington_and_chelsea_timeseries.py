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


crime = Crime(agg_crime="Major", major="Drug Offences")
crime.process()

lsoas = [
    'E01002852', 'E01002883', 'E01002884', 'E01002831', 'E01002856',
    'E01002830', 'E01002829', 'E01002882', 'E01002886', 'E01002833',
    'E01002832', 'E01002878', 'E01002854', 'E01002875', 'E01002857',
    'E01002905', 'E01002855', 'E01002879']
data = crime.crime.loc[crime.crime["LSOA"].isin(lsoas)]
data = data.iloc[:, 3:]
data = data.sum(axis=0)
data.index = pd.to_datetime(data.index, format="%Y %m")

fig = plt.figure(figsize=(5, 3.9))
ax = fig.add_axes([0.18, 0.15, 0.8, 0.65])
ax.plot(data.index, data.values, color=purple, label="Original values")
ax.set_ylim(0, 24000)

fig.suptitle("Drug Offences in Northern\nKensington and Chelsea",
             fontsize=20, y=0.97)
ax.set_xlabel("Date", fontsize=16, labelpad=10)
ax.set_ylabel("Recorded Crimes Per 100,000 People",
              fontsize=16, labelpad=10)

ax.set_yticks(ax.get_yticks())
ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
even_years = pd.date_range(start="2010", end="2022", freq="2YE")
ax.set_xticks(even_years)
ax.set_xticklabels(even_years.year, fontsize=12)
odd_years = pd.date_range(start="2011", end="2023", freq="2YE")
ax.set_xticks(odd_years, minor=True)
ax.tick_params(axis='x', which='minor')

path = join(get_base_path(__file__),
            "Output", "Results", "Spatial Temporal",
            "Results_DrugOffences_KensingtonAndChelsea_Timeseries.pdf")
make_folder(dirname(path))
plt.savefig(path, format="pdf")
