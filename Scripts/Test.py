import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Example data
data = {'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}
df = pd.DataFrame(data)

window_size = 11

# Apply the weighted moving average
df['centred_moving_average'] = df['values'].rolling(window=window_size, center=True, min_periods=1).mean()
a = df['values'].rolling(window=window_size, center=True, min_periods=1).mean()

print(len(df))
print(len(a))
df.plot()
plt.show()
