import config
import tensorflow as tf
import numpy as np
import os

weight_init = tf.truncated_normal_initializer(mean=config.mean, stddev=config.stddev)
activation = tf.nn.relu
padding = config.padding
conv2d = tf.layers.conv2d
dense = tf.layers.dense
flatten = tf.contrib.layers.flatten


class model():
    def __init__(self, name = "testing", model_type = "error"):
        if model_type == "error":
            print("model type unspecified")
            exit(0)

        self.name = name
        self.model_type = model_type
        self.create_dir()

        if self.model_type == "frequencey":
            self.x_len = config.frequency_x_len
            self.y_len = config.frequency_y_len

        else if self.model_type == "note":
            self.x_len = config.note_x_len
            self.y_len = config.note_y_len

        else:
            print("undefined model type")
            exit(0)



    def create_model(self):
        self.input_layer = tf.placeholder(????)

        NN = conv2d(name="conv2d_1", input=self.input_layer , filters = config.conv_1_filters, kernel_size= config.conv_1_size, strides = config.conv_1_strides, padding = config.padding, kernel_initializer = weight_init, activation = activation)
        NN = conv2d(name="conv2d_2", input= NN, filters = config.conv_2_filters, kernel_size= config.conv_2_size, strides = config.conv_2_strides, padding = config.padding, kernel_initializer = weight_init, activation = activation)
        NN = flatten(NN)
        NN = dense(name = "dense_1", input= NN, units= config.dense_1_units, kernel_initializer= weight_init, activation = activation)
        NN = dense(name = "dense_2", input= NN, units= config.dense_2_units, kernel_initializer= weight_init, activation = activation)
        # output layer
        NN = dense(name = "output_layer", input=NN , units=config.dense_output_units , kernel_initializer= weight_init, activation = activation)

        self.prob_y = NN
        self.prediction = tf.argmax(self.prob_y, 1)

        self.y_target = tf.placeholder(shape=[None], dtype=tf.float32)
        self.y_target_onehot = tf.one_hot(self.y_target, config.dense_output_units, dtype=tf.float32)
        self.error = tf.nn.softmax_cross_entropy_with_logits(labels=None, logits=None, dim=-1, name="cross_logit_loss")
        self.loss = tf.reduce_mean(self.error)

        return True


    def create_dir(self):
        self.model_path = "model/" + self.model_type + "/" + self.name
        self.data_path = "data/" + self.model_type + "/" + self.name

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        return True

    def save(self):
        self.saver.save(self.sess, save_path = self.model_path)

    def load(self);
        self.saver.restore(self.sess, save_path = self.model_path)
