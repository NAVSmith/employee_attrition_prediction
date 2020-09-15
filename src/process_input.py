########################################
# object that transform the input according to given
# input according to the way the train data was transformed
#
########################################

#import

import json

class Transform_input:
    dir_path = './../data/processed_files/'

    def __init__(self, directory):

        print('loaded')
        self.path = self.dir_path + directory

        self.json = None


    def load_json(self ,file):
        """

        :param load_json:
        :return:
        """
        file_path = self.path + file
        with open(file_path, 'r') as file:
            data = json.load(file)
            features = data.keys()
            print(features)




if __name__ == '__main__':
    example_input = '{"satisfaction":0.74,"evaluation":0.92,"number_of_projects":4,"average_montly_hours":261,"time_spend_company":5,"work_accident":0,"churn":1,"promotion":0,"department":"technical","salary":"medium"}'
    transform = Transform_input('test/')
    transform.load_json('metadata.json')

