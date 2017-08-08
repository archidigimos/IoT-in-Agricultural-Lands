#include <SimpleTimer.h>
SimpleTimer timer;
int flag = 0;

long randNumber;
String sensor1;
String sensor2;
String sensor3;
String sensor4;

String sensor_reading;

void sendDatatoESP()
{
  randNumber = random(1024);
  sensor1 = String(randNumber);
  randNumber = random(1024);
  sensor2 = String(randNumber);
  randNumber = random(1024);
  sensor3 = String(randNumber);
  randNumber = random(1024);
  sensor4 = String(randNumber);
  
  sensor_reading = "DATA-SENSOR1-"+sensor1+"-"+sensor2+"-"+sensor3+"-"+sensor4;
  if(flag==1)Serial.println(sensor_reading);
}

void serialReceive()
{
  String str = "";
  while(Serial.available()>0)
  {
    char temp = (char)Serial.read();
    str += temp;
    delay(10);
  }
  if(str != "")
  {
    if(str==String("Connected")){Serial.println("LOGIN-SENSOR1");flag=1;}
    else if(str==String("Disconnected"))flag=0;
  }
}

void setup() 
{
  Serial.begin(115200);
  timer.setInterval(5000, sendDatatoESP);
  randomSeed(analogRead(A0));
}

void loop() 
{
  serialReceive();
  timer.run();
}
