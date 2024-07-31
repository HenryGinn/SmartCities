import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Generate sine wave data
def generate_sine_wave(seq_length, num_samples):
    x = np.linspace(0, 50, num_samples)
    y = np.sin(x)
    return y

# Prepare the data
def create_dataset(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Parameters
seq_length = 4  # Length of the input sequence
num_samples = 200  # Total number of samples
units = 50  # Number of LSTM units

# Generate sine wave data
data = generate_sine_wave(seq_length, num_samples)

# Create dataset
X, y = create_dataset(data, seq_length)

# Reshape input to be [samples, time steps, features]
X = X.reshape((X.shape[0], X.shape[1], 1))

# Split the data into training and testing sets
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build the model
model = Sequential()
model.add(LSTM(units, input_shape=(seq_length, 1), return_sequences=True))
model.add(LSTM(units))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=1, validation_split=0.2, verbose=0)

# Make predictions
predictions = model.predict(X_test)

# Plot the results
plt.figure(figsize=(14, 5))
plt.plot(range(len(data)), data, label='True Data')
plt.plot(np.arange(train_size, train_size + len(predictions)) + seq_length, predictions, label='Predictions')
plt.legend()
plt.show()

# Plot training and validation loss
plt.figure(figsize=(14, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()
