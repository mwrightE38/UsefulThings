import pyrealsense2 as rs
import cv2
import numpy as np
import math
#intel camera resolution variables.
DresX =640
DresY =480
DFPS =15
CresX =640
CresY =480
CFPS =15
	
def Init():
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, DresX, DresY, rs.format.z16, DFPS)
	config.enable_stream(rs.stream.color, CresX, CresY, rs.format.bgr8, CFPS)
	pipeline.start(config)
	return pipeline;

def GetFrames(pipeline):
	align = rs.align(rs.stream.color)
	frames = pipeline.wait_for_frames()
	aligned_frames = align.process(frames)
	depth_frame = aligned_frames.get_depth_frame()
	color_frame = aligned_frames.get_color_frame()
	return  color_frame,depth_frame 



def GetImage(frame):
	return np.asanyarray(frame.get_data())

def GetImages(frame1,frame2):
	return np.asanyarray(frame1.get_data()),np.asanyarray(frame2.get_data())

def GetDepth(frame,x,y):
	return (frame.get_distance(int(x), int(y)))

def calc_xP(x):
	return ((-1) * (CresX/2 - x))

def calc_yP(y):
	return ((CresY/2 - y))

def calc_hP(x,y):
	return (math.sqrt((math.pow(CresX/2 - x,2)) + (math.pow(CresY/2 - y,2))))

def calcAngleA(xP,hP):
	return math.degrees((math.asin(xP/hP)))
	
def calcAngleB(yP,hP):
	return math.degrees((math.asin(yP/hP)))

def calc_camera_angle(x,y,hP):
	m = (math.sqrt(math.pow(CresX,2) + math.pow(CresY,2)))
	degPerPix = 77/m;
	return hP * degPerPix  

def calcOpposite(depth,angle):
	dist = (math.sin(math.radians(angle))) * depth
	return dist

#Required::x=x coordinate in an image
#Required::y=y coordinate in an image
#Required::depth_frame = depth frame from an intelrealsense camera
#Returns::xM=x distance in meters from the camera reference frame
#Returns::yM=y distance in meters from the camera reference frame
#Returns::Depth=z distance in meters from the camera reference frame
#Use::High level use of camera to get distances
def calcXY(x,y,depth_frame):
	xP = calc_xP(x)
	yP = calc_yP(y)
	hP = calc_hP(x,y)
	dist = depth_frame.get_distance(int(x), int(y))
	angle = calc_camera_angle(int(x),int(y),hP)
	A = calcAngleA(xP,hP)
	B = calcAngleB(yP,hP)
	hM = calcOpposite(dist,angle)
	xM = calcOpposite(hM,A)
	yM = calcOpposite(hM,B)
	return(xM,yM,dist)