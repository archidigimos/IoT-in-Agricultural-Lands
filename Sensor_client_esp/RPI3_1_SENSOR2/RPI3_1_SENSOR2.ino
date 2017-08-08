#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <WebSocketsClient.h>

#include <Hash.h>
#include <SimpleTimer.h>
SimpleTimer timer;

ESP8266WiFiMulti WiFiMulti;
WebSocketsClient webSocket;

long randNumber;

#define USE_SERIAL Serial
String sensor1;
String sensor2;

String sensor_reading;
String data_received;
int analog = 0;
#define actuator 4

void sendData_WS() {
  //analog = analogRead(A0);
  //sensor_reading = String(analog);

  randNumber = random(1024);
  sensor1 = String(randNumber);
  randNumber = random(1024);
  sensor2 = String(randNumber);
  
  sensor_reading = "DATA-SENSOR2-"+sensor1+"-"+sensor2;
  webSocket.sendTXT(sensor_reading);
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t lenght) {


    switch(type) {
        case WStype_DISCONNECTED:
            break;
        case WStype_CONNECTED:
            {
                webSocket.sendTXT("LOGIN-SENSOR2");
            }
            break;
        case WStype_TEXT:
            data_received=(char *)payload;
            if(data_received=="on"){webSocket.sendTXT("DATA-SENSOR2-3000");USE_SERIAL.println("Switched on");digitalWrite(actuator, HIGH);}
            else if(data_received=="off"){webSocket.sendTXT("DATA-SENSOR2-2000");USE_SERIAL.println("Switched off");digitalWrite(actuator, LOW);}
            break;
        case WStype_BIN:
            hexdump(payload, lenght);
            break;
    }

}

void setup() {
    USE_SERIAL.begin(115200);
    timer.setInterval(5000, sendData_WS);
  
    WiFiMulti.addAP("SNR_Arvind-Pi", "raspberry");

    while(WiFiMulti.run() != WL_CONNECTED) {
        delay(100);
    }

    webSocket.begin("172.24.1.1", 9000);
    webSocket.onEvent(webSocketEvent);
    pinMode(actuator, OUTPUT);

    randomSeed(analogRead(A0));
}

void loop() {
    webSocket.loop();
    timer.run();
}
