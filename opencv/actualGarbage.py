import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
from os.path import isfile, join
from os import listdir
import imutils

# this program finds:
# treble cleff
# lol no it doesnt lmao

if __name__ == "__main__":
    print ("Program Start...")

    # paths for reading
    path = 'C:/Users/Keegan/Desktop/fsuhacks/img/sheet/gourmet.png'
    qPath = 'C:/Users/Keegan/Desktop/fsuhacks/img/query/treble.jpg'

    # read in sheet music
    sheet = cv2.imread(path)
    img_gray = cv2.cvtColor(sheet, cv2.COLOR_BGR2GRAY)
    found = None

    # read in the query
    query = cv2.imread(qPath)
    # convert to grayscale
    query = cv2.cvtColor(query,cv2.COLOR_BGR2GRAY)
    # apply canny edge detection
    query = cv2.Canny(query, 50, 200)
    # grab height and width of query
    tW, tH = query.shape[::-1]

    list = []

    # loop template matching
    for scale in np.linspace(0.5, 1.0, 20)[::-1]:
        resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * scale))
        r = img_gray.shape[1] / float(resized.shape[1])

        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, query, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        clone = np.dstack([edged, edged, edged])
        cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
            (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
        cv2.imshow("Visualize", clone)
        cv2.waitKey(0)

        if found is None or maxVal > 4000000:
            list.append([maxVal, maxLoc, r])


    for x in list:
        (_, maxLoc, r) = x
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        cv2.rectangle(sheet, (startX, startY), (endX, endY), (0, 0, 255), 2)


    #(_, maxLoc, r) = found
    #(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    #(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    #cv2.rectangle(sheet, (startX, startY), (endX, endY), (0, 0, 255), 2)
    resized_image = cv2.resize(sheet, (700, 800))
    cv2.imshow("Image", resized_image)
    cv2.waitKey(0)
