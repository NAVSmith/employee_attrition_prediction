from data_preprocessing import Base_data_preprocessing
from split_data import Split_data
from dl_model import Basic_dl_model
import tensorflow as tf

#df = Base_data_preprocessing('./../data/eemployes_data.csv')
df = Basic_dl_model('test')

