########################################
# Base data preprocessing Class Object
#
#
#
########################################


# imports
import sys
import os
import json

import pandas as pd
import numpy as np


class Base_data_preprocessing:
    """
    Base data preprocessing object
    """
    # general att
    directory_path = './../data/'
    directory_path_processed = directory_path + '/processed_files/'

    # init
    def __init__(self, data_path):
        """

        :param data_path: csv path
        """

        # key_infomration
        self.label_data = None
        self.label_name = None
        self.features_data = None
        self.features_name = None
        self.columns_names = None

        # column transformation log
        # to be used to transform the data to be evelauated
        self.feature_transformation_log = {}

        print('loading data ...')
        # loading to pandas
        self.df = pd.read_csv(data_path)
        self.columns_names = list(self.df.columns)

        print('data set in loaded ...')

        # checking and handeling missing values

        num_of_null = self.df.isna().sum().sum()
        print(f'There are {num_of_null} null value in the data frames')
        if num_of_null == 0:
            print(f'No imputation is needed')
        else:
            # stop if there are missing values. will add a missing handeling machanisim in the future
            print(f'Imputation is needed, the data handling might not work. Model requires a clean data set')
            sys.exit()

        # handeling the label column
        self.handel_label_column()



        # the column of the label was drop so the rest of the data is feature data
        self.features_name = list(self.df.columns)
        # handeling feature columns
        for col in self.features_name:
            self.feature_transformation_log[col] = {}

        # setting the numeric columns
        self.numeric_columns = self.find_features_with_type('numeric')
        self.add_columns_type_to_metadata(self.numeric_columns, 'numeric')
        # setting bool columns
        self.bool_columns = self.find_features_with_type('bool')
        self.add_columns_type_to_metadata(self.bool_columns, 'bool')
        # setting string columns
        self.string_columns = self.find_features_with_type('string')
        self.add_columns_type_to_metadata(self.string_columns, 'string')

        print(self.feature_transformation_log)

        # normalizing the numeric columns
        print(f'normalizing numeric columns: {self.numeric_columns}')
        for col in self.numeric_columns:
            self.normalize_and_cast_to_float(col)

        # normalizing the bool columns there are any
        if len(self.bool_columns) > 0:
            print(f'normalizing bool columns: {self.bool_columns}')
        else:
            print('there are no bool columns moving on')

        print(self.feature_transformation_log)

        # handeling string columns
        # by asking for user input

        self.num_of_string_columns = len(self.string_columns)
        print(f'there are {self.num_of_string_columns} string columns in the data-set')
        if self.num_of_string_columns == 0:
            print('nothing to handel will move on')
        else:
            print('will have to handel it')
        self.handel_string_columns()

        # set the feature_data as the new data frame after the treament and the droping of the label column
        self.features_data = self.df

        print(self.feature_transformation_log)

        print(self.label_name, self.label_data)

        print(self.features_name, self.features_data)

        # seving the processed file
        self.save_prepossed_dataset()
        print('prepossessing is done')

    # meta data functions

    def add_columns_type_to_metadata(self, lst_columns, type):
        """
        :param type
        :param lst_columns:
        :return:
        """
        for col_name in lst_columns:
            self.feature_transformation_log[col_name]['type'] = type

    def add_max_min_to_metadata(self, col, max, min):
        """

        :param lst_columns:
        :return:
        """
        self.feature_transformation_log[col]['max'] = str(max)
        self.feature_transformation_log[col]['min'] = str(min)

    def add_string_metadata(self, col, string_dict, dict_values):
        """

        :param col:
        :return:
        """
        self.feature_transformation_log[col][string_dict] = dict_values

    #### general functions

    def find_features_with_type(self, col_type):
        """

        :param col_type: can be numeric, string or bool
        :return: list of columns with needed types
        """
        types_to_look = None
        columns_with_type = []

        if col_type == 'numeric':
            types_to_look = ['float64', 'int64']
        elif col_type == 'string':
            types_to_look = ['object']
        elif col_type == 'bool':
            types_to_look = ['bool']
        else:
            print(f'{col_type} is not supported')
        for col in self.df.columns:
            if self.df[col].dtype in types_to_look:
                columns_with_type.append(col)
        return columns_with_type

    def save_prepossed_dataset(self):
        """

        :return:
        """
        data_dir_name = input('please enter name for the dirctory the trasformed_dataset will be saved: ')
        # enter later avlidation mach that the names are not allready exsit
        path = self.directory_path_processed + data_dir_name
        os.mkdir(path)
        print(f'saving to: {path}')
        # saving label dat
        self.label_data.to_csv(path + "/label.csv", index=False, header=False)
        # saving features data
        self.features_data.to_csv(path + "/features.csv", index=False, header=False)
        #
        with open(path + '/metadata.json', 'w') as json_file:
            json.dump(self.feature_transformation_log, json_file)

    def handel_label_column(self):
        """
        asking the user to name the label column and returing the data handeled as a float32 var, and dropping the columns for the data Frame
        :return:
        """
        # reset the label column name
        self.label_name = None
        print('these are the columns names in the dataset:')
        for col in self.columns_names:
            print(col)
        self.label_name = input('please enter the label columns: ')
        # check if columns in DataFrame
        if self.label_name in self.columns_names and self.label_name is not None:
            print(f'{self.label_name} is in dataset')
        else:
            print('not a valid columns name')
            self.handel_label_column()

        # check if columns is numeric
        if self.df[self.label_name].dtype in ['float64', 'int64', 'int32', 'float32', 'bool']:
            print(f'{self.label_name} is a valid numeric column')
            # in the future enter more checks to make sure it is the right kond of columns

            # cast as a float
            self.cast_as_float(self.label_name)
            # set as label and save as np array
            self.label_data = self.df[self.label_name]

            # drop the column form the dataset
            self.df.drop(columns=[self.label_name], inplace=True)


        else:
            print('something went wrong lets start again')
            self.handel_label_column()

    #### function for handeling missing values

    def handel_nan_values(self):
        pass

    #### function for numeric columns handeling

    def normalize_and_cast_to_float(self, col, float_dtype='32', is_train_data=False):
        """

        normalizng a column and re
        :param float_dtype
        :param col:
        :param is_train_data : if it is train data will add the infomration to datalog
        :return:
        """
        print(col)
        column_array = self.df[col].values
        max_value = column_array.max()
        min_value = column_array.min()
        delimiter = max_value - min_value
        transformed_array = (column_array - min_value) / delimiter

        self.df[col] = transformed_array
        self.cast_as_float(col, float_type=float_dtype)

        # if is train data save it in the medadata dict
        self.add_max_min_to_metadata(col=col, max=max_value, min=min_value)

    def cast_as_float(self, col, float_type='32'):
        """
        change colum as to float
        :param col: the col the turn in to a float
        :param float_type: kind of float, defult is 32 (the best one for DL) values can be only 16, 32 or 64
        :return: None
        """
        ## change it the try epect logic
        str_type = 'float' + float_type
        if float_type == '32' or float_type == '16' or float_type == '64':
            self.df[col] = self.df[col].astype(str_type)
        else:
            print('not a valid float type, enter 16, 32, or 64')

    ### function for handeling string columns

    def handel_string_columns(self):
        """
        handle the string columns with the help of the user
        :return:
        """
        valid_encoding = ['ordinal', 'one_hot']

        for col in self.string_columns:
            print(f'handeling {col}', '\n')
            print(f'{col} contains {len(self.df[col].value_counts())} different values they are:', '\n')
            print(self.df[col].value_counts(normalize=True), '\n')
            print(f'choose a way to encode the columns {col}')
            how_to_handel = input('enter one_hot for one-hot encoding \nenter ordinal for ordinal encoding \n$$$$:')
            how_to_handel = how_to_handel.lower()
            if how_to_handel not in valid_encoding:
                print('not a valid entry')
                how_to_handel = input(
                    f' choose a way to encode the {col} '
                    f'enter one_hot for one-hot encoding \nenter ordinal for order encoding \n$$$$:')
                how_to_handel = how_to_handel.lower()
            elif how_to_handel == 'one_hot':
                self.one_hot_encoding(col)
            elif how_to_handel == 'ordinal':
                self.ordinal_encoding(col)

    def ordinal_encoding(self, col):
        """

        :param col:
        :return:
        """
        column_values = self.df[col].copy().unique()
        print(f'ordenial encoding encoding {col}')
        print(f'these are {column_values}\nlet loop on them and set a numeric value for each one')
        # setting the new numeric value
        col_numeric_name = col + '_numeric'
        self.df[col_numeric_name] = 0.0
        ordinal_dict = {}
        for value in column_values:
            numeric_value = None
            while numeric_value == None:
                print(f'handeling {value} in {col}')
                numeric_value = input(f'enter a numeric value to replace **{value}**: ')
                try:
                    numeric_value = float(numeric_value)
                except ValueError:
                    numeric_value = input(f'no a valid input, only numeric values')
                    numeric_value = None
            # seting the values in the columns
            self.set_numeric_value_for_a_string(col, col_numeric_name, value, numeric_value)
            # adding key value to oridnal dict
            ordinal_dict[value] = str(numeric_value)
        # entering the values and the numeric values into the metadata
        self.add_string_metadata(col, 'ordinal_trasformtion', ordinal_dict)
        # cast at flloat32
        self.cast_as_float(col_numeric_name, float_type='32')

        # dropping the orginal column
        self.df.drop(columns=col, inplace=True)

        # entering the column to the feature name columns
        self.features_name.append(col_numeric_name)

    def set_numeric_value_for_a_string(self, orignal_col, numeric_col, value, numeric_value):
        """

        :param col: the column to change the values in
        :param value: the values to chnage the values
        :param numeric_value: numeric value to chnage the value into
        :return:
        """

        self.df.loc[self.df[orignal_col] == value, numeric_col] = numeric_value

    def one_hot_encoding(self, col):
        """
        one hot encode a string column and dropping the original
        :param col: name of column to one hot encode
        :return:
        """
        print(f'one hot encoding {col}')
        values_for_dict = list(self.df[col].unique())
        # making the dummies dataframe
        one_hot = pd.get_dummies(self.df[col])
        # dropping the orginal column
        self.df.drop(columns=col, inplace=True)
        print(f'making {one_hot.shape[1]} new bool column')
        # turing all the bool columns that where made in the dummies dataframe into float32
        for one_hot_col in one_hot.columns:
            one_hot[one_hot_col] = one_hot[one_hot_col].astype('float32')
        # adding the dummies dataframe to the original datafarme
        self.df = self.df.join(one_hot)
        # adding the values as a dict to the metadata
        self.add_string_metadata(col, 'one_hot_encoding', values_for_dict)

        print('done')
