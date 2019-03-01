import os
import sys
import argparse
import numpy as np
import cv2




img = cv2.imread('grey.tif',0)

img2 = cv2.imread('grey.tif',0)

min = np.amin(img)
max = np.amax(img)
print min
print max

cv2.convertScaleAbs(img,img,255/(max-min),-255*min/(max-min))

overlay = cv2.applyColorMap(img, 9)
overlay2 = cv2.applyColorMap(img2, cv2.COLORMAP_BONE)
 
scale_percent = 400 

# percent of original size

width = int(overlay.shape[1] * scale_percent / 100)
height = int(overlay.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(overlay, dim, interpolation = cv2.INTER_AREA) 

width = int(overlay2.shape[1] * scale_percent / 100)
height = int(overlay2.shape[0] * scale_percent / 100)
dim = (width, height)


# resize image
resized2 = cv2.resize(overlay2, dim, interpolation = cv2.INTER_AREA) 

images = np.hstack((resized, resized2))


cv2.imshow('both',images)
cv2.waitKey(0)
cv2.destroyAllWindows()
