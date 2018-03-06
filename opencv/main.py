import cv2
import numpy as np
import glob
import os
import math
import soundToMidi as matt

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
    tsigLoc = r'img/query/tsig.png'
    qPath = os.path.join(os.getcwd(), tsigLoc)
    query = cv2.imread(qPath, 0)
    res = cv2.matchTemplate(img, query, cv2.TM_SQDIFF)

    return res


if __name__ == "__main__":
    noteNames = ['f4' 'e4', 'e4', 'c4', 'b3', 'a3', 'g3', 'f3', 'e3', 'd3', 'c3']
    musicLoc = r'img/sheet/twinkle.png'
    musicPath = os.path.join(os.getcwd(), musicLoc)
    #img = goodByeLines(musicPath)
    img = cv2.imread(musicPath,0)
    notes = []
    dividers = []
    flag = 0
    #trebleLoc = r'img/query/treble.png'
    #treblePath = os.path.join(os.getcwd(), trebleLoc)
    #treble = cv2.imread(treblePath, 0)
    #wT, hT = treble.shape[::-1]
    #while wT > 30:
    #    trebRes = cv2.matchTemplate(img, treble, cv2.TM_CCOEFF_NORMED)
    #    trebThreshold = 0.7
    #    loc = np.where(trebRes >= trebThreshold)
    #    treble = cv2.resize(treble, None, fx = 0.8, fy = 0.8, interpolation = cv2.INTER_AREA)
    #    wT, hT = treble.shape[::-1]
    
    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(trebRes)

    #top_left = max_loc
    #bottom_right = (top_left[0] + wT + 320, top_left[1] + hT)
    #cv2.rectangle(img, bottom_right,top_left,(0,0,255), 2)

    cv2.imshow('test', img)
    cv2.waitKey(0)
    
    # Find the staff bars (idk the term)    
    lineLoc = r'img/sheet/bigLine.png'
    linePath = os.path.join(os.getcwd(), lineLoc)
    frame = cv2.imread(linePath, 0)
    w, h = frame.shape[::-1]
    bestMax = 0
    bestW = 0
    bestH = 0
    i=0
    # Find lines 
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img,50,150,apertureSize = 3)
    lines = cv2.HoughLines(img,1,np.pi/180,20)
    desiredAngle = 1.57079632679
    print (np.shape(lines))
    for rho,theta in lines[0]:
        i+=1
        print("Line%d: %d     %f" %(i,rho, theta))
        # If the line's angle's percent difference to a horizontal line is greater than 5%
        # We consider it not straight and throw it away
        #if abs((theta - desiredAngle)/desiredAngle - 1) > 0.05:
         #   continue
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(img, (x1, y1), (x2 , y2), (0, 255, 0), 2)
        dividers.append((y2+y1)//2 )
        
                      
    #print (len(dividers))
    cv2.imshow('test', img)
    cv2.waitKey(0)
    diff = dividers[4] - dividers[0]
    diff /= 8
    start = dividers[0]
    
    img = cv2.imread(musicPath,0)
    # Finds the quarter notes and boxes them
    qtrLoc = r'img/query/qrt.png'
    qtrPath = os.path.join(os.getcwd(), qtrLoc)
    query = cv2.imread(qtrPath, 0)
    w, h = query.shape[::-1]
    bestMax = 0
    bestW = 0
    bestH = 0
    i = 0
    # Finds all matches above a 0.7 threshold
    while w > 30:
        #print ("W: %d, H: %d" %(w, h))
        res = cv2.matchTemplate(img, query, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        currentMax = max_val
        #print (currentMax)
        if currentMax > bestMax:
            bestH = h
            bestW = w
            bestMax = currentMax 
            i = 0
        else:
            i+=1
        if i >= 3:
            break
        query = cv2.resize(query, None, fx = 0.8, fy = 0.8, interpolation = cv2.INTER_AREA)
        w, h = query.shape[::-1]
        bestMax = currentMax

    # Throws away frames that are extremely close to each other     
    #print (np.shape(loc))
    #bucket=[]
    buckettoX = {}
    xVals = []
    for pt in zip(*loc[::-1]):
        #print ("X:%d Y:%d" %(pt[0], pt[1]))
        for pt2 in zip(*loc[::-1]):
            p1x = int(pt[0])
            p1y = int(pt[1])
            p2x = int(pt2[0])
            p2y = int(pt2[1])
            # If we've looked through all our points up to the current one,
            # move to the next one
            if p1x == p2x and p1y == p2y :
                break
            # If the frames are too close, don't draw it
            if abs(p2x - p1x + p2y - p1y) < 30:
                flag = 1
        if flag == 0:
            print ("Adding rect at x: %d, y: %d" %(p1x,p1y))
            cv2.rectangle(img, pt, (pt[0] + bestW, pt[1] + bestH), (0, 0, 255), 2)
            #cv2.rectangle(img, pt, (pt[0], pt[1]), (0, 0, 255), 2)
            #notes.append(img[pt[1]:pt[1] + bestH, pt[0]:pt[0] + bestW])
            bucket = int(math.floor((pt[1]+bestH) % start //diff))
            buckettoX[pt[0]] = bucket - 2
            xVals.append(pt[0])
            #print (bucket)
           # print(" ")
            #print (noteNames[bucket - 2]) 
            #print(" ")
            #cv2.imshow("Note", notes[len(notes) - 1])
            #cv2.waitKey(0)
        flag = 0
        #cv2.imshow("crop", crop_img)
        #cv2.waitKey(0)

        #crop_img = img[pt[1] + 5:(pt[1] + h - 5), pt[0] + 5:(pt[0] + w)]
        # what if you run template matching again on the cropped images
        # for cleanup?
        # can't I just make the rectangle smaller....
        # contour?? 

    xVals.sort()
    allNotes = []
    for value in xVals:
        print(noteNames[buckettoX[value]])
        allNotes.append(noteNames[buckettoX[value]])
    matt.generateMidi(allNotes)  
   # print (type(notes))
    cv2.imshow('test', img)
    cv2.waitKey(0)
    #cv2.imshow("crop", crop_img)
    #cv2.waitKey(0)
