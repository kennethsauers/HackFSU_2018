import cv2
import random
import os
import numpy as np
import datetime

# Generates the numpy for the non-note images
def generateEmptyLabels(count):
    print('Generating Empty Lables...')
    folderName = 'DataSet'
    path = os.path.join(os.getcwd(), folderName)
    ts = datetime.datetime.now()

    if not os.path.exists(path):
	    os.makedirs(path)
	
	# Fills the top row with 1, and the bottom row with 0	
    lilBoi = [[1 for x in range(int (count))]for y in range(2)]
    for i in range(int(count)):
        lilBoi[1][i] = 0
    lilBoi = np.asarray(lilBoi)
	
    fileName = ("EmptyLabels%s" % count)
    filePath = os.path.join(path, fileName)
    np.save(filePath, lilBoi, allow_pickle=True, fix_imports=True) 

# Generates the numpy of labels for quarter notes	
def generateQuarterLabels(count):
    print('Generating Quarter Labels...')
    folderName = 'DataSet'
    path = os.path.join(os.getcwd(), folderName)
    ts = datetime.datetime.now()
    if not os.path.exists(path):
	    os.makedirs(path)

	# Fills the top row with 0, and the bottom row with 1	
    lilBoi = [[0 for x in range(int(count))]for y in range(2)]
    for i in range(int(count)):
        lilBoi[1][i] = 1
    lilBoi = np.asarray(lilBoi)

    fileName = ("QuarterLabels%s" % count)
    filePath = os.path.join(path, fileName)
    np.save(filePath, lilBoi, allow_pickle=True, fix_imports=True) 

# Creates the set of slightly rotated and translated images
def createSet(imgFile, setSize):
    # Sets realistic boundaries for how different the picture will be
	degreeOffset = 10
    translationOffset = 5;
	
    totalImgs = []
    quarterNote = cv2.imread(imgFile, 0)
    quarterNote = cv2.bitwise_not(quarterNote)
    rows,cols = quarterNote.shape
    for i in range(setSize-2):
        M = cv2.getRotationMatrix2D((cols/2,rows/2),random.randint(-degreeOffset,degreeOffset),1)
        curImage = cv2.warpAffine(quarterNote,M,(cols,rows))
        M = np.float32([[1,0,random.randint(-translationOffset,translationOffset)],[0,1,random.randint(-translationOffset,translationOffset)]])
        curImage = cv2.warpAffine(curImage,M,(cols,rows))
        #curImage = cv2.bitwise_not(curImage)
        totalImgs.append(curImage)
    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    curImage = cv2.warpAffine(quarterNote,M,(cols,rows))
    M = np.float32([[1,0,random.randint(-translationOffset,translationOffset)],[0,1,random.randint(-translationOffset,translationOffset)]])
    curImage = cv2.warpAffine(curImage,M,(cols,rows))
    #curImage = cv2.bitwise_not(curImage)
    totalImgs.append(curImage)
    #quarterNote = cv2.bitwise_not(quarterNote)
    totalImgs.append(quarterNote)
    if imgFile == 'quarterNoLine.png':
    	generateQuarterLabels(setSize)
    else:
    	generateEmptyLabels(setSize)
    #saveImgs(totalImgs, imgFile)
    drawImgs(totalImgs, setSize)

# Draws the resultant images on the screen	
def drawImgs(imgList, setSize):
    for i in range(setSize):
        cv2.imshow('rotation' + str(i), imgList[i])

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Saves the resultant images	
def saveImgs(dataSet, imgFile):
    folderName = 'DataSet'
    path = os.path.join(os.getcwd(), folderName)
    size = len(dataSet)
    if not os.path.exists(path):
        os.makedirs(path)
    bigBoi = np.asarray(dataSet)
    if imgFile == 'quarterNoLine.png':
	    fileName = ("QuarterNotes%s" % size)
    else:
	    fileName = ("EmptyNotes%s" % size)
    filePath = os.path.join(path, fileName)
    np.save(filePath, bigBoi, allow_pickle=True, fix_imports=True)      
        
def main():
	filename = input('Enter file for base image: ')
	size = input('Enter size of data set to generate ')
	createSet(filename,int(size))

if __name__ == '__main__':
	main()