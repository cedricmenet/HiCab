#include <WebSocketClient.h>
#include "Arduino.h"
#include <LiquidCrystal.h>
#include <Ethernet.h>
#include <SPI.h>

#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

struct comDatas{
  String km;
  String id;
  String queue;
  String busy;
  String channel;
};

struct comDatas tmp;

int lcd_key       = 0;
int adc_key_in    = 0;
int adc_key_prev  = 0;

byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x34, 0x15 };
IPAddress server(192,168,2,1);

EthernetClient client;
WebSocketClient client2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Ethernet.begin(mac);
  system("etc/init.d/networking restart");
  client.connect(server,80);
  client2.connect("192.168.2.1:80");
  client2.onOpen(onOpen);
  client2.onMessage(onMessage);
  client2.onError(onError);
  client.println("GET /subscribe/cab\r\n");
  String message = "";
  while(client.available()) {
    char c = client.read();
    message += c;
  }
  Serial.println(message);
  tmp = ComProcess(message);
  /* Test de première reception */
  Serial.print("l'ID est : ");
  Serial.print(tmp.id);
  Serial.println(".");
  Serial.print("Le channel est : ");
  Serial.print(tmp.channel);
  Serial.println(".");
  client2.send("WS.CONNECT ws://192.168.2.1/cab_device");
  /* Fin de test */
}

void loop() {

  client2.monitor();
  // put your main code here, to run repeatedly:
  adc_key_prev = lcd_key ;       // Looking for changes
  lcd_key = read_LCD_buttons();  // read the buttons

  switch (lcd_key)               // depending on which button was pushed, we perform an action
  {
  case btnRIGHT:
  {
    client2.send("jfiorezhfohrez");
    client2.monitor();
    Serial.println("btnRight");
    break;
  }
  case btnLEFT:
  {
    break;
  }
  case btnUP:
  {

    break;
  }
  case btnDOWN:
  {

      break;
    }
  case btnSELECT:
    {
      break;
    }
  case btnNONE:
    {
      break;
    }
  }
}

int read_LCD_buttons(){
  adc_key_in = analogRead(0);      // read the value from the sensor 
  delay(5); //switch debounce delay. Increase this delay if incorrect switch selections are returned.
  int k = (analogRead(0) - adc_key_in); //gives the button a slight range to allow for a little contact resistance noise
  if (5 < abs(k)) return btnNONE;if (adc_key_in > 1000) return btnNONE; // We make this the 1st option for speed reasons since it will be the most likely result
  if (adc_key_in < 50)   return btnRIGHT;  
  if (adc_key_in < 220)  return btnUP; 
  if (adc_key_in < 420)  return btnDOWN; 
  if (adc_key_in < 640)  return btnLEFT; 
  if (adc_key_in < 790)  return btnSELECT;   
  return btnNONE;  
}

void onOpen(WebSocketClient client){
  Serial.println("onClient");
  Serial.println();
}

void onMessage(WebSocketClient client, char* message) {
  Serial.println("onMessage");
  Serial.print("Received: "); Serial.println(message);
}

void onError(WebSocketClient client, char* message) {
  Serial.println("onError");
  Serial.print("ERROR: "); Serial.println(message);
}

struct comDatas ComProcess(String in){ //Pour parser le string
    struct comDatas Datas;
    
    if(in.indexOf("\"odometer\":") != -1){ 
        String tmp_in = in.substring(in.indexOf("\"odometer\":"));
        String tmp = tmp_in.substring(12, tmp_in.indexOf(","));
        Datas.km = tmp;
    }
    if(in.indexOf("\"id_cab\":") != -1){
        Serial.println("Entré");
        String tmp_in = in.substring(in.indexOf("\"id_cab\":"));
        String tmp = tmp_in.substring(10, tmp_in.indexOf("\n"));
        Datas.id = tmp;
        
    }
    if(in.indexOf("\"isBusy\":") != -1){
        String tmp_in = in.substring(in.indexOf("\"isBusy\":"));
        String tmp = tmp_in.substring(10,tmp_in.indexOf(","));
        Datas.busy = tmp;
        Serial.println(tmp);
    }
    if(in.indexOf("\"channel\":") != -1){
        String tmp_in = in.substring(in.indexOf("\"channel\":"));
        String tmp = tmp_in.substring(11,tmp_in.indexOf(','));
        Datas.channel = tmp;
    }

    return Datas;
}
