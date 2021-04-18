########################################
# object that transform the input according to given
# input according to the way the train data was transformed
#
########################################

# import

import json
import os
import itertools



class Transform_input:
    dir_path = './../data/processed_files/'

    def __init__(self, directory):
        print('loaded')
        # vars
        self.path = self.dir_path + directory

        self.json = None
        # meta data file contains the logic to be used to transform the data
        self.metadata = None
        self.metadata_keys = None

        # the user input
        self.user_input = None
        self.user_input_keys = None
        # the transformed user input
        self.transformed_user_input = []

        # init the class by
        # finding the metadata json file to be to be used to transform the data in the model dir
        self.find_metadata_json_in_dir()

    ### json functions

    def find_metadata_json_in_dir(self):
        """
        find and load the the metadata json file to be to be used to transform the data in the model dir
        :return:
        """
        # looking for the metadata json file
        metadata_file = [file for file in os.listdir(self.path) if file.endswith('metadata.json')][0]

        # load the metadata file
        self.metadata, self.metadata_keys = self.load_metadata_json(metadata_file)
        print('the content of the metadata file:', self.metadata)
        # changing the data to ascii from unicode
        #self.metadata_keys = [i.encode('ascii', 'ignore') for i in self.metadata_keys]
        print(self.metadata_keys)

    def load_metadata_json(self, file):
        """

        :param load_json:
        :return: themeta data as dict and it is keys
        """
        try:
            file_path = self.path + file
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data, data.keys()
        except Exception as e:
            print(e)

    def trun_json_to_ascii(self, dictionary):
        """

        :param dictionary: takes a dictionary and transforms it form unicode to ascii
        :return:
        """
        for key, value in dictionary.items():
            [elm.encode('ascii', 'ignore') for elm in key]
            if isinstance(value, dict):
                self.trun_json_to_ascii(value)
            elif isinstance(value, list):
                [elm.encode('ascii', 'ignore') for elm in value]
            else:
                dictionary[key] = value.encode('ascii', 'ignore')
        print(dictionary)

        ### transformation functions

    def transform(self, user_input):
        """
        transform_user_input_to_model_input
        :param user_input: json of the user input
        :return:
        """
        # recalbrate the the class user input and transformed input vars
        print('recalibrating input vars')
        self.user_input = None
        # the transformed user input
        self.transformed_user_input = []
        # set the user_input

        # check it is a dict
        assert isinstance(user_input, dict), "not a valid input please enter a dict like input"

        # set the input
        self.user_input = user_input
        self.user_input_keys = user_input.keys()
        # check if the input is full and coincides with the metadata
        print(len(list(set(self.user_input_keys) - set(self.metadata_keys))))
        assert (len(list(set(self.user_input_keys) - set(
            self.metadata_keys))) == 0), 'Input does not coincides with metadate of input'

        # iterate over the user input solving each row acoording to the logic
        print(self.user_input_keys)
        for input_key in self.user_input_keys:
            # find the type on the input in the metadata
            input_type = self.metadata[input_key]['type']
            if input_type == 'numeric':
                transformed_value = self.transform_numeric(input_key)
            elif input_type == 'string':
                transformed_value = self.transform_string(input_key)
            elif input_type == 'bool':
                transformed_value = self.transform_bool(input_key)
            # append it to the transformed_user array
            try:
                if isinstance(transformed_value, list):
                    self.transformed_user_input.extend(transformed_value)
                else:
                    self.transformed_user_input.append(transformed_value)
            except Exception as e:
                print(e)
        print(self.transformed_user_input)

    def transform_numeric(self, input_key):
        """
        normalize the user input into a 0 to 1 number according to the trained data-set
        :param input_key: the input
        :return:normalized input between 0 and 1
        """
        # extract the relevant input
        input_value = float(self.user_input[input_key])
        # extract the normalization data
        print('input transform', input_key, ':',  self.user_input[input_key])
        max_value = float(self.metadata[input_key]['max'])
        min_value = float(self.metadata[input_key]['min'])
        print('parameters to use: ', max_value, min_value)
        delimiter = max_value - min_value
        # if the user input is between 1 and 100 but original data it is between 0.01 and 1 divide by 100
        # if not stay as it is
        if (input_value >= 1) and (min_value < 1):
            input_value = input_value / 100
        # in the cases where input values are larger the max value in model or smaller than min value the model trained on
        # set the value to min or max of the trained data-set.
        if input_value > max_value:
            input_value = max_value
        elif input_value < min_value:
            input_value = min_value
        # normalize the input
        normalized_input = (input_value - min_value) / delimiter
        print('transformted value', normalized_input)
        return normalized_input

    def transform_bool(self, input_key):
        """
        transformed bool yes or no entries to 0 or 1
        :param input_key:
        :return: 0 for on and 1 for yes
        """
        # extract the relevant input
        input_value = str(self.user_input[input_key]).lower()
        print('input transform', input_key, ':', self.user_input[input_key])
        if input_value == 'no':
            transformed_value = 0.0
        elif input_value == 'yes':
            transformed_value = 1.0
        else:
            print('transforming bool failed')
        print(transformed_value)
        return transformed_value

    def transform_string(self, input_key):
        """
        transformed strings to number between 0 and 1 if ordinal and to an array of one 1
        and several 0's if ine hot encoded
        :param input_key: input key
        :return: array of float or float
        """
        # retriving the string value
        input_value = str(self.user_input[input_key])
        # looking for kind of string transformation performed
        string_keys = self.metadata[input_key].keys()
        if 'ordinal_trasformtion' in string_keys:
            transformed_numeric_value = self.ordinal_trasformtion_string(input_key, input_value)
        elif 'one_hot_encoding' in string_keys:
            transformed_numeric_value = self.one_hot_encoding_trasformtion_string(input_key, input_value)
        else:
            print('no wax to resolve string input, and transformed it into number')
            raise ValueError('could not find a way to transformed string to numeric value: '
                             'option are ordinal_trasformtion or one_hot_encoding')
        return transformed_numeric_value

    def ordinal_trasformtion_string(self, input_key, input_value):
        """

        :param input_key:
        :return:
        """
        # extracting the transformation logic
        trans_logic_dict = self.metadata[input_key]['ordinal_trasformtion']
        # searching for the input_value in the keys in trans_logic_dict and replacing it with the coinciding numeric value
        try:
            transformed_numeric_value = trans_logic_dict[input_value]
            return float(transformed_numeric_value)
        except KeyError:
            print('KeyError: wrong value was entered')



    def one_hot_encoding_trasformtion_string(self, input_key, input_value):
        """

        :param input_key:
        :return:
        """
        # extracting the transformation logic
        trans_logic_list = [elm.encode('ascii', 'ignore') for elm in self.metadata[input_key]['one_hot_encoding']]
        if input_value in trans_logic_list:
            array = [1.0 if elm == input_value else 0 for elm in trans_logic_list]
            print(array)
        else:
            raise ValueError(input_value, 'is not a valid input')
        return array



if __name__ == '__main__':
    example_input = {"satisfaction": 67, "evaluation": 92, "number_of_projects": 4, "average_montly_hours": 261,
                     "time_spend_company": 5, "work_accident": 'no', "promotion": 'no', "department": "hr",
                     "salary": "medium"}
    troll_input = 'troll'
    #trans = Transform_input('test/')
    # unicode_dict = {u'salary': {u'ordinal_trasformtion': {u'high': u'1.0', u'medium': u'0.5', u'low': u'0.0'}, u'type': u'string'}, u'number_of_projects': {u'max': u'7', u'type': u'numeric', u'min': u'2'}, u'work_accident': {u'max': u'1', u'type': u'numeric', u'min': u'0'}, u'evaluation': {u'max': u'1.0', u'type': u'numeric', u'min': u'0.36'}, u'average_montly_hours': {u'max': u'310', u'type': u'numeric', u'min': u'96'}, u'satisfaction': {u'max': u'1.0', u'type': u'numeric', u'min': u'0.09'}, u'department': {u'one_hot_encoding': [u'sales', u'accounting', u'hr', u'technical', u'support', u'management', u'IT', u'product_mng', u'marketing', u'RandD'], u'type': u'string'}, u'promotion': {u'max': u'1', u'type': u'numeric', u'min': u'0'}, u'time_spend_company': {u'max': u'10', u'type': u'numeric', u'min': u'2'}}
    # transform.load_json('metadata.json')
    #trans.transform(example_input)
    # trans.trun_json_to_ascii(unicode_dict)
    for i in example_input.iterkeys():
        print(i)
