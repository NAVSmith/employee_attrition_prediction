########################################
# split and transform data object
#
#
#
########################################

# imports
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

class Split_data:
    """
    first splitting the data to label and features
    then splitting to train and validate
    """
    directory_path = './../data/'
    directory_path_processed = directory_path + 'processed_files/'

    # init function

    def __init__(self, project_dir_name):
        """

        :param data_path:
        """
        # path
        self.path = self.directory_path_processed + project_dir_name + '/'

        # infomration about that data
        self.train_is_data_balanced = False

        # validate data
        self.x_val = None
        self.y_val = None

        # train data
        self.x_train = None
        self.y_train = None


        # loading the data
        raw_features, raw_label = self.load_data()

        # splitting the data
        self.spliting_the_data(raw_features, raw_label)
        # dumping the big files to make room in the ram
        del raw_features, raw_label

        # checking if data is balanced
        # not working at the time fix it in the future

        if not self.train_is_data_balanced:
            self.balance_train_data()

        print('x_val:' ,self.x_val,
              self.y_val, self.x_train, self.y_train)



        #self.check_if_data_is_balanced(raw_train_label)


    def load_data(self):

        print('load the data to be train')
        # file_name = input('please enter name of the data file: ')
        print(self.path)
        try:
            raw_label = np.genfromtxt(self.path + 'label.csv', delimiter=',' )
            print(raw_label[0])
            raw_features = np.genfromtxt(self.path + 'features.csv', delimiter=',')
            print(raw_features[0])
        except Exception as e:
            # make this more detailed
            print('something went wrong please enter a valid scv file form the processed_files directory')
            print(e)
        return raw_features, raw_label



    def spliting_the_data(self, features_data, label_data):
        """
        based splitting funtion build on it
        :return:
        """
        # using sklearn to split
        # seving the validate data into the class as it will no change
        print('spliting data')
        self.x_train_unblanced, self.x_val, self.y_train_unblanced, self.y_val = train_test_split(features_data,
                                                          label_data,
                                                          test_size=.2,
                                                          random_state=12)


    def check_if_data_is_balanced(self, labels_data):
        """

        :param labels_data:
        :return:
        """
        """
        #fix it if there time
        unique_val = list(np.unique(labels_data, return_counts=True))
        label_zero = zip(unique_val[0][0], unique_val[1][0])
        label_one = zip(unique_val[0][1], unique_val[1][1])
        print(label_zero, label_one)
        """
        pass


    def balance_train_data(self):
        # resampling the traninging data to change the balnce the data
        sm = SMOTE(random_state=12)
        self.x_train, self.y_train = sm.fit_sample(self.x_train_unblanced, self.y_train_unblanced)
        self.train_is_data_balanced = True
