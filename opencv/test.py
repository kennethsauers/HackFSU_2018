import numpy as np
import cv2

path = 'C:/Users/Keegan/Desktop/fsuhacks/img/sheet/races.png'

gray = cv2.imread(path)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imwrite('edges-50-150.jpg',edges)
minLineLength=100
lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]),
                    minLineLength=minLineLength,maxLineGap=80)
