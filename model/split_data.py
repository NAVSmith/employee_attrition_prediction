########################################
# split and transform data object
#
#
#
########################################

# imports
import sys

import pandas as pd
import numpy as np
from sklearn import preprocessing

class Split_data:
    """
    first splitting the data to label and features
    then splitting to train and validate
    """
    directory_path = './../data/'
    directory_path_processed = directory_path + '/processed_files/'

    # init function

    def __init__(self):
        """

        :param data_path:
        """
        print('load the data to be train')
        file_name = input('please enter name of the csv file: ')
        path = self.directory_path_processed + file_name + '.csv'
        try:
            data = np.genfromtxt(path, delimiter=',')
            print(data[0])
        except:
            print('something went wrong please enter a valid scv file form the processed_files directory')







