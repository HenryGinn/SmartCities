from hgutilities import defaults, utils

from forecast import Forecast


class ARIMA(Forecast):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


defaults.load(ARIMA)
