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
crime = Crime(agg_time="Total", agg_crime="Total", population_weighted=True)
#crime = Crime(agg_crime="Total", agg_spatial="Borough", borough="Westminster")
crime.process()
#crime.plot(year=None, month=None)

#plotter = Plotter()
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
#plotter.generate(animate=True, time="Full", region="City", crime_type="Total", resolution="Borough")
#plotter.generate(animate=True, time="Month", region="City", crime_type="Total", resolution="Borough")
#plotter.generate(animate=True, time="Year", region="City", crime_type="Total", resolution="Borough")

#interesting = Interesting(figures=True, csv=True, series=True)
#interesting.analyse()
#interesting.output(measure="Flat")
#interesting.output_category(measure="Mean", category="Theft")

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
