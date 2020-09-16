########################################
# object that transform the input according to given
# input according to the way the train data was transformed
#
########################################

# import

import json
import os


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
        self.metadata , self.metadata_keys  = self.load_metadata_json(metadata_file)
        print('the content of the metadat file:', self.metadata)

        # finding the keys

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
        
        # check if the input is full and coinsides with the metadata
        

        # iterate over the user information solving each row acoording to the logic

    def transform_numeric(self, key):
        pass

    def transform_bool(self, key):
        pass

    def transform_string(self, key):
        pass
    
    def check_if_input_match_meta_data(self):
        """
        
        :return: the error or a greenlight 
        """
        user_keys = self.user_input.keys()

        

if __name__ == '__main__':
    example_input = {"satisfaction":0.74,"evaluation":0.92,"number_of_projects":4,"average_montly_hours":261,"time_spend_company":5,"work_accident":0,"churn":1,"promotion":0,"department":"technical","salary":"medium"}
    troll_input = 'troll'
    trans = Transform_input('test/')
    # transform.load_json('metadata.json')
    trans.transform(example_input)
