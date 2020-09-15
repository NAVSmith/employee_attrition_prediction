########################################
# basic deep learning model
#
#
#
########################################

# imports
import tensorflow as tf

from split_data import Split_data
from tensorflow.keras import models, layers, regularizers, metrics


class Basic_dl_model:
    def __init__(self, data_dir):
        """

           :param data_dir:
           """
        # the tensors

        self.tensor_x_val = None
        self.tensor_y_val = None

        # train data
        self.tensor_x_train = None
        self.tensor_y_train = None

        # calling
        raw_data = Split_data(data_dir)

        # turing data into tensors
        self.turn_to_tensor_flow(raw_data)

        # makeing the tensorflow data
        data_train = tf.data.Dataset.from_tensor_slices((self.tensor_x_train, self.tensor_y_train)).cache()

        data_validate = tf.data.Dataset.from_tensor_slices((self.tensor_x_val, self.tensor_y_val)).cache()

        print('ready to train')

        model = models.Sequential()
        model.add(layers.Flatten(input_shape=(18, 1, 1)))
        model.add(layers.Dense(18, activation='relu'))
        model.add(layers.Dense(9, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        model.summary()

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        history = model.fit(data_train.shuffle(10000).batch(32), epochs=10, validation_data=data_validate.batch(32))


    def turn_to_tensor_flow(self, raw_data):
        """

           :param raw_data:
           :return:
           """
        # validate data
        """self.x_val = None
           self.y_val = None
           """

        # turning the array to tensors
        print('transforming data to tensors')
        print('transforming training data')
        print(type(raw_data.y_train))

        self.tensor_y_train = tf.convert_to_tensor(raw_data.y_train, dtype='float32')
        self.tensor_x_train = tf.convert_to_tensor(raw_data.x_train, dtype='float32')

        print('transforming validation data')
        self.tensor_y_val = tf.convert_to_tensor(raw_data.y_val, dtype='float32')
        self.tensor_x_val = tf.convert_to_tensor(raw_data.x_val, dtype='float32')

        del raw_data



