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


crime = Crime(agg_time="Month", agg_crime="Major",
              borough="Kensington and Chelsea",
              major="Drug Offences")
crime.process()
crime.crime = crime.crime.drop(columns=[
    "01", "02", "03", "04", "05", "06", "07", "09", "10", "11", "12"])
crime.plot(output=None, year=None, month=None, cax_position=[0.75, 0.04, 0.05, 0.76],
           figsize=(5, 4.1), axis_size=[0.02, 0.04, 0.7, 0.76])
crime.plot_obj.cbar_fig.set_ylabel(
    "Recorded Crimes Per 100,000 People", labelpad=15.5, fontsize=16)

crime.plot_obj.ax.set_title("")
crime.plot_obj.fig.suptitle(
    "Average Drug Offences in\nKensington and Chelsea In August",
    fontsize=20, y=0.97)

crime.plot_obj.fig.subplots_adjust(left=0, bottom=0, right=1,
                                   top=1, wspace=0, hspace=0)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "Results_KensingtonAndChelsea_DrugOffences_ChoroplethAugust.svg")
make_folder(dirname(path))
plt.savefig(path, format="svg")
