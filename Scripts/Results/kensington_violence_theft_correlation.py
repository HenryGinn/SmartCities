import sys
import os
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt
from hgutilities.utils import make_folder

from DataProcessing.crime import Crime
from utils import purple, blue, grey, get_base_path


plt.rcParams.update({"font.family": "Times New Roman"})


crime = Crime(agg_time="Total", agg_crime="Major")
crime.process()
crime = crime.crime
crime = crime.pivot_table(index=["Borough", "LSOA"],
                          columns="Major Category",
                          values="Crime",
                          aggfunc="sum").reset_index()
crime = crime[["Borough", "LSOA", "Violence Against the Person", "Theft"]]

correlations = (crime.groupby("Borough")
                .apply(lambda x: x["Theft"].corr(x["Violence Against the Person"]),
                       include_groups=False))
correlations = correlations.sort_values(ascending=False)

fig = plt.figure(figsize=(10, 4))
ax = fig.add_axes([0.1, 0.4, 0.9, 0.5])
ax.bar(correlations.index, correlations.values, color=purple)

ax.set_ylim(0, 1)
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right',
                   fontsize=10)
ax.set_title("Correlation Between Theft and Violence Against the Person",
             fontsize=18, pad=10)
ax.set_ylabel("Correlation", fontsize=14)
ax.set_xlabel("Borough", fontsize=14, labelpad=-25)

path = join(get_base_path(__file__), "Output", "Results", "Spatial Temporal",
            "Results_CorrelationsViolenceAndTheft.pdf")
make_folder(dirname(path))
plt.savefig(path, bbox_inches="tight", format="pdf")
