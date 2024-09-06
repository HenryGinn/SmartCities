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


plt.rcParams.update({"font.family": "Century Gothic"})
purple = "#6c17b9"
blue = "#1db8f7"
grey = "#6d6d6d"


def get_residuals(folder_name, fit_category_index):
    path = join(results_path, folder_name, "Summary.json")
    with open(path, "r") as file:
        contents = json.load(file)
    residuals = contents[fit_category_index]["MSE Forecast"]
    return residuals

base_path = get_base_path(__file__)
nulls_v = 15.116594452988025
nulls_t = 8.16435185142622


results_path = join(base_path, "Output", "LSTM", f"Case_1")
results_validate = {folder_name: get_residuals(folder_name, 0)
                    for folder_name in listdir(results_path)}
df = pd.DataFrame({key: value for key, value in zip(
    ["Hyperparameters", "MSE Validate"], list(zip(*results_validate.items())))}
                  ).set_index("Hyperparameters")
results_test = [get_residuals(folder_name, 1)
                for folder_name in listdir(results_path)]
df.loc[:, "MSE Test"] = results_test
df = df.sort_values("MSE Validate")

fig = plt.figure(figsize=(5, 2.7))
ax = fig.add_axes([0.15, 0.14, 0.78, 0.69])
index = np.arange(len(df))
ax.semilogy(index, df["MSE Validate"], color=blue, label="Modelled Validate")
ax.bar(index, df["MSE Test"], width=1.2, color=purple, label="Modelled Test")
ax.semilogy([0, len(df)-1], [nulls_v, nulls_v], color=blue, dashes=(3, 3), linewidth=1.5, label="Control Validate")
ax.semilogy([0, len(df)-1], [nulls_t, nulls_t], color=purple, dashes=(3, 3), linewidth=1.5, label="Control Test")

ax.set_ylim((0.1, 1.3))
ax.set_xticks([])
ax.set_yticks(ax.get_yticks())
ax.set_yticklabels(ax.get_yticklabels(), fontsize=10)
ax.set_xlabel("Hyperparameter Configurations", fontsize=14, labelpad=10)
ax.set_ylabel("MSE", fontsize=14)
fig.suptitle(f"LSTM Configurations For Case 1", fontsize=20, y=0.97)

output_path_plot = join(base_path, "Output", "Results", "Forecasting", f"Selection_LSTM_Case_1.svg")

plt.savefig(output_path_plot, format="svg")
