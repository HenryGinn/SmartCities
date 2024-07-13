from os.path import join

import pandas as pd
from hgutilities import defaults

from utils import get_base_path


class Forecast():

    def __init__(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_paths()
        self.load_time_series()
        print(self.borough, self.major, self.lsoa)
        print(self.data)

    def set_paths(self):
        self.path_base = get_base_path(self)
        self.path_data = join(self.path_base, "Data", "Forecast")
        self.path_output_base = join(self.path_base, "Output")

    def load_time_series(self):
        path = join(self.path_data, f"Case_{self.case}.csv")
        self.read_data(path)
        self.read_metadata(path)

    def read_data(self, path):
        self.data = pd.read_csv(
            path, skiprows=3, index_col="Time",
            date_format="%Y-%m-%d", parse_dates=True)

    def read_metadata(self, path):
        with open(path) as file:
            self.borough = self.extract_from_line(file)
            self.major   = self.extract_from_line(file)
            self.lsoa    = self.extract_from_line(file)

    def extract_from_line(self, file):
        metadata = file.readline().strip("\n").split(",")[1]
        return metadata

defaults.load(Forecast)
