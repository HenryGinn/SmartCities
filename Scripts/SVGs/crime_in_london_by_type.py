import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt
from matplotlib import rc
from hgutilities.utils import make_folder

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path, add_line_breaks


plt.rcParams.update({"font.family": "Century Gothic"})


crime = Crime(agg_time="Total", agg_crime="Major", agg_spatial="City", population_weighted=False)
crime.process()
crime.remove_major()
crime = crime.crime

fig = plt.figure(figsize=(5, 4))
ax = fig.add_axes([0.13, 0.3, 0.86, 0.55])

labels = [add_line_breaks(label, length=20)
          for label in crime["Major Category"].values]

ax.bar(labels, crime["Crime"], color=purple)
fig.suptitle("Crime Rates by Category", fontsize=20, y=0.97)

ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
                   ha='right', fontsize=10)
ax.set_ylabel("Recorded Crimes per 100,000 People", fontsize=14, labelpad=10)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "CrimeRatesByCategory.svg")
make_folder(dirname(path))
plt.savefig(path, format="svg")
