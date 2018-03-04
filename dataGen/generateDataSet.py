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
	
	# create 2D array that labels data as invalid	
    lilBoi = [[1 for x in range(int (count))]for y in range(2)]
    for i in range(int(count)):
        lilBoi[1][i] = 0
    lilBoi = np.asarray(lilBoi)
	
    fileName = input('Enter desired label file name ')
    filePath = os.path.join(path, fileName)
    np.save(filePath, lilBoi, allow_pickle=True, fix_imports=True) 

# Generates the numpy of labels for quarter notes	
def generateQuarterLabels(count):
    print('Generating Quarter Labels...')

    # create folder to store label data
    folderName = 'DataSet'
    path = os.path.join(os.getcwd(), folderName)

    # use current datetime to generate unique file name
    ts = datetime.datetime.now()
    if not os.path.exists(path):
	    os.makedirs(path)

	# create a 2D array that labels the data as valid
    lilBoi = [[0 for x in range(int(count))]for y in range(2)]
    for i in range(int(count)):
        lilBoi[1][i] = 1
    lilBoi = np.asarray(lilBoi)

    fileName = input('Enter desired label file name ')
    filePath = os.path.join(path, fileName)
    np.save(filePath, lilBoi, allow_pickle=True, fix_imports=True) 

# Creates the set of slightly rotated and translated images
def createSet(imgFile, setSize, quarter, debug):

    # Sets realistic boundaries for how different the picture will be
    degreeOffset = 10
    translationOffset = 5
    invert = 'n'
    # create list to store all images
    totalImgs = []

    if debug == 'y':
        invert = input('Invert color? (y/n) ')

    # read in the file given by the filname and invert the color
    # count rows and columns in the image
    baseImage = cv2.imread(imgFile, 0)
    baseImage = cv2.bitwise_not(baseImage)
    rows,cols = baseImage.shape

    # generate random rotations and translations of the original image
    # bounded by the offsets and then append to a list
    for i in range(setSize-2):
        M = cv2.getRotationMatrix2D((cols/2,rows/2),random.randint(-degreeOffset,degreeOffset),1)
        curImage = cv2.warpAffine(baseImage,M,(cols,rows))
        M = np.float32([[1,0,random.randint(-translationOffset,translationOffset)],[0,1,random.randint(-translationOffset,translationOffset)]])
        curImage = cv2.warpAffine(curImage,M,(cols,rows))
        ## undo color inversion
        curImage = cv2.bitwise_not(curImage) if invert != 'y' else curImage
        totalImgs.append(curImage)

    # generate specific case of 180 rotation
    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    curImage = cv2.warpAffine(baseImage,M,(cols,rows))
    M = np.float32([[1,0,random.randint(-translationOffset,translationOffset)],[0,1,random.randint(-translationOffset,translationOffset)]])
    curImage = cv2.warpAffine(curImage,M,(cols,rows))
    # undo color inversion and append the original and special case
    curImage = cv2.bitwise_not(curImage) if invert != 'y' else curImage
    totalImgs.append(curImage)
    baseImage = cv2.bitwise_not(baseImage) if invert != 'y' else baseImage
    totalImgs.append(baseImage)

    if debug == 'y':
        drawImgs(totalImgs, setSize)
    else:
    # check whether label array is formatted for a valid input or invalid input
        if quarter == 'y':
    	    generateQuarterLabels(setSize)
        else:
    	    generateEmptyLabels(setSize)
        saveImgs(totalImgs, imgFile)

# Draws the resultant images on the screen	
# Mostly used for debugging
def drawImgs(imgList, setSize):
    for i in range(setSize):
        cv2.imshow('rotation' + str(i), imgList[i])

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# store 2d pixel arrays to the filename stored at the filename imgFile	
def saveImgs(dataSet, imgFile):
    folderName = 'DataSet'

    # find the current working directly to create a folder there to store the images
    path = os.path.join(os.getcwd(), folderName)
    size = len(dataSet)
    if not os.path.exists(path):
        os.makedirs(path)

    # store the 2D array representation of the images in an array and allow for 
    # customized outputfile naming
    bigBoi = np.asarray(dataSet)
    fileName = input('Enter desired output file name ')
    filePath = os.path.join(path, fileName)
    np.save(filePath, bigBoi, allow_pickle=True, fix_imports=True)      
        
def main():
    filename = input('Enter file for base image: ')
    size = input('Enter size of data set to generate ')
    quarter = input('Does this have a quarter note? (y/n) ')
    debug = input('Debug mode? (y/n) ')
    createSet(filename, int(size), quarter, debug)

if __name__ == '__main__':
	main()