"""
This script determines if an LSOA region is interesting.

For each major crime category, the mean and standard deviation are found
across the time series. The regions with highest scores depending on some
metric are then output. This is done both overall and for each crime category.
"""


from crime import Crime

from utils import get_time_columns


class Interesting():

    def __init__(self):
        self.crime_obj = Crime()
        self.crime = self.crime_obj.crime
        self.major_categories = list(set(self.crime["Major Category"].values))
        self.initialise_scores_dataframe()

    def analyse(self):
        self.add_scores_basic()

    def initialise_scores_dataframe(self):
        self.time_columns = get_time_columns(self.crime)
        all_columns = self.crime.columns.values
        self.non_time_columns = [column for column in all_columns
                                 if column not in self.time_columns]
        self.data = self.crime[self.time_columns]
        self.scores = self.crime.loc[:, self.non_time_columns].copy()

    def add_scores_basic(self):
        self.scores.loc[:, "Mean"] = self.data.mean(axis=1)
        self.scores.loc[:, "Standard Deviation"] = self.data.std(axis=1)
        self.scores.loc[:, "Normalised Deviation"] = (
            self.scores["Mean"] / self.scores["Standard Deviation"])

    def output(self, n=10, measure=None):
        if measure is None:
            self.process_measure(self.output, n=n)
        else:
            self.output_overall(measure=measure, n=n)
            for category in self.major_categories:
                self.output_category(category, measure=measure, n=n)

    def process_measure(self, function, *args, **kwargs):
        measures = [column for column in self.scores.columns.values
                    if column not in self.non_time_columns]
        for measure in measures:
            function(measure=measure, *args, **kwargs)

    def output_overall(self, measure=None, n=10):
        if measure is None:
            self.process_measure(output_overall, self.scores)
        else:
            self.output_from_dataframe(measure, self.scores, n)

    def output_category(self, category, measure=None, n=10):
        if measure is None:
            self.process_measure(self.output_category, category)
        else:
            self.output_category_measure(measure, category, n)

    def output_category_measure(self, measure, category, n):
        scores_category = self.scores.loc[self.scores["Major Category"] == category]
        print(category, end="\t")
        self.output_from_dataframe(measure, scores_category, n)

    def output_from_dataframe(self, measure, scores, n):
        scores = scores.sort_values(by=measure, ascending=
        print(measure)
        print(scores.head(n).to_string())
        print("")


















