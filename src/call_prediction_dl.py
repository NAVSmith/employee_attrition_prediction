########################################
# object that use the model to make prediction
# the
#
########################################

#imports
import tensorflow as tf

class Predict:
    """

    """
    # vars
    path = '../data/processed_files'

    def __init__(self, model_to_use, data_to_predict):
        """

        :param model_to_use: path to the h5 model file
        :param data_to_predict:
        """
        # vars
        self.data_evalute = None
        self.array_to_evaluate = None

        # model to use
        self.model = model_to_use


        # input shape
        self.tensor_shape = [1, 18]

        self.array_to_evaluate = self.turn_data_to_tensor(data_to_predict)

        self.risk_output = self.predict_churn_prob(self.model, self.array_to_evaluate)

    def turn_data_to_tensor(self, array_to_change):
        """

        :return:
        """

        try:
            # making the array into a tensor
            arr = tf.convert_to_tensor(array_to_change, dtype='float32')
            #  reshaping to the right shape to be feed to the model
            array_to_evaluate = tf.reshape(arr, self.tensor_shape)

        except Exception as e:
            print('something went wrong while trying to covert the data to tensor')
            print(e)

        return array_to_evaluate

    def predict_churn_prob(self, model, tensor_array):
        """

        :param model:
        :param tensor_array:
        :return:
        """
        print('calculating probabilty of churn')
        result = model.predict(tensor_array)[0][0]
        print(f'the rist the eemploy is going to leave is {result}')
        return result

if __name__ == '__main__':
    data = [0.35164836,0.265625,0.0,0.28504673,0.125,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0]
    model = tf.keras.models.load_model('../data/processed_files' + '/test/' + 'my_model.h5')
    Predict(model , data)






