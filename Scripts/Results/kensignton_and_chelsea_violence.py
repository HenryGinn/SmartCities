import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt
from matplotlib import rc
from hgutilities.utils import make_folder

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Times New Roman"})
rc('mathtext', default='regular') 


crime = Crime(agg_time="Total", agg_crime="Major",
              borough="Kensington and Chelsea",
              major="Violence Against the Person")
crime.process()
crime.plot(output=None, year=None, month=None,
           figsize=(5, 5), axis_size=[0, 0, 0.8, 0.9])

crime.plot_obj.cbar_fig.set_yticks([10000])
crime.plot_obj.cbar_fig.set_yticklabels(
    [r"$10^4$"], fontsize=14)
crime.plot_obj.cbar_fig.set_yticks([
    5000, 6000, 7000, 8000, 9000, 20000, 30000, 40000, 50000], minor=True)
crime.plot_obj.cbar_fig.set_yticklabels(
    [r"$5 \cdot 10^3$", "", "", "", "", "", "", "", r"$5 \cdot 10^4$"],
    minor=True, fontsize=12)
crime.plot_obj.cbar_fig.set_ylabel("Reported Crimes Per 100,000 People", labelpad=5)

crime.plot_obj.ax.set_title("")
crime.plot_obj.fig.suptitle(
    "Violence Against the Person in\nKensington and Chelsea Since 2010",
    fontsize=20, y=0.97)

crime.plot_obj.fig.subplots_adjust(left=0.05, bottom=-0.2, right=0.83,
                                   top=1.1, wspace=0, hspace=0)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "Results_Kensington_Violence.pdf")
make_folder(dirname(path))
plt.savefig(path, format="pdf")

