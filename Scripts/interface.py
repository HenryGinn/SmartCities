from crime import Crime
from plotter import Plotter

#crime = Crime(agg_time="Total", agg_spatial="Borough", agg_crime="Total", title="Total Crime in London")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London\nby LSOA Region")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Croydon", title="Total Crime in Croydon")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Westminster", title="Total Crime in Westminster")
#crime = Crime(agg_time="Total", lsoa="E01035716", title="Total Crime around Regents Street")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London by LSOA Region")
#crime = Crime(agg_crime="Total", agg_spatial="Borough", borough="Westminster")
crime = Crime(agg_crime="Major", major="Theft", borough="Westminster")

crime.process()
crime.remove_major()
crime.plot(month="December", year=2010, output="show")

#crime.time()
#crime.time_plot(save=False, log=True)#, bbox_to_anchor=(0.5, 0.5), squish_vertical=0.35)

#plotter = Plotter()
#plotter.generate(absolute=False, boroughs=["Westminster"], categories_major=["Theft"], time="Full", animate=True, year=2020, region="Borough", dpi=300, format="png")

