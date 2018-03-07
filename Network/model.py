from __future__ import print_function
import tensorflow as tf
import database
import os
import datetime
import numpy as np
# Parameters

log_histograms = False

batch_size = 20
display_step = 1

filters_conv_1 = 16
kernal_size_conv1 = 3
strides_conv1 = 2

n_hidden_1 = 128
n_hidden_2 = 128
dense = tf.layers.dense
conv_2d = tf.layers.conv2d
flatten = tf.contrib.layers.flatten


class brain():
    def __init__(self, name, input_size = [None,30,30,1],input_size_1= [-1,30,30,1], output_size = 2
                ,learning_rate = .001):
        self.input_size = input_size
        self.output_size = output_size
        self.input_size_1 = input_size_1
        self.name = name
        self.learning_rate = learning_rate
        self.model_path = "model/" + name
        self.model_name = self.model_path + '/' + name
        if not os.path.exists(self.model_name):
            os.makedirs(self.model_name)
        self.create_network()
        return

    # this function creating all variables and methods need to train the model
    def create_network(self):
        self.X = tf.placeholder("float", self.input_size, name='X_placeholder')
        self.Y = tf.placeholder("float",  [None, self.output_size], name = 'Y_placeholer')
##################################################################################################################################################################################
        conv_1 = conv_2d(inputs=self.X, filters = filters_conv_1,
            kernel_size = kernal_size_conv1, strides=strides_conv1,
            padding = 'SAME', name = 'Conv_1')
        conv_2 = conv_2d(inputs=conv_1, filters = filters_conv_1,
            kernel_size = kernal_size_conv1, strides=strides_conv1,
            padding = 'SAME', name = 'Conv_2')
        flat = flatten(conv_2)
        layer_1 = dense(inputs = flat, units = n_hidden_1, name = 'Layer_1')
        layer_2 = dense(inputs = layer_1, units = n_hidden_2, name = 'Layer_2')
        self.logits = dense(inputs = layer_2, units = self.output_size, name='Layer_Output')
##################################################################################################################################################################################
        self.loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y), name = 'Loss_op')
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate, name = 'Optimizer')
        self.train_op = optimizer.minimize(self.loss_op)
        self.pred = tf.nn.softmax(self.logits, name = 'Pred')
        correct_prediction = tf.equal(tf.argmax(self.pred, 1), tf.argmax(self.Y, 1), name='correct_prediction')
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"), name= 'Accuracy')
###################################################################################################################################################################################
        tf.summary.scalar('Accuracy', self.accuracy)
        tf.summary.scalar("loss", self.loss_op)
        if log_histograms:
            tf.summary.histogram('X',self.X)
            tf.summary.histogram('Y',self.Y)
            tf.summary.histogram('conv_1',conv_1)
            tf.summary.histogram('layer_1',layer_1)
            tf.summary.histogram('layer_2',layer_2)
            tf.summary.histogram('logits', self.logits)
        return

    # trains model on data from database.py for Parameter epoch times
    def train_for(self, training_epochs = 20, save_after_training = True, with_restore = False):
        with tf.Session() as sess:
            #setting up Tensorboard, saver and restore
            writer = tf.summary.FileWriter("Tensorboard/" + self.name, sess.graph)
            self.merged = tf.summary.merge_all()
            self.saver = tf.train.Saver()
            sess.run(tf.global_variables_initializer())
            if with_restore:
                self.saver.restore(sess, tf.train.latest_checkpoint(self.model_path))
            #training loop
            for epoch in range(training_epochs):
                avg_cost = 0.
                total_batch = database.train_x.shape[0]
                _, c, mer, acc = sess.run([self.train_op, self.loss_op, self.merged, self.accuracy], feed_dict={self.X: database.train_x, self.Y: database.train_y})
                writer.add_summary(mer, epoch)
                cost = c
                if epoch % display_step == 0:
                    print("Epoch:", '%04d' % (epoch+1), "cost={:.5f}".format(cost),"Accuracy_training={:.5f}".format(acc))
                    print("Accuracy_testing:", self.accuracy.eval({self.X: database.test_x, self.Y: database.test_y}))
            #saves model after training and closes writer
            print("Optimization Finished!")
            if save_after_training:
                self.saver.save(sess, self.model_name, global_step=1000)
            writer.close()
            return True

    #productes the model's confidence on the output of a givin action
    def predict(self, input, restore = True):
        feed_dict = {self.X: input.reshape(self.input_size_1)}
        with tf.Session() as sess:
            self.saver = tf.train.Saver()
            self.saver.restore(sess, tf.train.latest_checkpoint(self.model_path))
            prob = sess.run(self.pred, feed_dict = feed_dict)
        return prob

    # finds the output with this highest predicted probability
    def evaluate(self, input, restore = True):
        prob = self.predict(input)
        return np.argmax(prob)

    def save(self, sess, filepath = '/model'):
        self.saver.save(sess, filepath)
