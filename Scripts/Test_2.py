import math
import random

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import model_from_json


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

dataframe = read_csv('airline-passengers.csv', usecols=[1], engine='python')
dataset = dataframe.values
dataset = dataset.astype('float32')

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.6)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# reshape into X=t and Y=t+1
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


def create():
    model.add(LSTM(4))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=0)

def save():
    file_contents = model.to_json(indent=4)
    with open("Model.json", "w+") as file:
        file.write(file_contents)
    model.save_weights("AirPassengers.weights.h5")

def load():
    with open("Model.json", "r") as file:
        file_contents = file.read()
    model = model_from_json(file_contents)
    model.load_weights("AirPassengers.weights.h5")
    return model

# create and fit the LSTM network
#model = Sequential()
#create()
#save()
model = load()

time_steps = 30
last_sequence = trainX[:time_steps]
predictions = list(last_sequence[:, :, 0].reshape(-1))

for _ in range(30):
    input_sequence = last_sequence.reshape((1, -1, 1))
    predicted_value = model.predict(input_sequence, verbose=0)
    predictions.append(predicted_value[0, 0])
    last_sequence = np.append(last_sequence[:], predicted_value)

# invert predictions
predictions = scaler.inverse_transform([predictions]).reshape(-1)

# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(predictions, color="red")
plt.show()
