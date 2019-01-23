import serial
import time


class Sender: 
    def __init__(self, port, baud, x,y):
        self.x = x
        self.y = y
        self.baud = baud
        self.port = port
        self.connection = None
        self.updated = None
        self.run()
        
    def connect(self):
        self.connection=serial.Serial(self.port, self.baud)
        
    def disconnect(self):
        self.connection.close()
                    
    def encode(self,x,y):
        self.send("<"+ str(self.x) + "><" +str(self.y) + ">")
        self.updated = lambda: int(round(time.time() * 1000))
        
    def send(self,message):
        self.connection.write(message)
        
    def run(self):
        self.connect()
        self.encode(self.x,self.y)
        

sender = Sender('/dev/ttyUSB0',57600,12,1);
