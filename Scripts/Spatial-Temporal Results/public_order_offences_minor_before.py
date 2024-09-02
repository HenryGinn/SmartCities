import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))


import matplotlib.pyplot as plt
import numpy as np

import utils
from DataProcessing.crime import Crime

plt.rcParams.update({"font.family": "Times New Roman"})
colors = ["#6c17b9", "#1db8f7", "#a8acaf"]

crime = Crime(major="Public Order Offences",
              agg_spatial="City",
              agg_time="Year",
              population_weighted=False)

crime.process()
crime = crime.crime[["Minor Category", "2011", "2023"]]
crime = crime.loc[crime["Minor Category"] != "Violent Disorder"]

minor_map = {
    "Public Fear Alarm or Distress": "Public Fear\nAlarm or Distress",
    "Race or Religious Agg Public Fear": "Race or Religious\nAggravated Public Fear",
    "Other Offences Public Order": "Other Public\nOrder Offences"}
crime["Minor Category"] = crime["Minor Category"].apply(minor_map.get)

h = 0.85
w = 0.5
b = 0.1
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_axes([0, b, w, h])
ax2 = fig.add_axes([0.5, b, w, h])

ax1.pie(crime["2011"], colors=colors, startangle=100, explode=[False, 0.2, False],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'antialiased': True})
ax2.pie(crime["2023"], colors=colors, startangle=100, explode=[False, 0.2, False],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'antialiased': True})

ax1.set_title("2011", fontsize=16, y=0.95)
ax2.set_title("2023", fontsize=16, y=0.95)

fig.suptitle("Public Order Offences", fontsize=20)
legend = fig.legend(
    crime["Minor Category"], loc="lower center",
    fontsize=16, ncols=3)
for t in legend.get_texts():
    t.set_ha('center')

path = join(utils.get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "Results_PublicOrderOffences_MinorChanges")
plt.savefig(f"{path}.pdf", format="pdf")
plt.savefig(f"{path}.png", format="png", dpi=600)
