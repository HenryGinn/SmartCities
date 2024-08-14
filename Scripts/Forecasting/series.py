"""
Anything data before modelling is referred to as 'data'
Anything data after modelling is referred to as 'modelled'
All intermediate steps are stored in the time_series dataframe
In the dataframe all data will be labelled as 'Data{Label}',
'Modelled{Label}', or 'Residuals{Label}'.
"""


from os.path import join
from os.path import dirname
import warnings

import pandas as pd
import numpy as np
from hgutilities import defaults, utils

from utils import get_base_path


warnings.simplefilter(action='ignore', category=FutureWarning)


class Series():

    def __init__(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.load_time_series()
        self.set_split_indices()
        self.set_fit_category(self.fit_category)
        self.extend_dataframe()

    # Loading time series data
    def load_time_series(self):
        self.set_main_paths()
        path = join(self.path_data, f"Case_{self.case}.csv")
        self.read_data(path)
        self.read_metadata(path)

    def set_main_paths(self):
        self.path_base = get_base_path(self)
        self.path_data = join(self.path_base, "Data", "Forecast")
        self.path_output_base = join(self.path_base, "Output")

    def read_data(self, path):
        self.time_series = pd.read_csv(
            path, skiprows=3, index_col="Time", dtype=np.float32,
            date_format="%Y-%m-%d", parse_dates=True)

    def read_metadata(self, path):
        with open(path) as file:
            self.borough = self.extract_from_line(file)
            self.major   = self.extract_from_line(file)
            self.lsoa    = self.extract_from_line(file)

    def extract_from_line(self, file):
        metadata = file.readline().strip("\n").split(",")[1]
        return metadata


    # Facilitate the convenient indexing anywhere into a time series
    
    def set_split_indices(self):
        length = len(self.time_series)
        self.index_start    = 0
        self.index_train    = int(length * self.train) - 1
        self.index_validate = int(length * self.validate) + self.index_train
        self.index_test     = length - 1
        self.index_forecast = int(length * self.forecast) + self.index_test
        self.length = self.index_forecast + 1

    def i(self, start="start", stop="forecast", look_back=False):
        start_index = self.get_start_index(start, look_back)
        stop_index  = self.get_stop_index(stop, look_back)
        slice_obj = slice(start_index, stop_index)
        return slice_obj

    def get_start_index(self, start, look_back):
        return getattr(self, f"index_{start}")

    def get_stop_index(self, stop, look_back):
        offset = 0
        if look_back:
            offset = self.look_back - 1
        return getattr(self, f"index_{stop}") - offset


    # Allowing the dataframe to handle all series lengths

    def extend_dataframe(self):
        forecast_dates = self.get_forecast_dates()
        extended_data = self.get_extended_data()
        extended = pd.DataFrame(extended_data, index=forecast_dates)
        self.time_series = pd.concat([self.time_series, extended])

    def get_forecast_dates(self):
        original_end = self.time_series.index[len(self.time_series) - 1]
        additional_periods = self.length - self.index_test
        forecast_dates = pd.date_range(start=original_end, freq='MS',
                                       periods=additional_periods)[1:]
        return forecast_dates

    def get_extended_data(self):
        additional_rows = self.length - self.index_test - 1
        array_extension = np.array([None] * additional_rows)
        extended_data = {column: array_extension.copy()
                         for column in self.time_series.columns.values}
        return extended_data
    

    def add_column(self, values, name):
        extension = np.empty(self.length - values.size)*np.nan
        column = np.concatenate([values.reshape(-1), extension], axis=0)
        self.time_series.loc[:, name] = column.copy()

    def predict(self):
        self.modelled = np.zeros((self.self.length))

    def no_nan(self, value_type, stage=None):
        if stage is None:
            stage = self.stage
        values = self.time_series[f"{value_type}{stage}"]
        values = self.np_nan(values)
        return values

    def np_nan(self, values):
        values = values[~np.isnan(values)]
        return values

    def set_fit_category(self, fit_category):
        self.fit_category = fit_category
        self.set_forecast_category()
        self.slice = self.i("start", self.fit_category, look_back=True)
        self.slice_data = self.i("start", self.fit_category)
        self.slice_plot = self.i("start", self.forecast_category)
        self.slice_forecast = self.i(self.fit_category, self.forecast_category, look_back=True)
        if hasattr(self, "history_validate"):
            delattr(self, "history_validate")

    def set_forecast_category(self):
        match self.fit_category:
            case "train"   : self.forecast_category = "validate"
            case "validate": self.forecast_category = "test"
            case "test"    : self.forecast_category = "forecast"

        
defaults.load(Series)
