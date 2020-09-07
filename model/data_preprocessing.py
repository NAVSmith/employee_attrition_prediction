########################################
# Base data preprocessing Class Object
#
#
#
########################################


# imports
import sys

import pandas as pd
import numpy as np
from sklearn import preprocessing


class Base_data_preprocessing:
    """
    Base data preprocessing object
    """

    # init
    def __init__(self, data_path):
        """

        :param data_path: csv path
        """
        print('loading data ...')
        # loading to pandas
        self.df = pd.read_csv(data_path)

        print('data set in loaded ...')

        # checking and handeling missing values

        num_of_null = self.df.isna().sum().sum()
        print(f'There are {num_of_null} null value in the data frames')
        if num_of_null == 0:
            print(f'No imputation is needed')
        else:
            print(f'Imputation is needed, the data handeling might not work. Model requires a clean data set')
            sys.exit()




        # setting the numeric columns
        self.numeric_columns_1 = self.df.columns[:-5]
        self.numeric_columns = self.find_numeric_columns()
        print(self.numeric_columns_1)
        print(self.numeric_columns)

        # normalizing the numeric columns
        for col in self.numeric_columns:
            self.normalize_and_cast_to_float(col)

    # missing values

    def handel_nan_values(self):
        pass



    # numeric columns habdeling

    def find_numeric_columns(self):
        """

        :return: the numeric columns in in the dataframe
        """
        numeric_columns = []
        for col in self.df.columns:
            if self.df[col].dtype in ['float64', 'int64']:
                numeric_columns.append(col)
        return numeric_columns


    def normalize_and_cast_to_float(self, col, float_dtype='32'):
        """
        normalizng a column and re
        :param col:
        :return:
        """
        print(col)
        column_array = self.df[col].values
        max_value = column_array.max()
        min_value = column_array.min()
        delimiter = max_value - min_value
        transformed_array = (column_array - min_value) / delimiter
        print()
        self.df[col] = transformed_array
        self.cast_as_float(col, float_type=float_dtype)
 

    def cast_as_float(self, col, float_type='32'):
        """
        change colum as to float
        :param col: the col the turn in to a float
        :param float_type: kind of float, defult is 32 (the best one for DL) values can be only 16, 32 or 64
        :return: None
        """
        ## change it the try epect logic
        str_type = 'float'+float_type
        if float_type == '32' or float_type == '16' or float_type == '64':
            self.df[col] = self.df[col].astype(str_type)
        else :
            print('not a valid float type, enter 16, 32, or 64')

