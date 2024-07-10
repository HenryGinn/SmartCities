"""
This script determines if an LSOA region is interesting.

For each major crime category, the mean and standard deviation are found
across the time series. The regions with highest scores depending on some
metric are then output. This is done both overall and for each crime category.
"""


from os.path import join

from hgutilities import utils
from hgutilities import defaults
import numpy as np
import pandas as pd

from crime import Crime
from plot import Plot
from utils import get_time_columns
from timeseries import Time


class Interesting():

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.initialise_crime()
        self.initialise_scores_dataframe()
        self.set_paths()

    def initialise_crime(self):
        self.crime_obj = Crime(agg_crime="Major")
        self.crime_obj.process()
        self.crime = self.crime_obj.crime
        self.major_categories = list(set(self.crime["Major Category"].values))

    def set_paths(self):
        self.path_base = join(self.crime_obj.path_output_base, "Interesting")
        self.set_paths_csv()
        self.set_paths_figures()
        self.set_paths_time()

    def set_paths_csv(self):
        self.path_csv = join(self.path_base, "Text")
        utils.make_folder(self.path_csv)

    def set_paths_figures(self):
        self.path_figures = join(self.path_base, "Figures")
        utils.make_folder(self.path_figures)

    def set_paths_time(self):
        self.path_time = join(self.path_base, "Time Series")
        utils.make_folder(self.path_time)

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
        self.scores.loc[:, "Mean"] = self.data.mean(axis=1).round(1)
        self.scores.loc[:, "Standard Deviation"] = self.data.std(axis=1).round(1)
        self.scores.loc[:, "Normalised Deviation"] = (
            self.scores["Mean"] / self.scores["Standard Deviation"]).round(2)

    def output(self, measure=None):
        if measure is None:
            self.process_measure(self.output)
        else:
            self.output_measure(measure)

    def output_measure(self, measure):
        self.output_overall(measure=measure)
        for category in self.major_categories:
            self.output_category(category, measure=measure)

    def process_measure(self, function, *args, **kwargs):
        measures = [column for column in self.scores.columns.values
                    if column not in self.non_time_columns]
        for measure in measures:
            function(measure=measure, *args, **kwargs)

    def output_overall(self, measure=None):
        if measure is None:
            self.process_measure(output_overall, self.scores)
        else:
            self.output_from_dataframe(measure, self.scores, "Overall")

    def output_category(self, category, measure=None):
        if measure is None:
            self.process_measure(self.output_category, category)
        else:
            self.output_category_measure(measure, category)

    def output_category_measure(self, measure, category):
        scores_category = self.scores.loc[self.scores["Major Category"] == category]
        self.output_from_dataframe(measure, scores_category, category)

    def output_from_dataframe(self, measure, scores, name):
        scores = scores.sort_values(by=measure, ascending=False).copy()
        name = f"{name}: {measure}"
        print(name)
        self.output_all(measure, scores, name)

    def output_all(self, measure, scores, name):
        self.output_csv(scores.head(self.n_csv), name, measure)
        self.output_figure(scores.head(self.n_figure), name, measure)
        self.output_time_series(scores.head(self.n_time), name, measure)

    def output_csv(self, scores, name, measure):
        if self.csv:
            path = join(self.path_csv, f"{name}.csv")
            scores.to_csv(path)

    def output_figure(self, scores, name, measure):
        if self.figures:
            scores = scores.drop(columns=["Major Category"])
            self.crime_obj.crime = scores
            self.plot(name, measure)

    def plot(self, name, measure):
        self.plot_obj = Plot(
            self.crime_obj, path_output=self.path_figures,
            title=name, figure_name=name, plot_column=measure, **self.kwargs,
            population_weighted=False, colorbar_label="Score")
        self.plot_obj.plot()

    def output_time_series(self, scores, name, measure):
        filtered = self.get_filtered_dataframe(scores)
        self.time_obj = Time(filtered, output="Show")
        self.time_obj.create_figure()

    def get_filtered_dataframe(self, scores):
        filtered = self.crime[self.crime["LSOA"].isin(scores["LSOA"])]
        if "Major Category" in scores.columns.values:
            filtered = filtered[filtered["Major Category"].isin(
                scores["Major Category"])]
        return filtered


defaults.load(Interesting)















