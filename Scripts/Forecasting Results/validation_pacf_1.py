import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

from os.path import join
from os import listdir
import json

from hgutilities.utils import json, make_folder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from utils import get_base_path


plt.rcParams.update({"font.family": "Times New Roman"})
purple = "#6c17b9"
blue = "#1db8f7"
grey = "#6d6d6d"

base_path = get_base_path(__file__)
data_path = join(
    base_path, "Output", "Results", "Data",
    "Case_1", "SARIMA", "Autocorrelations_train.json")

with open(data_path, "r") as file:
    contents = json.load(file)

pacf = np.array(contents["PACF"])
x = np.arange(pacf.size)

fig = plt.figure(figsize=(5, 3.8))
ax = fig.add_axes([0.2, 0.14, 0.76, 0.67])

self.ax.bar(x, pacf, width=0.1, color=self.purple)
self.ax.plot([-0.5, x[-1]+1], cf_confidence,
             color=grey, dashes=(3, 3))
ax.set_ylim((-0.25, 1))

ax.set_xlabel("Lag", fontsize=14, labelpad=5)
ax.set_ylabel("Partial Autocorrelation", fontsize=14, labelpad=10)
fig.suptitle("Partial Autocorrelation in the Validation\nRegion For Case 1",
             fontsize=20, y=0.97)
ax.legend(fontsize=14, loc="lower left")

#ax.set_yticks(ax.get_yticks())
#ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
#ax.set_xticks(ax.get_xticks())
#ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)

output_path = join(
    base_path, "Output", "Results", "Forecasting",
    "PACF_SARIMA_Case_1.pdf")
plt.savefig(output_path, format="pdf")
