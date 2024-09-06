import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))
import io
import PIL

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import pandas as pd
from hgutilities.utils import make_folder
from scipy.interpolate import CubicSpline

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Times New Roman"})
rc('mathtext', default='regular') 

crime = Crime(
    agg_time="Year",
    agg_crime="Major",
    major="Public Order Offences")
crime.process()
df = crime.crime


times = np.arange(2010, 2025)
times_smooth = np.linspace(times.min(), times.max(), 100)
time_columns = [str(year) for year in times]
years = [str(round(year)) for year in times_smooth]

def interpolate(x):
    cs = CubicSpline(x.index, x.values)
    new_series = pd.Series(dict(zip(times_smooth, cs(times_smooth))))
    return new_series

interpolated = df[time_columns].apply(interpolate, axis=1)
df = df[["LSOA", "Borough"]]
df = (pd
      .merge(df, interpolated, on=df.index)
      .drop(columns="key_0"))

df[times_smooth] = df[times_smooth].map(lambda x: 1 if x < 1 else x)
values = df[times_smooth].values
minimum = np.min(values)
maximum = np.max(values)

def create_figure(data, year):
    plt.close("all")
    crime.crime = data
    print(data.columns.values[-1])
    crime.plot(output=None, year=None, month=None,
               figsize=(5, 4), axis_size=[0, 0, 0.8, 0.9],
               vmin=minimum, vmax=maximum)
    crime.plot_obj.cbar_fig.set_ylabel(
        "Recorded Crimes Per 100,000 People",
        labelpad=15.5, fontsize=16)

    crime.plot_obj.ax.set_title("")
    crime.plot_obj.fig.suptitle(
        f"Overall London Crime Rate in {year}",
        fontsize=20, y=0.97)

    _ = crime.plot_obj.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

def get_frame(data, year):
    create_figure(data, year)
    buffer = io.BytesIO()
    plt.savefig(buffer, dpi=600)
    buffer.seek(0)
    image = PIL.Image.open(buffer)
    return image


output_path = join(
    get_base_path(__file__),
    "Output", "Results", "Animations",
    "PublicOrderOffences.gif")

make_folder(dirname(output_path))

frames = [get_frame(df[["LSOA", "Borough", time]], year)
          for time, year in zip(times_smooth, years)]
frames[0].save(output_path, loop=True, save_all=True, append_images=frames[1:])
