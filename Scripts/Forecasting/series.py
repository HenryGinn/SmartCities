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
        self.length = len(self.data)
        self.set_split_points()

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
        self.path_output_forecast = join(
            self.path_output_base, "Forecasting", f"Case_{self.case}")
        utils.make_folder(self.path_output_forecast)

    def read_data(self, path):
        self.time_series = pd.read_csv(
            path, skiprows=3, index_col="Time", dtype=np.float32,
            date_format="%Y-%m-%d", parse_dates=True)
        self.data = self.time_series["DataOriginal"].values

    def read_metadata(self, path):
        with open(path) as file:
            self.borough = self.extract_from_line(file)
            self.major   = self.extract_from_line(file)
            self.lsoa    = self.extract_from_line(file)

    def extract_from_line(self, file):
        metadata = file.readline().strip("\n").split(",")[1]
        return metadata

    # Processing time series data
    def extend_dataframe(self):
        if len(self.time_series) == self.length:
            self.do_extend_dataframe()

    def do_extend_dataframe(self):
        forecast_dates = self.get_forecast_dates()
        extended_data = self.get_extended_data()
        extended = pd.DataFrame(extended_data, index=forecast_dates)
        self.time_series = pd.concat([self.time_series, extended])

    def get_forecast_dates(self):
        original_end = self.time_series.index[self.length - 1]
        forecast_dates = pd.date_range(start=original_end, freq='MS',
                                       periods=self.forecast_length + 1)[1:]
        return forecast_dates

    def get_extended_data(self):
        array_extension = np.array([None] * self.forecast_length)
        extended_data = {column: array_extension.copy()
                         for column in self.time_series.columns.values}
        return extended_data

    def add_column(self, values, name):
        extension = np.empty(self.length_forecast - values.size)*np.nan
        column = np.concatenate([values.reshape(-1), extension], axis=0)
        self.time_series.loc[:, name] = column


    # Defining the train, validate, and test data
    def set_split_points(self):
        self.set_split_index_points()
        self.set_split_indices()

    def set_split_index_points(self):
        self.index_train    = int(self.length * self.train)
        self.index_validate = int(self.length * self.validate) + self.index_train
        self.length_forecast = int(self.length * self.forecast) + self.length
        self.forecast_length = self.length_forecast - self.length

    def set_split_indices(self):
        self.slice_train    = slice(0, self.index_train)
        self.slice_validate = slice(self.index_train, self.index_validate)
        self.slice_test     = slice(self.index_validate, self.length)
        self.slice_forecast = slice(self.length, self.length_forecast)

    def set_iterable_splits(self, attribute, look_back=False):
        self.set_iterable_split(attribute, "train", look_back)
        self.set_iterable_split(attribute, "validate", look_back)
        self.set_iterable_split(attribute, "test", look_back)

    def set_iterable_split(self, attribute, split, look_back):
        iterable = getattr(self, attribute)
        other_dimensions = ((len(iterable.shape) - 1) * [slice(None)])
        slice_first = self.get_slice_first(split, look_back)
        slice_all = [slice_first, *other_dimensions]
        setattr(self, f"{attribute}_{split}", iterable[*slice_all])

    def get_slice_first(self, split, look_back):
        base_slice = getattr(self, f"slice_{split}")
        if look_back:
            return self.get_slice_first_look_back(base_slice, split)
        else:
            return base_slice

    def get_slice_first_look_back(self, base_slice, split):
        if split == "train":
            return slice(base_slice.start,
                         base_slice.stop - self.look_back + 1)
        else:
            return slice(base_slice.start - self.look_back + 1,
                         base_slice.stop - self.look_back + 1)

    def get_fitting_data(self, attribute):
        match self.fit_category:
            case "train"   : return self.get_fitting_data_train(attribute)
            case "validate": return self.get_fitting_data_validate(attribute)
            case "test"    : return self.get_fitting_data_test(attribute)

    def get_fitting_data_train(self, attribute):
        fitting_data = getattr(self, f"{attribute}_train")
        return fitting_data

    def get_fitting_data_validate(self, attribute):
        fitting_data = np.concatenate((
            getattr(self, f"{attribute}_train"),
            getattr(self, f"{attribute}_validate")))
        return fitting_data

    def get_fitting_data_test(self, attribute):
        fitting_data = np.concatenate((
            getattr(self, f"{attribute}_train"),
            getattr(self, f"{attribute}_validate"),
            getattr(self, f"{attribute}_test")))
        return fitting_data

    def predict(self):
        self.modelled = np.zeros((self.length_forecast))

    def no_nan(self, value_type, stage=None):
        if stage is None:
            stage = self.stage
        values = self.time_series[f"{value_type}{stage}"]
        values = values[~np.isnan(values)]
        return values

        
defaults.load(Series)
