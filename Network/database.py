import tflearn.datasets.mnist as mnist
X, train_y, test_x, test_y = mnist.load_data(one_hot=True)
train_x = X.reshape([-1, 28, 28, 1])
test_x = test_x.reshape([-1, 28, 28, 1])
