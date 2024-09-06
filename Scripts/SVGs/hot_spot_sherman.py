import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from hgutilities.utils import make_folder

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Century Gothic"})
rc('mathtext', default='regular') 

x = np.array([0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.3, 6.0, 6.8, 7.9, 9.4, 11.4, 14.4, 19.4, 29.2, 60.4])
y = np.array([0, 50.4, 51.7, 53.1, 54.6, 56.3, 58.4, 60.6, 63.0, 65.7, 68.8, 72.4, 76.7, 81.9, 88.9, 100])
fig = plt.figure(figsize=(5, 4.1))
ax = fig.add_axes([0.15, 0.15, 0.8, 0.72])

ax.plot(x, y, color=purple)

ax.set_xlabel(
    "Cumulative Locations (% Addresses)",
    labelpad=5, fontsize=16)
    
ax.set_ylabel(
    "Cumulative Calls to Police (%)",
    labelpad=5, fontsize=16)

fig.suptitle(
    "Spatial Distribution of Crimes",
    fontsize=20, y=0.97)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "SpatialDistributionOfCrimes.svg")
make_folder(dirname(path))
plt.savefig(path, format="svg")
