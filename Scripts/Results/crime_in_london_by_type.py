import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt
from matplotlib import rc
from hgutilities.utils import make_folder

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Times New Roman"})


crime = Crime(agg_time="Total", agg_crime="Major", agg_spatial="City")
crime.process()
crime.remove_major()
crime = crime.crime

fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0.2, 0.3, 0.8, 0.6])

ax.bar(crime["Major Category"], crime["Crime"], color=purple)
fig.suptitle("Crime Rates by Category", fontsize=20)

ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
                   ha='right', fontsize=10)
ax.set_ylabel("Reported Crimes per 100,000 People", fontsize=14)
ax.set_xlabel("Category", fontsize=14, labelpad=None)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "CrimeRatesByCategory.pdf")
make_folder(dirname(path))
plt.savefig(path, bbox_inches="tight", format="pdf")
