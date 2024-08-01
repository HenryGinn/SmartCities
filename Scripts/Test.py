import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from random import seed as random_seed
from tensorflow.random import set_seed as tf_seed

random_seed(9)
tf_seed(9)
np.random.seed(9)
os.environ['PYTHONHASHSEED'] = '0'
os.environ['TF_DETERMINISTIC_OPS'] = '1'

# Generate sine wave data
def generate_sine_wave(num_samples):
    x = np.linspace(0, 20, num_samples)
    y = np.sin(x)
    return y

# Prepare the data
def create_dataset(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 3
num_samples = 30
units = 20

data = generate_sine_wave(num_samples)
X, y = create_dataset(data, seq_length)
X = X.reshape((X.shape[0], X.shape[1], 1))

train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

model = Sequential()
model.add(LSTM(units, input_shape=(3, 1), return_sequences=True))
model.add(LSTM(units))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

history = model.fit(X_train, y_train, epochs=20, batch_size=1, verbose=0)
predictions = model.predict(X_train)

"""
plt.figure(figsize=(14, 5))
plt.plot(range(len(data)), data, label='True Data')
plt.plot(np.arange(train_size, train_size + len(predictions)) + seq_length, predictions, label='Predictions')
plt.legend()
plt.show()
"""
