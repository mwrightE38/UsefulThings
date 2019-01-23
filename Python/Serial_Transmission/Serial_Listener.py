import threading
import queue
import time
import re
import serial

class Listener: 
    def __init__(self, port, baud, thread_name):
        self.x = None
        self.y = None
        self.baud = baud
        self.port = port
        self.connection = None
        self.thread = None
        self.updated = None
        self.run()
        
    def connect(self):
        self.connection=serial.Serial(self.port, self.baud)
        
    def disconnect(self):
        self.connection.close()
        
    def wait_for_update(self):
        while (True):
            if(self.connection.inWaiting() != 0):
                self.decode(self.connection.read(self.connection.inWaiting()))
            
    def decode(self,bufferData):
        print(bufferData)
        bufferData = re.findall('<(.+?)>', bufferData)
        self.x = bufferData[0]
        self.y = bufferData[1]
        self.updated = lambda: int(round(time.time() * 1000))
        
    def start_thread(self,name):
        self.thread = threading.Thread(target=self.wait_for_update,name=name)
        self.thread.dameon = True
        self.thread.start()
        
    def run_on_update(self):
        print("X is",self.x,"Y is",self.y)
    
    def run(self):
        self.connect()
        self.start_thread("receive_data")
        
        
def main():
    listener = Listener('com15',57600,"receive_data")
    lastUpdate = listener.updated
    
    while (True):    
        if (listener.updated != lastUpdate):
            listener.run_on_update()
            lastUpdate = listener.updated


main()   
