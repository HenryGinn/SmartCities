from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Input


class Architecture():

    def __init__(self, dense_0, lstm_0, lstm_1, lstm_2, dense_1):
        self.dense_0 = dense_0
        self.lstm_0 = lstm_0
        self.lstm_1 = lstm_1
        self.lstm_2 = lstm_2
        self.dense_1 = dense_1

    def reset_model(self):
        self.set_name()
        self.model.set_model_paths()
        self.model.results_summary = []
        self.create_model()

    def set_name(self):
        self.model.folder_name = (
            f"D0_{self.dense_0}__L0_{self.lstm_0}"
            f"__L1_{self.lstm_1}__L2_{self.lstm_2}"
            f"__D1_{self.dense_1}")

    def create_model(self):
        self.model.model = Sequential()
        self.set_architecture()
        self.model.model.add(Dense(1))
        self.model.model.compile(loss=self.model.loss,
                                 optimizer=self.model.optimizer)

    def set_architecture(self):
        self.add_layer_dense(0)
        self.add_layer_lstm(0)
        self.add_layer_lstm(1)
        self.add_layer_lstm(2)
        self.add_layer_dense(1)

    def add_layer_dense(self, number):
        units = getattr(self, f"dense_{number}")
        if units is not False:
            self.model.model.add(Dense(units))

    def add_layer_lstm(self, number):
        units = getattr(self, f"lstm_{number}")
        if units is not False:
            self.model.model.add(LSTM(units, return_sequences=(number != 2)))
        
