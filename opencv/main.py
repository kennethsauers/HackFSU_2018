import cv2
import numpy as np
import glob

def goodByeLines(path):
    ## Read
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## (1) Create long line kernel, and do morph-close-op
    kernel = np.ones((1,40), np.uint8)
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("line_detected.png", morphed)

    ## (2) Invert the morphed image, and add to the source image:
    dst = cv2.add(gray, (255-morphed))
    cv2.imwrite("line_removed.png", dst)

    # show the final result pls god work
    cv2.imshow("smooth - final", dst)
    cv2.waitKey(0)

    return dst

def findTimeSig(img):
    qPath = 'C:/Users/Keegan/Desktop/fsuhacks/img/query/tsig.png'
    query = cv2.imread(qPath, 0)
    res = cv2.matchTemplate(img, query, cv2.TM_SQDIFF)

    return res


if __name__ == "__main__":
    path = 'C:/Users/Keegan/Desktop/fsuhacks/img/sheet/twinkle.png'
    img = goodByeLines(path)

    tPath = 'C:/Users/Keegan/Desktop/fsuhacks/img/query/treble.png'
    treble = cv2.imread(tPath, 0)
    wT, hT = treble.shape[::-1]

    result = cv2.matchTemplate(img,treble,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    bottom_right = (top_left[0] + wT + 320, top_left[1] + hT)
    cv2.rectangle(img,top_left, bottom_right, (0,0,255), 2)

    cv2.imshow('test', img)
    cv2.waitKey(0)


    qtrPath = 'C:/Users/Keegan/Desktop/fsuhacks/img/query/qrt.png'

    query = cv2.imread(qtrPath, 0)
    w, h = query.shape[::-1]

    res = cv2.matchTemplate(img, query, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        crop_img = img[pt[1]:pt[1] + h, pt[0]:pt[0] + w]
        #cv2.imshow("crop", crop_img)
        #cv2.waitKey(0)




        #crop_img = img[pt[1] + 5:(pt[1] + h - 5), pt[0] + 5:(pt[0] + w)]
        # what if you run template matching again on the cropped images
        # for cleanup?
        # can't I just make the rectangle smaller....
        # contour??


    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.imshow("crop", crop_img)
    cv2.waitKey(0)
