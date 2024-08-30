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
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import warnings

# Suppress all warnings
warnings.simplefilter("ignore")

a = Crime(agg_crime="Major")
a.process()
b = a.crime.copy()
inputs = np.arange(b.iloc[:, 3:].shape[1])

def sinusoidal(x, c, A, B, phi):
    return c + A * np.exp((B**2+1)*np.sin(np.pi*x / 6 + phi))

def fit_and_calculate_r2(row):
    try:
        popt, _ = curve_fit(sinusoidal, inputs, row.values[3:], maxfev=10000)
        y_pred = sinusoidal(inputs, *popt)
        r2 = r2_score(row.values[3:], y_pred)
    except:
        r2 = 0
    return r2

b["R2"] = b.apply(fit_and_calculate_r2, axis=1)
b = b.sort_values("R2", ascending=False)

k = 2
for i in range(50):
    data = b.iloc[k*i:k*(i+1), :-1]
    print(b.iloc[k*i:k*(i+1), :])
    t = Time(data, output="Show", label_format='f"{borough} {lsoa} {crime}"')
    t.create_figure()
"""

"""
a = Crime(major="Public Order Offences", agg_crime="Major", population_weighted=False)
a.process()
b = a.crime.copy()
b["Total"] = b.iloc[:, 4:].sum(axis=1)
b["Ratio"] = b.iloc[:, -36:].mean(axis=1).values/b.iloc[:, 6:42].mean(axis=1).values
c = b.sort_values("Ratio", ascending=False)
d = c.loc[c["Ratio"] != np.inf]
d = d.loc[d["Total"] > 300]
d = d.dropna()

k = 2
for i in range(50):
    data = d.iloc[k*i:k*(i+1), :-2]
    print(d.iloc[k*i:k*(i+1), :])
    t = Time(data, output="Show", label_format='f"{borough} {lsoa}"')
    t.create_figure()
"""
