# Import socket module 
import socket                
import struct
import os  
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
port = 4001         
  
# connect to the server on local computer 
s.connect(('192.168.1.128', port)) 

i = 0;
while (True):
	data = s.recv(1024);
	print (data);
	data = (struct.unpack('<i',data))
	print (data[0])
	s.send("connected/n")
	received = 0;
	with open((imagedir+(str(i)+".jpg")), 'wb') as f:
		i = i+ 1
		print ('file opened');
		print('receiving data...');
		while (received < data[0]): 
			filedata = s.recv(1024)
			received = received + len(filedata)
		# write data to a file
			f.write(filedata)
		s.send("finished")	
		f.close()
# close the connection 

s.close()  