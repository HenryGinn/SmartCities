"""
This script determines if an LSOA region is interesting.

For each major crime category, the mean and standard deviation are found
across the time series. The regions with highest scores depending on some
metric are then output. This is done both overall and for each crime category.
"""


from os.path import join

from hgutilities import defaults, utils
import numpy as np
import pandas as pd

from crime import Crime
from plot import Plot
from timeseries import Time
from .utils import get_time_columns, add_line_breaks


class Interesting():

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        defaults.kwargs(self, kwargs)
        self.initialise_crime()
        self.initialise_scores_dataframe()
        self.set_paths()

    def initialise_crime(self):
        self.crime_obj = Crime(agg_crime="Major", keep_population_column=True)
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
        self.name = f"{name} - {measure}"
        self.measure = measure
        print(self.name)
        self.output_all(scores)

    def output_all(self, scores):
        self.output_csv(scores.head(self.n_csv))
        self.output_figure(scores.head(self.n_figure))
        self.output_time_series(scores.head(self.n_time))

    def output_csv(self, scores):
        if self.csv:
            path = join(self.path_csv, f"{self.name}.csv")
            scores.to_csv(path)

    def output_figure(self, scores):
        if self.figures:
            scores = scores.drop(columns=["Major Category"])
            self.crime_obj.crime = scores
            self.plot()

    def plot(self):
        self.plot_obj = Plot(
            self.crime_obj, path_output=self.path_figures, title=self.name,
            figure_name=self.name, plot_column=self.measure, **self.kwargs,
            population_weighted=False, colorbar_label="Score")
        self.plot_obj.plot()

    def output_time_series(self, scores):
        filtered = self.get_filtered_dataframe(scores)
        self.set_plot_peripherals()
        self.create_time_obj(filtered)
        self.time_obj.create_figure()

    def get_filtered_dataframe(self, scores):
        key = self.get_filtering_key(scores)
        crime_reindex = self.crime.set_index(key)
        scores = scores.set_index(key)
        filtered = crime_reindex.loc[scores.index, :].reset_index()
        return filtered

    def get_filtering_key(self, scores):
        potential_keys = ["LSOA", "Major Category"]
        columns = set(scores.columns.values)
        keys = list(set(potential_keys).intersection(columns))
        return keys

    def create_time_obj(self, filtered):
        self.time_obj = Time(filtered, output="Save", title=self.time_series_title,
                             label_format="f'{rank}: {crime} {lsoa}'",
                             y_label=self.time_series_y_label, name=self.name,
                             path_output=self.path_time)

    def set_plot_peripherals(self):
        self.set_time_series_y_label()
        self.set_title()

    def set_time_series_y_label(self):
        self.time_series_y_label = (
            f"Report Crimes per {self.crime_obj.per_n_people} People")

    def set_title(self):
        self.time_series_title = add_line_breaks(
            f"Interesting Candidates: {self.name}")
        


defaults.load(Interesting)















