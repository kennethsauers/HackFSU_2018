import numpy as np

len_x = 30
len_y = 30
resolution = len_x * len_y
num_chan = 1


data_6 = np.load('SixteenthTest.npy')
print(data_6.shape)
data_6_label = np.load('SixteenthLabel.npy')
data_6 = data_6.reshape(-1,resolution)
data_6_label = data_6_label.reshape(1250,2)

print(data_6.shape)

big_data = []
big_data_label = []

for i in range(1250):

    big_data.append(data_6[i])
    big_data_label.append(data_6_label[i])


big_data = np.array(big_data)
big_data_label = np.array(big_data_label)

big_data = big_data.reshape(-1,len_x,len_y,num_chan)

#print(big_data.shape)

np.save('big_test', big_data)
np.save('big_test_label', big_data_label)
