from crime import Crime
from plotter import Plotter

#crime = Crime(agg_time="Total", agg_spatial="Borough", agg_crime="Total", title="Total Crime in London")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London\nby LSOA Region")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Croydon", title="Total Crime in Croydon")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Westminster", title="Total Crime in Westminster")
#crime = Crime(agg_time="Total", lsoa="E01035716", title="Total Crime around Regents Street")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London by LSOA Region")

#crime.plot(save=True, log=True)

plotter = Plotter()
plotter.generate(region="Borough")
