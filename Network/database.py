# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


train_x = mnist.train.images.reshape([-1,28,28,1])
train_y = mnist.train.labels
test_x = mnist.test.images.reshape([-1,28,28,1])
test_y = mnist.test.labels
