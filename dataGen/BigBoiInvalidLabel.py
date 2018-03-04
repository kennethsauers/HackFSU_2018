import cv2
import random
import os
import numpy as np
import datetime

folderName = 'DataSet'
path = os.path.join(os.getcwd(), folderName)
ts = datetime.datetime.now()
if not os.path.exists(path):
	os.makedirs(path)
lilBoi = np.zeros(100)
fileName = "BigBoiInvalidLabel"
filePath = os.path.join(path, fileName)
np.save(filePath, lilBoi, allow_pickle=True, fix_imports=True) 
