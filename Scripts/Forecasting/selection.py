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
nulls_v = [5.849196, 3.884590, 2.707384, 50.267810]
nulls_t = [1.831300, 0.904695, 0.322781, 4.407980]

methods = ["LSTM"]
for method in methods:
    for case in range(1, 5):
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

        fig, ax = plt.subplots(1, figsize=(10, 6))
        index = np.arange(len(df))
        ax.semilogy(index, df["MSE Validate"], color=blue, label="Modelled Validate")
        ax.bar(index, df["MSE Test"], width=1.2, color=purple, label="Modelled Test")
        ax.semilogy([0, len(df)-1], [nulls_v[case-1], nulls_v[case-1]], color=grey, label="Control Validate")
        ax.semilogy([0, len(df)-1], [nulls_t[case-1], nulls_t[case-1]], color="black", label="Control Test")

        handles, labels = ax.get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
        ax.legend(handles, labels, fontsize=18)

        ax.set_xticks([])
        ax.tick_params(axis='y', labelsize=16)
        ax.set_xlabel("Hyperparameter Configurations", fontsize=18)
        ax.set_ylabel("MSE", fontsize=18)
        ax.set_title(f"{method}, Case {case}", fontsize=24)

        output_path_plot = join(base_path, "Output", "Selection", method, f"Selection_{method}_Case_{case}.pdf")
        output_path_text = join(base_path, "Output", "Selection", method, f"Selection_{method}_Case_{case}.txt")
        make_folder(dirname(output_path_plot))
        
        with open(output_path_text, "w+") as file:
            file.writelines(df.to_string())
        plt.savefig(output_path_plot, format="pdf", bbox_inches="tight")
