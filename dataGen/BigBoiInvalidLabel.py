import cv2
import random
import os
import numpy as np
import datetime

folderName = 'DataSet'
path = os.path.join(os.getcwd(), folderName)
ts = datetime.datetime.now()
count = input("How many labels do you need? ")

if not os.path.exists(path):
	os.makedirs(path)
	
lilBoi = [[1 for x in range(int (count))]for y in range(2)]
for i in range(int(count)):
    lilBoi[0][i] = 0
lilBoi = np.asarray(lilBoi)

fileName = ("EmptyLabels%s" % count)
filePath = os.path.join(path, fileName)
np.save(filePath, lilBoi, allow_pickle=True, fix_imports=True) 
