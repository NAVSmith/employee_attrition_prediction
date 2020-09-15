########################################
# basic deep learning model
#
#
########################################
#

# imports
import tensorflow as tf

from split_data import Split_data
from tensorflow.keras import models, layers, regularizers, metrics


class Basic_dl_model:
    directory_path = './../data/'
    directory_path_processed = directory_path + 'processed_files/'
    def __init__(self, data_dir):
        """

           :param data_dir:
           """
        # source directory
        self.data_dir = self.directory_path_processed + data_dir + '/'

        # the tensors
        self.data_train = None
        self.data_validate = None

        #the model
        self.model = None
        self.model_weights = None

        #the history
        #self.history = None


        # calling
        # this must not be here if more them just one model is used
        raw_data = Split_data(data_dir)

        # turing data into tensors
        self.data_train, self.data_validate = self.turn_to_tensor_flow(raw_data)

        # building the net work

        self.create_neural_net_work()

        # training

        self.train_dl()

        # saving the model

        self.save_model()



        print('ready to be used')




    def turn_to_tensor_flow(self, raw_data):
        """

           :param raw_data:
           :return:
           """

        # turning the array to tensors
        print('transforming data to tensors')
        print('transforming training data')

        tensor_y_train = tf.convert_to_tensor(raw_data.y_train, dtype='float32')
        tensor_x_train = tf.convert_to_tensor(raw_data.x_train, dtype='float32')

        print('transforming validation data')
        tensor_y_val = tf.convert_to_tensor(raw_data.y_val, dtype='float32')
        tensor_x_val = tf.convert_to_tensor(raw_data.x_val, dtype='float32')

        del raw_data

        # makeing the tensorflow data
        data_train = tf.data.Dataset.from_tensor_slices((tensor_x_train, tensor_y_train)).cache()

        data_validate = tf.data.Dataset.from_tensor_slices((tensor_x_val, tensor_y_val)).cache()

        del tensor_y_train, tensor_x_train, tensor_y_val, tensor_x_val

        return data_train, data_validate


    def create_neural_net_work(self):
        """

        :return:
        """

        print('building DL network')
        self.model = models.Sequential()
        self.model.add(layers.Flatten(input_shape=(18, 1)))
        self.model.add(layers.Dense(18, activation='relu'))
        self.model.add(layers.Dense(9, activation='relu'))
        self.model.add(layers.Dense(1, activation='sigmoid'))
        self. model.summary()

        # Create a callback that saves the model's weights
        """
        self.model_weights = tf.keras.callbacks.ModelCheckpoint(filepath=self.data_dir,
                                                         save_best_only=True,
                                                         verbose=1)
                                                         
        """

        print('compliing the net work')
        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['accuracy'])

    def train_dl(self):
        """

        :return:
        """

        self.history = self.model.fit(self.data_train.shuffle(10000).batch(32),
                                      epochs=50,
                                      validation_data=self.data_validate.batch(32),
                                      )
                                    # callbacks=[self.model_weights]

    def save_model(self):
        """

        :return:
        """
        print(f'saving to model to {self.data_dir}')
        self.model.save(self.data_dir + 'my_model.h5')
