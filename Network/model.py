import tflearn
import tensorflow
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import os

import database
import config

class agent():
    def __init__(self, name):
        self.name = name
        self.model = self.model_create()
        self.main_dir = 'model_saves'
        self.model_name = self.main_dir + '/' + self.name
        if not os.path.exists(self.main_dir):
            os.makedirs(self.main_dir)

    def saver(self):
        self.model.save(self.model_name)

    def restorer(self):
        self.model.load(self.model_name)

    def train_for(self, num):
        for i in range(num):
            self.model.fit({'input': database.train_x}, {'targets': database.train_y}, n_epoch=1, snapshot_step=500, show_metric=True, run_id='openai_learning')


    def model_create(self):
        network = input_data(shape=[None, config.input_size], name='input')
        network = fully_connected(network, 128, activation='relu', name = 'hidden_1')
        network = dropout(network,config.keep)
        network = fully_connected(network, 256, activation='relu', name = 'hidden_2')
        network = dropout(network,config.keep)
        network = fully_connected(network, 512, activation='relu', name = 'hidden_3')
        network = dropout(network,config.keep)
        network = fully_connected(network, 256, activation='relu', name = 'hidden_4')
        network = dropout(network,config.keep)
        network = fully_connected(network, 128, activation='relu', name = 'hidden_5')
        network = dropout(network,config.keep)
        network = fully_connected(network, 10, activation='softmax', name = 'softmax')
        network = regression(network, optimizer='adam', learning_rate=config.LR, loss='categorical_crossentropy', name='targets')
        model = tflearn.DNN(network, tensorboard_verbose=3)
        return model


# In[4]:


def main():
    name = agent('broo')

    name.train_for(1)




# In[5]:


if __name__ == '__main__':
    main()
