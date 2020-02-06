import cv2
import numpy as np
from Camera import camera
from Image import image
from time import sleep
refPt = ()
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def FindBounds(event, x, y, flags, param):
    global Image
    if event == cv2.EVENT_LBUTTONDOWN:
        contours = make_contours(Image)
        refPt = (x, y)
        print(refPt)
        check_countour(Image,contours,refPt)
                
    
def check_countour(Image,contours,point):
    i = 0;
    # create hull array for convex hull points
    hull = []
 
    # calculate points for each contour
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull.append(cv2.convexHull(contours[i], False))
    Image.convexHullFrame = cv2.drawContours(Image.uneditedFrame, hull, -1, (0,255,0), 3)
    print (len(hull))
    i = 0;
    while i < len(hull):        
        ret = cv2.pointPolygonTest(hull[i],point,False)
        i=i+1;
        if (ret == 1):
            rect = cv2.boundingRect(hull[i-1])
            print(i)
            print(rect)
            #box = cv2.boxPoints(rect)
            #print(box)
            #box = np.int0(box)
            #cv2.drawContours(Image.frame,[box],0,(0,0,255),2)
            #cv2.imshow('frame',Image.frame)
            begin_track((rect),Image)
    

def make_contours(Image):   
    Image.grayFrame = cv2.cvtColor(Image.uneditedFrame , cv2.COLOR_BGR2GRAY) 
    Image.cannyFrame = cv2.Canny(Image.grayFrame, 250, 500)
    _, contours, _ = cv2.findContours(Image.cannyFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)    
    Image.contourFrame = cv2.drawContours(Image.uneditedFrame, contours, -1, (0,255,0), 3)
    return contours

def begin_track(box,Image):
    global tracker
    global trackerenabled
    if (trackerenabled):
        trackerenabled = 0;
        tracker = None
        tracker = cv2.TrackerMIL_create()
    trackerenabled =1;
    Image.boundingFrame = Image.uneditedFrame
    ok = tracker.init(Image.boundingFrame, box)
    
    
Camera = camera(0).start()
Image = image
trackerenabled = 0
tracker = cv2.TrackerMIL_create()
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", FindBounds)


while(True):
    if (Camera.grabbed == True):
        Image.uneditedFrame = Camera.frame
        if(trackerenabled):
            Image.boundingFrame = Image.uneditedFrame
            ok, bbox = tracker.update(Image.boundingFrame)
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(Image.boundingFrame, p1, p2, (255,0,0), 2, 1)
                cv2.imshow('Canny',Image.cannyFrame)
                cv2.imshow('Contour',Image.contourFrame)
                cv2.imshow('convexHull',Image.convexHullFrame)
                #cv2.imshow('Bounding',Image.boundingFrame)
            else :
            # Tracking failure
                cv2.putText(Image.boundingFrame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)           

        cv2.imshow('frame',Image.uneditedFrame)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Camera.stop();
            exit()
            break

