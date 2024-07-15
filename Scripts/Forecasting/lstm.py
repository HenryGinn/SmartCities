from sklearn.preprocessing import MinMaxScaler

from hgutilities import defaults
import numpy as np

from forecast import Forecast


class LSTM(Forecast):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        defaults.kwargs(self, kwargs)

    def preprocess_data(self):
        self.labels = self.data[self.look_back :]
        self.inputs = MinMaxScaler().fit_transform(self.data.reshape(-1, 1))
        self.set_look_back()

    def set_look_back(self):
        look_backed = np.zeros(
            (self.length - self.look_back + 1, self.look_back))
        for look_back in range(self.look_back):
            self.add_to_look_backed(look_backed, look_back)
        self.inputs = look_backed

    def add_to_look_backed(self, look_backed, look_back):
        start = look_back
        end = self.length + look_back - self.look_back + 1
        look_backed[:, look_back] = self.inputs[start : end].reshape(-1)


defaults.load(LSTM)
