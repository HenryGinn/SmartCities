import sys
import os
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

import matplotlib.pyplot as plt

from forecast import Forecast

forecast = Forecast()
forecast.create_forecast()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_axes([0.12, 0.12, 0.8, 0.72])
forecast.create_plot(fig, ax, output="save", legend_bbox_to_anchor=(0.13, 0.8), loc=10,
                     title="Modelling Arson and Criminal\nDamage in E01004734")
