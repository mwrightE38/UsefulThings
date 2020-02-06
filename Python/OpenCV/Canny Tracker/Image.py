import cv2

class image:
    def __init__(self, src):
        self.uneditedFrame = None
        self.cannyFrame = None
        self.contourFrame = None
        self.boundingFrame = None
        self.grayFrame = None
        self.convexHullFrame = None
        