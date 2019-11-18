#include <SPI.h>
#include <SD.h>

const int chipselect = 10;
#define tach 7
unsigned long timenow = 0;
int pps = 0;
int RPMMax =0;
int RPMMin=9999;
int curRPM = 0;
int syncCounter = 0;
int lastState = 7;
int state = 0;
bool fileExists = false;
File datafile;



void nameAndOpen(){
  if(!SD.begin(chipselect)){
    while(1){}
  }
  
for(int i=1;;i++)
{
   String temp = "log";
   temp = temp + i + ".txt";
   char fileName[temp.length()];
   temp.toCharArray(fileName, temp.length()); 
   if(!SD.exists(fileName))
   {
      datafile = SD.open(fileName,FILE_WRITE);
      break;
   }
}

if (datafile){
  Serial.print("yes");
}
else{  Serial.print("no");}

}
void setup() {
  pinMode(tach,INPUT);
  timenow = millis();
  digitalWrite(tach,LOW);

Serial.begin(9600);

while(!Serial){

  }
nameAndOpen();
}

int calc(int pps){
  return(pps * 60);  
}

void loop() {
  
  while(1){
    
    while((timenow + 1000)  >= millis()){
          state = digitalRead(tach);
      if (state != lastState){           
        pps+=1;
        lastState = state;
      }
    }

  //increment syncCounter every second to save variable space
  syncCounter+=1;
  //convert pulses per second to minute
  curRPM = calc(pps/2);

  if (curRPM > RPMMax){

    RPMMax = curRPM;
  }
    if (curRPM > 1500 && curRPM < RPMMin){

    RPMMin = curRPM;
    
  }
  
  String data = (",RPM,");
  data = (data + curRPM + ",RPM_MAX," + RPMMax+ ",RPM_MIN," + RPMMin);
  datafile.print("TBOOT,");
  datafile.print(millis());
  datafile.println(data);

  if (syncCounter%5 == 0){
    Serial.print("TBOOT,");
    Serial.print(millis());
    Serial.println(data);
  }
  
  if (syncCounter == 5){ 
  //sync sd card to ensure no data loss occurs every 30 seconds
  syncCounter = 0;  
  datafile.flush();
  }

  pps = 0;
  timenow = millis();

  }

}
