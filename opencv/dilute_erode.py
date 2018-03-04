# we gonna try one more time leggo

import sys
import numpy as np
import cv2


if __name__ == "__main__":
    path = 'C:/Users/Keegan/Desktop/fsuhacks/img/sheet/races.png'

    # read in sheet music
    sheet = cv2.imread(path, cv2.IMREAD_COLOR)
    cv2.imshow("sheet", sheet)
    cv2.waitKey(0)

    # convert to grayscale
    if len(sheet.shape) != 2:
        gray = cv2.cvtColor(sheet, cv2.COLOR_BGR2GRAY)
    else:
        gray = sheet

    cv2.imshow("gray", gray)
    cv2.waitKey(0)

    # convert to a binary image
    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                             cv2.THRESH_BINARY, 15, -2)

    cv2.imshow("binary", bw)
    cv2.waitKey(0)

    # create images for extraction
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    # specify size
    cols = horizontal.shape[1]
    horizontal_size = (int)(cols / 15)

    # create structure element for extracting horizontal lines
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

    # apply morphology whatever that is
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    cv2.imshow("deleted", horizontal)
    cv2.waitKey(0)



    rows = vertical.shape[0]
    verticalsize = (int)(rows / 30)

    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    cv2.imshow("vertical", vertical)

    # inverse vertical for some reason
    vertical = cv2.bitwise_not(vertical)
    cv2.imshow("vertical", vertical)
    cv2.waitKey(0)

    # extract edges
    edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 3, -2)
    cv2.imshow("edges", edges)
    cv2.waitKey(0)

    # dilate the edges
    kernal = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernal)
    cv2.imshow("dilate", edges)
    cv2.waitKey(0)

    # smooooooth
    smooth = np.copy(vertical)

    # blur smooth lmao
    smooth = cv2.blur(smooth, (2,2))

    # smoooooooth copy
    (rows, cols) = np.where(edges != 0)
    vertical[rows, cols] = smooth[rows, cols]

    # show the final result pls god work
    cv2.imshow("smooth - final", vertical)
    cv2.waitKey(0)
