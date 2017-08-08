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
String sensor3;
String sensor4;


String data_received;
int connectedWS = 0;

void sendData_WS() {

  if(connectedWS==1){
    
  randNumber = random(1024);
  sensor1 = String(randNumber);
  randNumber = random(1024);
  sensor2 = String(randNumber);
  randNumber = random(1024);
  sensor3 = String(randNumber);
  randNumber = random(1024);
  sensor4 = String(randNumber);
  
  sensor_reading = "DATA-SENSOR1-"+sensor1+"-"+sensor2+"-"+sensor3+"-"+sensor4;
  webSocket.sendTXT(sensor_reading);
  }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t lenght) {


    switch(type) {
        case WStype_DISCONNECTED:
        {
          connectedWS = 0;
        }
            break;
        case WStype_CONNECTED:
            {
                webSocket.sendTXT("LOGIN-RPI3_1");
                connectedWS = 1;
            }
            break;
        case WStype_TEXT:
            data_received=(char *)payload;
            Serial.println(data_received);
            break;
        case WStype_BIN:
            hexdump(payload, lenght);
            break;
    }

}

void setup() {
    USE_SERIAL.begin(115200);
    timer.setInterval(5000, sendData_WS);
  
    WiFiMulti.addAP("Micromax A106", "micromax264");

    while(WiFiMulti.run() != WL_CONNECTED) {
        delay(100);
    }

    webSocket.begin("sp.ebiw.com", 9000);
    webSocket.onEvent(webSocketEvent);
    pinMode(actuator, OUTPUT);

    randomSeed(analogRead(A0));
}

void loop() {
    webSocket.loop();
    timer.run();
}
