from crime import Crime
from plotter import Plotter
from interesting import Interesting


#crime = Crime(agg_time="Total", agg_spatial="Borough", agg_crime="Total", title="Total Crime in London")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London\nby LSOA Region")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Croydon", title="Total Crime in Croydon")
#crime = Crime(agg_time="Total", agg_crime="Total", borough="Westminster", title="Total Crime in Westminster")
#crime = Crime(agg_time="Total", lsoa="E01035716", title="Total Crime around Regents Street")
#crime = Crime(agg_time="Total", agg_crime="Total", title="Total Crime in London by LSOA Region")
#crime = Crime(agg_crime="Total", agg_spatial="Borough", borough="Westminster")
#crime = Crime(agg_crime="Major", major="Theft", borough="Westminster")

#crime.process()
#crime.remove_major()
#crime.plot(month="December", output="show")

#crime.time()
#crime.time_plot(save=False, log=True)#, bbox_to_anchor=(0.5, 0.5), squish_vertical=0.35)

#plotter = Plotter()
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

interesting = Interesting(figures=False, csv=True, series=False)
interesting.analyse()
interesting.output()
#interesting.output_category(measure="Mean", category="Theft")
