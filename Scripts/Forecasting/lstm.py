from os.path import join, dirname
from random import seed as random_seed

from hgutilities import defaults
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import tf.random.set_seed as tf_seed
from keras.models import Sequential
from keras.layers import LSTM as LSTM_Layer
from keras.layers import Dense as Dense
from keras.layers import Lambda as Lambda
from keras.models import model_from_json

from model import Model


random_seed(9)
tf_seed(9)
np.random.seed(9)


class LSTM(Model):

    model_type = "LSTM"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        defaults.kwargs(self, kwargs)

    def set_model_files_paths(self):
        self.path_model_config = join(
            self.path_model, "LSTM Config.json")
        self.set_path_model_weights_all()

    def set_path_model_weights_all(self):
        self.set_path_model_weights("train")
        self.set_path_model_weights("validate")
        self.set_path_model_weights("test")

    def set_path_model_weights(self, fit_category):
        name = f"Case_{self.case}_{fit_category}.weights.h5"
        attribute = f"path_model_weights_{fit_category}"
        setattr(self, attribute, join(self.path_model, name))
        

    def set_inputs_and_labels(self):
        self.labels = self.data[self.look_back :]
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
        look_backed[:, look_back] = self.data[start : end].reshape(-1)

    def set_splits(self):
        self.set_split_points()
        self.set_iterable_splits("labels", look_back=True)
        self.set_iterable_splits("inputs", look_back=True)
        self.reshape_inputs()

    def reshape_inputs(self):
        self.inputs_train    = self.reshape_training_data(self.inputs_train)
        self.inputs_validate = self.reshape_training_data(self.inputs_validate)
        self.inputs_test     = self.reshape_training_data(self.inputs_test)

    def reshape_training_data(self, iterable):
        x, y = iterable.shape
        iterable = iterable.reshape(x, 1, y)
        return iterable

    def create_model(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.model = Sequential()
        self.model.add(LSTM_Layer(self.units))
        self.model.add(Dense(1))
        self.model.compile(loss=self.loss, optimizer=self.optimizer)

    def load(self):
        self.load_model()
        self.load_weights()

    def load_model(self):
        with open(self.path_model_config, "r") as file:
            file_contents = file.read()
        self.model = model_from_json(file_contents)

    def load_weights(self):
        path = getattr(self, f"path_model_weights_{self.fit_category}")
        self.model.load_weights(path)

    def save(self):
        self.save_model()
        self.save_weights()

    def save_model(self):
        file_contents = self.model.to_json(indent=4)
        with open(self.path_model_config, "w+") as file:
            file.write(file_contents)

    def save_weights(self):
        path = getattr(self, f"path_model_weights_{self.fit_category}")
        self.model.save_weights(path)

    def fit(self, **kwargs):
        defaults.kwargs(self, kwargs)
        inputs = self.get_fitting_data("inputs")
        labels = self.get_fitting_data("labels")
        self.model.fit(inputs, labels, epochs=self.epochs,
                       batch_size=self.batch_size, verbose=self.verbose)

    def predict(self):
        inputs = self.initialise_prediction()
        for index in range(self.length_forecast - self.look_back):
            inputs = self.predict_one_step(inputs, index)

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


defaults.load(LSTM)
