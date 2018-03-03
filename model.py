import tflearn
import tensorflow as tf
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d

from tflearn.layers.estimator import regression
import os

import database

keep = 0.8
input_size = 28*28
LR = 1e-3



class agent():
    def __init__(self, name = "Standard_Name", input_x = 28, input_y = 28, num_output = 10):
        self.name = name
        self.input_x = input_x
        self.input_y = input_y
        self.num_output = num_output
        self.model = self.model_create()
        self.main_dir = 'model_saves'
        self.model_name = self.main_dir + '/' + self.name + '/' + self.name
        if not os.path.exists(self.main_dir):
            os.makedirs(self.main_dir)
        if not os.path.exists(self.main_dir + '/' + self.name):
            os.makedirs(self.main_dir + '/' + self.name)

    def save(self):
        self.model.save(self.model_name)

    def restore(self):
        self.model.load(self.model_name)

    def train_for(self, num):
        for i in range(num):
            self.model.fit({'input': database.train_x}, {'targets': database.train_y}, n_epoch=1, snapshot_step=500, show_metric=True, run_id='helpme')

    def predict(self, input):
        prob = self.model.predict(input)
        return prob, np.argmax(prob)

    def model_create(self):
        network = input_data(shape=[None, self.input_x, self.input_y,1], name='input')
        network = conv_2d(network,32,3, activation='relu', regularizer="L2", name = 'conv_2d_1')
        network = max_pool_2d(network, 2)
        network = fully_connected(network, 128, activation='relu', name = 'dense_1')
        network = dropout(network,keep)
        network = fully_connected(network, 64, activation='relu', name = 'dense_2')
        network = dropout(network,keep)
        network = fully_connected(network, self.num_output, activation='softmax', name = 'softmax')
        network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
        model = tflearn.DNN(network, tensorboard_verbose=3)
        return model
