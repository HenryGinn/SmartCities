from os.path import join, dirname

from sklearn.preprocessing import MinMaxScaler
from hgutilities import defaults, utils
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM as LSTM_Layer
from keras.layers import Dense as Dense
from keras.layers import Lambda as Lambda
from keras.models import model_from_json

from forecast import Forecast


class LSTM(Forecast):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        defaults.kwargs(self, kwargs)
        self.set_lstm_paths()

    def set_lstm_paths(self):
        self.path_model = join(
            self.path_output_base, "Models", f"Case_{self.case}", self.name)
        utils.make_folder(self.path_model)
        self.path_model_config = join(self.path_model, "Config.json")
        self.path_model_weights = join(self.path_model, f"Case_{self.case}.weights.h5")

    def preprocess_data(self):
        self.labels = self.data[self.look_back :]
        self.scaler = MinMaxScaler()
        self.inputs = self.scaler.fit_transform(self.data.reshape(-1, 1))
        self.set_look_back()

    def set_look_back(self):
        look_backed = np.zeros(
            (self.length - self.look_back + 1, self.look_back))
        for look_back in range(self.look_back):
            self.add_to_look_backed(look_backed, look_back)
        self.inputs = look_backed

    def add_to_look_backed(self, look_backed, look_back):
        start = look_back
        end = self.length + look_back - self.look_back + 1
        look_backed[:, look_back] = self.inputs[start : end].reshape(-1)

    def set_splits(self):
        super().set_split_points()
        self.set_iterable_splits("labels", look_back=True)
        self.set_iterable_splits("inputs", look_back=True)
        self.inputs_train = self.reshape_training_data(self.inputs_train)

    def reshape_training_data(self, iterable):
        x, y = iterable.shape
        iterable = iterable.reshape(x, 1, y)
        return iterable

    def create_model(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.model = Sequential()
        self.model.add(LSTM_Layer(self.units))
        self.model.add(Dense(1))
        #self.model.add(Lambda(lambda x : 1 - x[:, :, 0]))
        self.model.compile(loss=self.loss, optimizer=self.optimizer)

    def load(self):
        self.load_model()
        self.load_weights()

    def load_model(self):
        with open(self.path_model_config, "r") as file:
            file_contents = file.read()
        self.model = model_from_json(file_contents)

    def load_weights(self):
        self.model.load_weights(self.path_model_weights)

    def save(self):
        self.save_model()
        self.save_weights()

    def save_model(self):
        file_contents = self.model.to_json(indent=4)
        with open(self.path_model_config, "w+") as file:
            file.write(file_contents)
            

    def save_weights(self):
        self.model.save_weights(self.path_model_weights)

    def fit(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.model_fitted = True
        self.model.fit(self.inputs_train, self.labels_train, epochs=self.epochs,
                       batch_size=self.batch_size, verbose=self.verbose)

    def predict(self):
        inputs = self.initialise_prediction()
        for index in range(self.length_forecast - self.look_back):
            inputs = self.predict_one_step(inputs, index)
        self.postprocess_prediction()

    def initialise_prediction(self):
        inputs = self.inputs_train[0, :, :].reshape(1, 1, self.look_back)
        self.modelled = np.zeros(self.length_forecast)
        self.modelled[:self.look_back] = inputs.reshape(-1)
        return inputs

    def predict_one_step(self, inputs, index):
        forecast = self.model.predict(inputs, verbose=0).reshape(1, 1, 1)
        inputs = np.concatenate((inputs[:, :, 1:], forecast), axis=2)
        self.modelled[self.look_back + index] = forecast
        return inputs

    def postprocess_prediction(self):
        print(self.modelled)
        self.modelled = self.scaler.inverse_transform(
            self.modelled.reshape(-1, 1)).reshape(-1)


defaults.load(LSTM)
