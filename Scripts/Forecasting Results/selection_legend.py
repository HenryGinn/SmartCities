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


plt.rcParams.update({"font.family": "Times New Roman"})
purple = "#6c17b9"
blue = "#1db8f7"
grey = "#6d6d6d"


base_path = get_base_path(__file__)

fig, ax = plt.subplots(1)
ax.bar(1, 1, color=purple, label="Modelled Test", width=1.2,)
ax.plot(1, 1, color=blue, label="Modelled Validate")
ax.semilogy(1, 1, color=blue, dashes=(3, 3), linewidth=1.5, label="Control Validate")
ax.semilogy(1, 1, color=purple, dashes=(3, 3), linewidth=1.5, label="Control Test")

handles, labels = ax.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))

fig_legend = plt.figure(figsize=(10, 0.5))
fig_legend.legend(
    handles, labels, ncols=4, fontsize=16, loc="center",
    bbox_to_anchor=[0.1, 0.02, 0.8, 0.96])

output_path = join(base_path, "Output", "Results", "Forecasting", "Selection_Legend.pdf")
fig_legend.savefig(output_path, format="pdf")
