import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Example time series data
time_series = np.random.randn(100)

# Compute autocorrelation
acf_values = sm.tsa.acf(time_series, nlags=20)
acf_values = sm.tsa.pacf(time_series, nlags=20)

# Plot autocorrelation
sm.graphics.tsa.plot_pacf(time_series, lags=20)
plt.show()
