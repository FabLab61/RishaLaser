import serial
import time
import sys
import cv2
import numpy as np
import pickle

if len(sys.argv) < 2:
    print """
    No arguments.
    run it as:
    python print.py serialport
    """

#read image
img = pickle.load(open("output.pic",'r'))
img = img/255
shape = img.shape

if "show" in sys.argv:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    while(True):
        cv2.imshow('image',img)
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break

# open serial port
ser = serial.Serial(sys.argv[1],9600)
time.sleep(4)
#convert to comand
#commands from arduino handlers
def unknownCommand(data):
    print "I don't know how to react to %s"%data
    exit(1)

cur_y = 0
cur_x = 0
laser_on = False
at_new_row = False

def sendCommand(data):
    global cur_y,cur_x,laser_on,shape
    if img[cur_y,cur_x] and not laser_on :    #turn on laser_on
        ser.write("O:20\n")
        laser_on = True
    else:                                     #go too next position
        laser_on = False
        #new row
        if ((cur_x+1 == shape[1] and cur_y%2==0) or (cur_x == 0 and cur_y%2==1)) and not at_new_row: # go to new row
            cur_y += 1
            if cur_y < shape[0]:
                ser.write("Y:1\n")
                at_new_row = True
        else: # new x
            at_new_row = False
            if cur_y%2==0:
                cur_x+=1
                ser.write("X:1\n")
            else:
                cur_x-=1
                ser.write("X:-1\n")

def doNothing(data):
    pass

"""
    Commands from arduino:
        S - I am ready for data, you must send next command when recive it send 1 command
        E - Stop transmiting, the queue is full, standby.
"""
commands = {'S':sendCommand, 'E':doNothing}

while (cur_y < shape[0]):
    data = ser.read(size=1)
    commands.get(data,unknownCommand)(data)
    #print percent of work
    sys.stdout.write("\r%d%%" % 100.0*cur_y/shape[1] )

print "Done"
time.sleep(4)
ser.flush()
ser.close()
