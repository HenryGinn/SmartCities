import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))


import matplotlib.pyplot as plt
import numpy as np

import utils
from DataProcessing.crime import Crime

plt.rcParams.update({"font.family": "Century Gothic"})
colors = ["#6c17b9", "#1db8f7", "#a8acaf"]

crime = Crime(major="Public Order Offences",
              agg_spatial="City",
              agg_time="Year",
              population_weighted=False)

crime.process()
crime = crime.crime[["Minor Category", "2010", "2024"]]
crime = crime.loc[crime["Minor Category"] != "Violent Disorder"]

minor_map = {
    "Public Fear Alarm or Distress": "Alarm or\nDistress",
    "Race or Religious Agg Public Fear": "Racially or\nReligiously Aggravated",
    "Other Offences Public Order": "Other"}
crime["Minor Category"] = crime["Minor Category"].apply(minor_map.get)

h = 0.83
w = 0.5
b = 0.12
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_axes([0, b, w, h])
ax2 = fig.add_axes([0.5, b, w, h])

ax1.pie(crime["2010"], colors=colors, startangle=100, explode=[False, 0.2, False],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'antialiased': True})
ax2.pie(crime["2024"], colors=colors, startangle=100, explode=[False, 0.2, False],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'antialiased': True})

ax1.set_title("2010", fontsize=24, y=0.92, x=0.3)
ax2.set_title("2024", fontsize=24, y=0.92, x=0.7)

fig.suptitle("Public Order Offences", fontsize=28)
legend = fig.legend(
    crime["Minor Category"], loc="lower center",
    fontsize=19, ncols=3)
for t in legend.get_texts():
    t.set_ha('center')

path = join(utils.get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "Results_PublicOrderOffences_MinorChanges")
plt.savefig(f"{path}.svg", format="svg")
plt.savefig(f"{path}.png", format="png", dpi=600)
