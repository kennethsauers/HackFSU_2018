import numpy as np
import tensorflow as tf

# pulls data from data folder for training and testing
big_data = np.load('Data/big_data.npy')
big_data_label = np.load('Data/big_data_label.npy')
big_test = np.load('Data/big_test.npy')
big_test_label = np.load('Data/big_test_label.npy')

# data using by other files ie. model.py and main.py
train_x =big_data
train_y = big_data_label
test_x = big_test
test_y = big_test_label
