import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA as Arima
from sklearn.model_selection import train_test_split

# Generate synthetic time series data
np.random.seed(42)
n = 100
time_series = np.cumsum(np.random.randn(n)) + 50  # Random walk data
data = pd.Series(time_series, index=pd.date_range(start='2020-01-01', periods=n, freq='D'))

# Split the data into training and validation sets
train_data, val_data = train_test_split(data, test_size=0.2, shuffle=False)

# Fit the ARIMA model on the training data
order = (5, 1, 0)  # ARIMA(p=5, d=1, q=0) for demonstration
model = Arima(train_data, order=order)
model_fit = model.fit()

# In-sample predictions for training data
in_sample_forecast = model_fit.get_prediction(start=train_data.index[0], end=train_data.index[-1])
in_sample_predicted_mean = in_sample_forecast.predicted_mean
in_sample_confidence_intervals = in_sample_forecast.conf_int()

# Out-of-sample predictions for validation data
out_of_sample_forecast = model_fit.get_forecast(steps=len(val_data))
out_of_sample_predicted_mean = out_of_sample_forecast.predicted_mean
out_of_sample_confidence_intervals = out_of_sample_forecast.conf_int()

# Plot the results
plt.figure(figsize=(12, 6))

# Plot training data
plt.plot(train_data, label='Training Data', color='blue')

# Plot in-sample predicted values
plt.plot(train_data.index[1:], in_sample_predicted_mean[1:], label='In-Sample Predicted', color='red')

# Plot in-sample confidence intervals
plt.fill_between(train_data.index[1:], 
                 in_sample_confidence_intervals.iloc[1:, 0], 
                 in_sample_confidence_intervals.iloc[1:, 1], 
                 color='red', alpha=0.3, label='In-Sample 95% Confidence Interval')

# Plot validation data
plt.plot(val_data.index, val_data, label='Validation Data', color='orange')

# Plot out-of-sample predicted values
plt.plot(val_data.index, out_of_sample_predicted_mean, label='Out-of-Sample Predicted', color='green')

# Plot out-of-sample confidence intervals
plt.fill_between(val_data.index, 
                 out_of_sample_confidence_intervals.iloc[:, 0], 
                 out_of_sample_confidence_intervals.iloc[:, 1], 
                 color='green', alpha=0.3, label='Out-of-Sample 95% Confidence Interval')

plt.title('ARIMA Model Predictions with Confidence Intervals on Training and Validation Data')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
