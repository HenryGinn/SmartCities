import os

import matplotlib.pyplot as plt
import pandas as pd
from hgutilities import defaults
from hgutilities import utils
from hgutilities.utils import get_dict_string

from utils import get_time_columns


plt.rcParams["font.family"] = "Times New Roman"


class Time():

    def __init__(self, crime, **kwargs):
        defaults.kwargs(self, kwargs)
        self.crime = crime
        self.data = crime.crime

    def transpose(self):
        self.set_columns()
        self.population_weight_data()
        self.data = self.data.set_index(self.columns_non_time, drop=True)
        self.data = self.data.transpose()
        self.convert_to_date_datatype()

    def set_columns(self):
        self.columns = self.data.columns.values
        self.columns_time = get_time_columns(self.data)
        self.columns_non_time = list(set(self.columns) - set(self.columns_time))

    def population_weight_data(self):
        if self.population_weighted:
            pass
        self.data = self.data.drop(columns="Population")
        self.columns_non_time.remove("Population")

    def convert_to_date_datatype(self):
        self.data = self.data.reset_index()
        self.data = self.data.rename(columns={"index": "Time"})
        self.data["Time"] = pd.to_datetime(self.data["Time"], format="%Y %B")
        self.data = self.data.sort_values("Time")
        self.data = self.data.set_index("Time", drop=True)

    def plot(self):
        pass

defaults.load(Time)
