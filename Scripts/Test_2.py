import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Create a sample datetime index and series
dates = pd.date_range(start="2010-01-01", end="2024-01-01", freq="M")
data = range(len(dates))
series = pd.Series(data, index=dates)

# Plotting using pandas' built-in plot
ax = series.plot()

# Set major ticks to every 2 years starting from the first even year in the range
ax.xaxis.set_major_locator(mdates.YearLocator(base=2, month=1, day=1))

# Set the formatter to display the year only
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Rotate labels if needed
plt.xticks(rotation=45)

plt.show()
