import numpy as np

len_x = 30
len_y = 30
resolution = len_x * len_y
num_chan = 1

data_1 = np.load('BlankStaffTest.npy')
data_1_label = np.load('BlankStaffLabel.npy')

data_2 = np.load('HalfNoteTest.npy')
data_2_label = np.load('HalfNoteLabel.npy')

data_3 = np.load('highInSpaceTest.npy')
data_3_label = np.load('highInSpaceLabel.npy')

data_4 = np.load('highOnStaffTest.npy')
data_4_label = np.load('highOnStaffLabel.npy')

data_5 = np.load('quarterInSpaceTest.npy')
data_5_label = np.load('quarterInSpaceLabel.npy')

#data_6 = np.load('SixteenthTest.npy')
#data_6_label = np.load('SixteenthLabel.npy')

data_7 = np.load('WholeTest.npy')
data_7_label = np.load('WholeLabel.npy')

# data_1 length =  to data_n length
# todo implement failsafe if data lengths do not equal eacherother
length = data_1.shape[0]
#print(data_6.shape)
data_1 = data_1.reshape(-1,resolution)
data_2 = data_2.reshape(-1,resolution)
data_3 = data_3.reshape(-1,resolution)
data_4 = data_4.reshape(-1,resolution)
data_5 = data_5.reshape(-1,resolution)
#data_6 = data_6.reshape(-1,resolution)
data_7 = data_7.reshape(-1,resolution)

data_1_label = data_1_label.reshape(length,2)
data_2_label = data_2_label.reshape(length,2)
data_3_label = data_3_label.reshape(length,2)
data_4_label = data_4_label.reshape(length,2)
data_5_label = data_5_label.reshape(length,2)
#data_6_label = data_6_label.reshape(length,2)
data_7_label = data_7_label.reshape(length,2)

big_data = []
big_data_label = []

for i in range(length):
    big_data.append(data_1[i])
    big_data_label.append(data_1_label[i])
    big_data.append(data_2[i])
    big_data_label.append(data_2_label[i])
    big_data.append(data_3[i])
    big_data_label.append(data_3_label[i])
    big_data.append(data_4[i])
    big_data_label.append(data_4_label[i])
    big_data.append(data_5[i])
    big_data_label.append(data_5_label[i])
#    big_data.append(data_6[i])
#    big_data_label.append(data_6_label[i])
    big_data.append(data_7[i])
    big_data_label.append(data_7_label[i])

big_data = np.array(big_data)
big_data_label = np.array(big_data_label)

big_data = big_data.reshape(-1,len_x,len_y,num_chan)

#print(big_data.shape)

np.save('big_data', big_data)
np.save('big_data_label', big_data_label)
