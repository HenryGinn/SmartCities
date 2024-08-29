import sys
import os
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


import matplotlib.pyplot as plt
import numpy as np

import utils
from DataProcessing.crime import Crime
from DataProcessing.plotter import Plotter
from DataProcessing.interesting import Interesting
from DataProcessing.timeseries import Time


#crime = Crime(agg_time="Total", agg_spatial="Borough", agg_crime="Total", title="Total Crime in London")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London\nby LSOA Region")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Croydon", title="Total Crime in Croydon")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Westminster", title="Total Crime in Westminster")
#crime = Crime(agg_time="Total", lsoa="E01035716", title="Total Crime around Regents Street")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London by LSOA Region")
#crime = Crime(agg_time="Total", agg_crime="Total", population_weighted=False)
#crime = Crime(agg_crime="Total", agg_spatial="Borough", borough="Westminster")
#crime.process()
#crime.plot(year=None, month=None)

a = Crime(major="Public Order Offences", agg_crime="Major", population_weighted=False)
a.process()
b = a.crime.copy()
b["Total"] = b.iloc[:, 4:].sum(axis=1)
b["Ratio"] = b.iloc[:, -36:].mean(axis=1).values/b.iloc[:, 6:42].mean(axis=1).values
c = b.sort_values("Ratio", ascending=False)
d = c.loc[c["Ratio"] != np.inf]
d = d.loc[d["Total"] > 300]
d = d.dropna()
print(len(d))

k = 2
for i in range(50):
    data = d.iloc[k*i:k*(i+1), :-2]
    print(d.iloc[k*i:k*(i+1), :])
    t = Time(data, output="Show", label_format='f"{borough} {lsoa}"')
    t.create_figure()

#crime = Crime(lsoa="E01001562", major="Public Order Offences", agg_crime="Major")
#crime = Crime(agg_spatial="City", major="Public Order Offences", agg_crime="Major")
#crime.process()
#crime.time_plot(output="Show")

#b["Ratio"] = b.iloc[:, -36:].mean(axis=1).values/b.iloc[:, 6:42].mean(axis=1).values

#interesting = Interesting(figures=True, csv=True, series=True)
#interesting.analyse()
#interesting.output()

#plotter = Plotter()
#plotter.generate(crime_type="Major", region="Borough", resolution="LSOA", time="Total")
#plotter.generate(crime_type="Major", region="Borough", resolution="LSOA", time="Total")
#plotter.generate(crime_type="Major", region="City", resolution="LSOA", time="Total")
#plotter.generate(crime_type="Total", region="Borough", resolution="LSOA", time="Total")
#plotter.generate(crime_type="Total", region="City", resolution="LSOA", time="Total")
#plotter.generate(boroughs=["Westminster"], categories_major=["Theft"], animate=True, time="Full", start=2024, region="Borough")
#plotter.generate(animate=True, time="Month", region="Borough", crime_type="Total")
#plotter.generate(animate=True, time="Year", region="Borough", crime_type="Total")
#plotter.generate(animate=True, time="Full", region="Borough", crime_type="Total")
#plotter.generate(animate=True, time="Full", region="City", crime_type="Total")
#plotter.generate(animate=True, time="Month", region="City", crime_type="Total")
#plotter.generate(animate=True, time="Year", region="City", crime_type="Total")
#plotter.generate(animate=True, time="Month", region="Borough", crime_type="Major")
#plotter.generate(animate=True, time="Year", region="Borough", crime_type="Major")
#plotter.generate(animate=True, time="Full", region="Borough", crime_type="Major")
#plotter.generate(animate=True, time="Full", region="City", crime_type="Major")
#plotter.generate(animate=True, time="Month", region="City", crime_type="Major")
#plotter.generate(animate=True, time="Year", region="City", crime_type="Major")
#plotter.generate(animate=True, time="Full", region="City", crime_type="Total", resolution="Borough")
#plotter.generate(animate=True, time="Month", region="City", crime_type="Total", resolution="Borough")
#plotter.generate(animate=True, time="Year", region="City", crime_type="Total", resolution="Borough")

"""
crime_1 = Crime(agg_crime="Major", major="Arson and Criminal Damage", lsoa="E01004734", population_weighted=False)
crime_2 = Crime(agg_crime="Major", major="Violence Against the Person", lsoa="E01000863", population_weighted=False)
crime_3 = Crime(agg_crime="Major", major="Vehicle Offences", lsoa="E01002818", population_weighted=False)
crime_4 = Crime(agg_crime="Major", major="Theft", lsoa="E01035716", population_weighted=False)
crimes = [crime_1, crime_2, crime_3, crime_4]


fig, axes = plt.subplots(nrows=2, ncols=2)
axes = axes.flatten()

for index, (crime, ax) in enumerate(zip(crimes, axes)):
    crime.process()
    crime.time(output=None, title=index+1, label_format="f'{crime} {lsoa}'")
    crime.time_obj.data.to_csv(os.path.join(crime.path_output_base, f"{index}.csv"))
    crime.time_obj.fig, crime.time_obj.ax = fig, ax
    crime.time_obj.create_plot()

fig.subplots_adjust(left=0.05, right=0.95, bottom=0.08, top=0.95, wspace=0.15, hspace=0.3)
plt.show()
"""
