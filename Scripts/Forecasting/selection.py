import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

from os.path import join
from os import listdir
import json

import matplotlib.pyplot as plt

from utils import get_base_path


def get_residuals(folder_name):
    path = join(results_path, folder_name, "Summary.json")
    with open(path, "r") as file:
        contents = json.load(file)
    residuals = contents[0]["MSE Forecast"]
    return residuals

base_path = get_base_path(__file__)
results_path = join(base_path, "Output", "Forecasting ARIMA", "Case_1")

results = {folder_name: get_residuals(folder_name)
           for folder_name in listdir(results_path)}
results = dict(sorted(results.items(), key=lambda item: item[1])[:20])

fig, ax = plt.subplots(1, figsize=(10, 6))
ax.bar(results.keys(), results.values(), width=1)

ax.set_xticks([])
ax.set_xticks(range(len(results)))
ax.set_xticklabels(results.keys(), rotation=45, ha='right')

ax.set_xlabel('Architecture')
ax.set_ylabel('MSE')
ax.set_title('Best Architectures')
plt.show()
