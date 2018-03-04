from __future__ import print_function
import tensorflow as tf
import database
import os
import numpy as np
# Parameters
learning_rate = 0.001
training_epochs = 33
batch_size = 100
display_step = 1

n_hidden_1 = 128
n_hidden_2 = 128
dense = tf.layers.dense
conv_2d = tf.layers.conv2d
flatten = tf.contrib.layers.flatten


class brain():

    def __init__(self, name, input_size = [None,30,30,1],input_size_1= [-1,30,30,1], output_size = 2):
        self.input_size = input_size
        self.output_size = output_size
        self.input_size_1 = input_size_1
        self.model_path = "model/" + name
        self.model_name = self.model_path + '/' + name
        if not os.path.exists(self.model_name):
            os.makedirs(self.model_name)

        self.loss_op, self.train_op, self.logits = self.create_optimizer()

    def save(self, sess, filepath = '/model'):
        self.saver.save(sess, filepath)

    # This function sets up the model
    def multilayer_perceptron(self):
        self.X = tf.placeholder("float", self.input_size)
        self.Y = tf.placeholder("float",  [None, self.output_size])
        conv_1 = conv_2d(inputs=self.X, filters = 16, kernel_size = 3, strides=2, padding = 'SAME')
        flat = flatten(conv_1)
        layer_1 = dense(inputs = flat, units = n_hidden_1)
        layer_2 = dense(inputs = layer_1, units = n_hidden_2)
        out_layer = dense(inputs = layer_2, units = self.output_size)
        return out_layer

    # this function creating all variables and methods need to train the model
        def create_optimizer(self):
        logits = self.multilayer_perceptron()
        loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=self.Y))
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        train_op = optimizer.minimize(loss_op)
        return loss_op, train_op, logits

    # trains model on data from database.py for Parameter epoch times
    def training(self, save_after_training = True, with_restore = False):
        with tf.Session() as sess:
            writer = tf.summary.FileWriter("output", sess.graph)
            self.saver = tf.train.Saver()
            sess.run(tf.global_variables_initializer())
            if with_restore:
                self.saver.restore(sess, tf.train.latest_checkpoint(self.model_path))
            for epoch in range(training_epochs):
                avg_cost = 0.
                total_batch = database.train_x.shape[0]
                _, c = sess.run([self.train_op, self.loss_op], feed_dict={self.X: database.train_x, self.Y: database.train_y})
                cost = c
                if epoch % display_step == 0:
                    print("Epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(cost))
            print("Optimization Finished!")

            pred = tf.nn.softmax(self.logits)
            correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(self.Y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            print("Accuracy:", accuracy.eval({self.X: database.test_x, self.Y: database.test_y}))
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
            prob = sess.run(self.logits, feed_dict = feed_dict)
            prob = sess.run(tf.nn.softmax(prob))
        return prob

    # finds the output with this highest predicted probability
    def evaluate(self, input, restore = True):
        prob = self.predict(input)
        return np.argmax(prob)
