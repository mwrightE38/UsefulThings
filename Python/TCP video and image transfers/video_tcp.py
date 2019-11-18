# Import socket module 
import socket                
import struct
import os
import io
import numpy as np
from PIL import Image
import cv2
from os.path import expanduser
global imagedir;

def mkdir_p(dir):
    if not dir:
        return
    if dir.endswith("/"):
        mkdir_p(dir[:-1])
        return
    if os.path.isdir(dir):
        return
    mkdir_p(os.path.dirname(dir))
    os.mkdir(dir)

#function to create file in path incremented by number of flights currently in path
def CreateDIR():
	global imagedir
	home = expanduser("~");
	basedir = home + "/Desktop/imagery/"
	mkdir_p(basedir)
	for i in range(1,10000):
		imagedir = os.path.join(basedir, 'flight%uimages/' % i)
		if not os.path.exists(imagedir):
			mkdir_p(imagedir)
			break

CreateDIR();

# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 5001        
print ("on"); 
# connect to the server on local computer 
s.connect(('192.168.1.128', port)) 
print ("connected");
i = 0;
size = (1024,680)
#out = cv2.VideoWriter((imagedir)+'project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15,size) 
while (True):
	data = s.recv(1024);
	print (data);
	data = (struct.unpack('<i',data))
	print (data[0])
	s.send("connected/n")
	received = 0;
	with open((imagedir+(str(i)+".jpg")), 'wb') as f:
		while (received < data[0]): 
			filedata = s.recv(1024)
			received = received + len(filedata)
		# write data to a file
			f.write(filedata)
		s.send("finished")	
		f.close()
		imgname = (imagedir+(str(i)+".jpg"));
		img = cv2.imread(imgname,1)
#		out.write(img)
        # Show images
		cv2.namedWindow('LiveView', cv2.WINDOW_AUTOSIZE)
		cv2.imshow('LiveView', img)
		cv2.waitKey(1)        
# close the connection 

#out.release()
s.close()  