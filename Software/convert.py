#!/usr/bin/python
import sys
import cv2
import numpy as np
import pickle
import scipy.ndimage.measurements
img = np.zeros((300,512,3), np.uint8)

def openFile():
    global img
    if len(sys.argv) < 3:
        exit()
    img = cv2.imread(sys.argv[2])

def makePhoto():
    global img
    if len(sys.argv) < 3:
        exit()
    cap = cv2.VideoCapture(int(sys.argv[2]))
    ret, img = cap.read()

def deviceList():
    pass
    exit()


def unknownArg():
    exit("What doe's it mean: '%s' ?"%sys.argv[1])

if len(sys.argv) < 2:
    print """
    No arguments.
    Use one of this:
        camera (device inddex) - to make photo
        open file - to open image
        list - to print device list
    """
{"camera":makePhoto,
"open":openFile,
"list":deviceList,
}.get(sys.argv[1], unknownArg)()
img = cv2.resize(img,(16000/20 , 11000/20), interpolation = cv2.INTER_LINEAR)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.createTrackbar('R','image',100,100,lambda x: 0)
cv2.createTrackbar('G','image',100,100,lambda x: 0)
cv2.createTrackbar('B','image',100,100,lambda x: 0)
cv2.createTrackbar('Tcoof','image',50,100,lambda x: 0)
cv2.createTrackbar('Tsize','image',11,20,lambda x: 0)
cv2.createTrackbar('minC','image',100,300,lambda x: 0)
cv2.createTrackbar('maxC','image',200,300,lambda x: 0)
cv2.createTrackbar('Threshold','image',0,1,lambda x: 0)
cv2.createTrackbar('UseCanny','image',0,1,lambda x: 0)

while(1):
    r_persent = 0.01 * cv2.getTrackbarPos('R','image')
    g_persent = 0.01 * cv2.getTrackbarPos('G','image')
    b_persent = 0.01 * cv2.getTrackbarPos('B','image')
    Tcoof = 0.02 * cv2.getTrackbarPos('Tcoof','image')
    Tsize = cv2.getTrackbarPos('Tsize','image')+2

    if Tsize%2==0:Tsize+=1
    tmp_img = np.copy(img)

    tmp_img[:,:,0]=tmp_img[:,:,0]*b_persent
    tmp_img[:,:,1]=tmp_img[:,:,1]*g_persent
    tmp_img[:,:,2]=tmp_img[:,:,2]*r_persent
    gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
    if cv2.getTrackbarPos('Threshold','image') == 1:
        gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,Tsize,Tcoof)
    if cv2.getTrackbarPos('UseCanny','image') == 1:
        minC = cv2.getTrackbarPos('minC','image')
        maxC = cv2.getTrackbarPos('maxC','image')
        gray = cv2.Canny(gray,maxC,minC)
        gray = 255-gray

    #gray  = cv2.Canny(gray,10,20)
    gravity_center =  scipy.ndimage.measurements.center_of_mass(gray)
    gravity_center = (int(gravity_center[0]),int(gravity_center[1]))
    #get center of image gravity
    cv2.circle(tmp_img,gravity_center, 3, (255,0,0), -1)

    cv2.imshow('image',tmp_img)
    cv2.imshow('result',gray)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        with open("output.pic",'w') as f:
            pickle.dump(gray,f)
        break

cv2.destroyAllWindows()
