from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


date_range = pd.date_range(start="2020-01-01", periods=24, freq="MS")
steps = np.random.normal(loc=0, scale=1, size=len(date_range))
random_walk = np.cumsum(steps)
df = pd.DataFrame(data={"RandomWalk": random_walk}, index=date_range)

a = auto_arima(df["RandomWalk"].values)

#forecaster = ARIMA(df["RandomWalk"], order=a.order, seasonal_order=a.seasonal_order)
forecaster = ARIMA(df["RandomWalk"].values, order=a.order, seasonal_order=a.seasonal_order)

b = forecaster.fit()
date_range = pd.date_range(start="2020-01-01", periods=36, freq="MS")
#pred = b.predict(start=date_range[0], end=date_range[-1])
pred = b.predict(start=6, end=36)
print(pred)

"""
i = df.index[-1]

fig, ax = plt.subplots(1)
ax.plot(df, color="purple")
ax.plot(pred, color="green")
ax.plot([i, i], [-3, 3], color="gray")

plt.show()
"""
