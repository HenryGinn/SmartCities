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


plt.rcParams.update({"font.family": "Century Gothic"})
purple = "#6c17b9"
blue = "#1db8f7"
grey = "#6d6d6d"

base_path = get_base_path(__file__)
data_path = join(
    base_path, "Output", "Results", "Data",
    "Case_1", "LSTM", "Case_1_train_history.json")

with open(data_path, "r") as file:
    contents = json.load(file)

train = np.array(contents["Train"])
validate = np.array(contents["Validate"])
x = np.arange(train.size) + 1

fig = plt.figure(figsize=(5, 3.8))
ax = fig.add_axes([0.2, 0.14, 0.76, 0.67])

ax.semilogy(x, train, color=purple, label="Training")
ax.semilogy(x, validate, color=blue, label="Validating")

ax.set_xlabel("Epoch", fontsize=14, labelpad=5)
ax.set_ylabel("Mean Squared Error", fontsize=14, labelpad=10)
fig.suptitle("Training History in the Validation\nRegion For Case 1",
             fontsize=20, y=0.97)
ax.legend(fontsize=14, loc="lower left")

#ax.set_yticks(ax.get_yticks())
#ax.set_yticklabels(ax.get_yticklabels(), fontsize=12)
#ax.set_xticks(ax.get_xticks())
#ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)

output_path = join(
    base_path, "Output", "Results", "Forecasting",
    "Validation_History_Case_1.svg")
plt.savefig(output_path, format="svg")
