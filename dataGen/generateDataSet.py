import cv2
import random

def rotateBaseImg(imgFile, setSize):
    degreeOffset = 10
    totalImgs = []
    quarterNote = cv2.imread(imgFile, 0)
    quarterNote = cv2.bitwise_not(quarterNote)
    rows,cols = quarterNote.shape
    for i in range(setSize-2):
        M = cv2.getRotationMatrix2D((cols/2,rows/2),random.randint(-degreeOffset,degreeOffset),1)
        curImage = cv2.warpAffine(quarterNote,M,(cols,rows))
        curImage = cv2.bitwise_not(curImage)
        totalImgs.append(curImage)
    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    curImage = cv2.warpAffine(quarterNote,M,(cols,rows))
    curImage = cv2.bitwise_not(curImage)
    totalImgs.append(curImage)
    quarterNote = cv2.bitwise_not(quarterNote)
    totalImgs.append(quarterNote)
    drawImgs(totalImgs, setSize)


def drawImgs(imgList, setSize):
    for i in range(setSize):
        cv2.imshow('rotation' + str(i), imgList[i])

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
	# filename = input('Enter file for base image: ')
	# size = input('Enter size of data set to generate ')
	rotateBaseImg('quarterNoLine.png', 100)
if __name__ == '__main__':
	main()