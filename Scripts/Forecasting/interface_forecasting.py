import sys
import os
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt

from forecast import Forecast

forecast = Forecast()
forecast.create_forecast()

fig, ax = plt.subplots(1)
forecast.create_plot(fig, ax)
