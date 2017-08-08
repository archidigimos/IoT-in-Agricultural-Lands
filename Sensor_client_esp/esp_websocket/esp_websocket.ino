#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <WebSocketsClient.h>

#include <Hash.h>
ESP8266WiFiMulti WiFiMulti;
WebSocketsClient webSocket;

void serialReceive()
{
  String str = "";
  while(Serial.available()>0)
  {
    char temp = (char)Serial.read();
    if(temp!='\n')
    str += temp;
    delay(10);
  }
  if(str != "")
  {
    webSocket.sendTXT(str);
  }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t lenght) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("Disconnected");
            break;
        case WStype_CONNECTED:
            {
              Serial.println("Connected");
              webSocket.sendTXT("connected");
            }
            break;
        case WStype_TEXT:
            Serial.println((char *)payload);
            webSocket.sendTXT("ping");
            break;
        case WStype_BIN:
            hexdump(payload, lenght);
            break;
    }
}

void setup() {
    Serial.begin(115200);
  
    WiFiMulti.addAP("ESP_Websocket", "");

    while(WiFiMulti.run() != WL_CONNECTED) {
        delay(100);
    }

    webSocket.begin("ws://192.168.4.1", 9000);
    webSocket.onEvent(webSocketEvent);
}

void loop() {
    webSocket.loop();
    serialReceive();
}
