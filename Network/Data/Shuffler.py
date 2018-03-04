import numpy as np

len_x = 30
len_y = 30
resolution = len_x * len_y
num_chan = 1

data_1 = np.load('emptyTest.npy')
data_1_label = np.load('QuarterTestLabels1500.npy')

data_2 = np.load('quarterTest.npy')
data_2_label = np.load('EmptyTestLabels1500.npy')

# data_1 length =  to data_n length
# todo implement failsafe if data lengths do not equal eacherother
length = data_1.shape[0]

data_1 = data_1.reshape(-1,resolution)
data_2 = data_2.reshape(-1,resolution)
data_1_label = data_1_label.reshape(length,2)
data_2_label = data_2_label.reshape(length,2)

big_data = []
big_data_label = []

for i in range(length):
    big_data.append(data_1[i])
    big_data_label.append(data_1_label[i])
    big_data.append(data_2[i])
    big_data_label.append(data_2_label[i])

big_data = np.array(big_data)
big_data_label = np.array(big_data_label)

big_data = big_data.reshape(-1,len_x,len_y,num_chan)

np.save('big_test', big_data)
np.save('big_test_label', big_data_label)
