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
from scipy.interpolate import PchipInterpolator

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Times New Roman"})
rc('mathtext', default='regular') 

crime = Crime(
    agg_time="Month",
    agg_crime="Major",
    major="Drug Offences",
    borough="Kensington and Chelsea")
crime.process()
df = crime.crime


time_columns = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
times = np.array([int(time) for time in time_columns])
times_smooth = np.linspace(times.min(), times.max(), 90)
months = [str(round(month)) for month in times_smooth]

def interpolate(x):
    cs = PchipInterpolator(x.index, x.values)
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

def create_figure(data, month):
    plt.close("all")
    crime.crime = data
    print(data.columns.values[-1])
    crime.plot(output=None, year=None, month=None,
               cax_position=[0.75, 0.06, 0.05, 0.76],
               figsize=(5, 3.9), axis_size=[0.02, 0.04, 0.74, 0.8],
               vmin=minimum, vmax=maximum)
    crime.plot_obj.cbar_fig.set_ylabel(
        "Recorded Crimes Per 100,000 People", labelpad=15.5, fontsize=16)

    crime.plot_obj.ax.set_title("")
    crime.plot_obj.fig.suptitle(
        f"Average Drug Offences in Kensington\nand Chelsea In {month}",
        fontsize=20, y=0.97)

    crime.plot_obj.fig.subplots_adjust(left=0, bottom=0, right=1,
                                       top=1, wspace=0, hspace=0)

def get_frame(data, year):
    create_figure(data, year)
    buffer = io.BytesIO()
    plt.savefig(buffer, dpi=300)
    buffer.seek(0)
    image = PIL.Image.open(buffer)
    return image


output_path = join(
    get_base_path(__file__),
    "Output", "Results", "Animations",
    "DrugOffences.gif")

make_folder(dirname(output_path))

frames = [get_frame(df[["LSOA", "Borough", time]], month)
          for time, month in zip(times_smooth, months)]
frames[0].save(output_path, loop=True, save_all=True, append_images=frames[1:])
