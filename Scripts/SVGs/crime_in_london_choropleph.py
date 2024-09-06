import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt
from matplotlib import rc
from hgutilities.utils import make_folder

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Century Gothic"})
rc('mathtext', default='regular') 


crime = Crime(agg_time="Total", agg_crime="Total")
crime.process()
crime.plot(output=None, year=None, month=None,
           figsize=(5, 4), axis_size=[0, 0, 0.8, 0.9])
crime.plot_obj.cbar_fig.set_ylabel(
    "Recorded Crimes Per 100,000 People",
    labelpad=15.5, fontsize=16)

crime.plot_obj.ax.set_title("")
crime.plot_obj.fig.suptitle(
    "Overall London Crime Rate\nFrom 2010 to 2024",
    fontsize=20, y=0.97)

crime.plot_obj.fig.subplots_adjust(left=0, bottom=0, right=1,
                                   top=1, wspace=0, hspace=0)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "CrimeInLondonDistribution.svg")
make_folder(dirname(path))
plt.savefig(path, format="svg")
