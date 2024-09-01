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


def get_residuals(folder_name, fit_category_index):
    path = join(results_path, folder_name, "Summary.json")
    with open(path, "r") as file:
        contents = json.load(file)
    residuals = contents[fit_category_index]["MSE Forecast"]
    return residuals

base_path = get_base_path(__file__)
nulls_v = [15.116594452988025, 6.628650253619732, 2.429720862049619, 22.610260686255142]
nulls_t = [8.16435185142622, 0.8105473322991597, 0.5148320194421647, 12.173913936193571]

methods = ["SARIMA"]
for method in methods:
    for case in range(1, 2):
        results_path = join(base_path, "Output", method, f"Case_{case}")

        results_validate = {folder_name: get_residuals(folder_name, 0)
                         for folder_name in listdir(results_path)}
        df = pd.DataFrame({key: value for key, value in zip(
            ["Hyperparameters", "MSE Validate"], list(zip(*results_validate.items())))}
                          ).set_index("Hyperparameters")
        results_test = [get_residuals(folder_name, 1)
                        for folder_name in listdir(results_path)]
        df.loc[:, "MSE Test"] = results_test
        df = df.sort_values("MSE Validate")

        fig, ax = plt.subplots(1, figsize=(5, 3))
        index = np.arange(len(df))
        ax.semilogy(index, df["MSE Validate"], color=blue, label="Modelled Validate")
        ax.bar(index, df["MSE Test"], width=1.2, color=purple, label="Modelled Test")
        ax.semilogy([0, len(df)-1], [nulls_v[case-1], nulls_v[case-1]], color=blue, dashes=(3, 3), linewidth=2, label="Control Validate")
        ax.semilogy([0, len(df)-1], [nulls_t[case-1], nulls_t[case-1]], color=purple, dashes=(3, 3), linewidth=2, label="Control Test")

        ax.set_ylim((0.01, 1.3))
        ax.set_xticks([])
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=10)
        ax.set_xlabel("Hyperparameter Configurations", fontsize=14)
        ax.set_ylabel("MSE", fontsize=14)
        ax.set_title(f"{method}, Case {case}", fontsize=20)

        output_path_plot = join(base_path, "Output", "Selection", method, f"Selection_{method}_Case_{case}.pdf")
        output_path_text = join(base_path, "Output", "Selection", method, f"Selection_{method}_Case_{case}.txt")
        make_folder(dirname(output_path_plot))
        
        #with open(output_path_text, "w+") as file:
        #    file.writelines(df.to_string())
        plt.savefig(output_path_plot, format="pdf", bbox_inches="tight")

"""
handles, labels = ax.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))

fig_legend = plt.figure(figsize=(10, 0.5))
fig_legend.legend(
    handles, labels, ncols=4, fontsize=16, loc="center",
    bbox_to_anchor=[0.1, 0.02, 0.8, 0.96])

output_path_legend = join(base_path, "Output", "Selection", method, f"Selection_{method}_Legend.pdf")
fig_legend.savefig(output_path_legend, format="pdf")
"""
