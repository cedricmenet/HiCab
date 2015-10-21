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

LiquidCrystal lcd(8,9,4,5,6,7);

struct comDatas{
  String km;
  String id;
  String queue;
  String busy;
  String channel;
};

struct comDatas tmp;

int lcd_key       =  0;
int adc_key_in    =  0;
int adc_key_prev  =  0;
int incr          =  0;

byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x34, 0x15 };
IPAddress server(192,168,2,1);
char* serverAddress   =   "192.168.2.1";
int port              =   80;
String message        =   "";

EthernetClient client;
WebSocketClient client2;

void setup() {
  tmp.busy = "False";         /* On part du principe que le cab est libre de base */
  Serial.begin(9600);         
  lcd.begin(16,2);            /* initialisation du lcd */
  lcd.setCursor(0,0);
  lcd.print("   En attente   ");
  lcd.setCursor(0,1);
  lcd.print("  de connexion  ");
  Ethernet.begin(mac);
  system("etc/init.d/networking restart");
  client.connect(server,80);  /* Connexion au serveur via Ethernet */
  client.println("GET /subscribe/cab\r\n");
  delay(1000);
  
  /* -- Parse du premier message -- */
  while(client.available()){
    char c = client.read();
    message += c;
  }
  Serial.print("Le message est :");
  Serial.println(message);
  tmp = ComProcess(message,tmp);
  /* -- -- -- -- -- -- Fin du parse -- -- -- -- -- -- */
  
   /* -- Initialisation de la connexion Websocket -- */
  client2.connect("192.168.2.1",80,"","/cab_device");
  client2.onOpen(onOpen);
  client2.onMessage(onMessage);
  client2.onError(onError);
  /* -- Fin de l'initialisation de la connexion -- */

  /* Test de première reception */
  Serial.print("l'ID est : ");
  Serial.print(tmp.id);
  Serial.println(".");
  Serial.print("Le channel est : ");
  Serial.print(tmp.channel);
  Serial.println(".");
  /* Fin de test */
}

void loop() {
  client2.monitor();  /* Exécute le onOpen, onMessage et onError de sa classe */
  
  IPAddress myAddr = Ethernet.localIP(); /* Stocke l'adresse IP donné par le serveur (pour la traiter après) */
  adc_key_prev = lcd_key ;       // Looking for changes
  lcd_key = read_LCD_buttons();  // read the buttons

  if(incr==0){  /* Affiche les informations relatives aux trames reçues */
   lcd.clear();
   if(tmp.busy == "False"){
     lcd.print("Free");
   }
   else{
     lcd.print("Busy");
   }
   
   lcd.setCursor((12-(sizeof(tmp.id)/8)),0);
   lcd.print("id:");
   lcd.setCursor((15-(sizeof(tmp.id)/8)),0);
   lcd.print(tmp.id);
   lcd.setCursor(0,1);
   lcd.print("Queue:");
   lcd.print(tmp.queue);
   lcd.print("  km:");
   lcd.print(tmp.km);
  }
  else if(incr==1){ /* Menu2: Affiche l'IP donné au Galileo par le serveur */
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Mon IP HiCab :");
    lcd.setCursor(0,1);
    lcd.print(myAddr[0]);
    lcd.print(".");
    lcd.print(myAddr[1]);
    lcd.print(".");
    lcd.print(myAddr[2]);
    lcd.print(".");
    lcd.print(myAddr[3]);
  }
  else if(incr==2){ /* Why not */
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Version 1.2.34.2");
    lcd.setCursor(0,1);
    lcd.print("ISO 9000 ");
  }
  switch (lcd_key)               // depending on which button was pushed, we perform an action
  {
    case btnRIGHT:  /* Envoie l'acceptation de la première trame de la queue */
    {               /* Dans le cas où le cab n'est pas occupé et que la queue n'est pas vide */
      if(tmp.busy=="False" && tmp.queue!="0"){
        char *publishMessageC = "{\"is_accepted\":true}";
        client2.send(publishMessageC);
      }
      break;
    }
    case btnLEFT:   /* Envoie le refus de la première trame de la queue */
    {               /* Dans le cas où le cas n'est pas occupé et que la queue n'est pas vide */
      if(tmp.busy=="False" && tmp.queue!="0"){
        char *publishMessageC = "{\"is_accepted\":false}";
        client2.send(publishMessageC);
      }
      break;
    }
    case btnUP: /* Bouton Haut et Bas pour switcher entre les menus */
    {
      incr++;
      Serial.println("UP");
      if(incr==3)
        incr=0;
      break;
    }
    case btnDOWN:
    {
      incr--;
      Serial.println("DOWN");
      if(incr<0)
        incr=2;
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

/* Fonction pour lire l'état des boutons
Code repris, mais modification des valeurs */
int read_LCD_buttons(){
  adc_key_in = analogRead(0);      // read the value from the sensor 
  delay(5); //switch debounce delay. Increase this delay if incorrect switch selections are returned.
  int k = (analogRead(0) - adc_key_in); //gives the button a slight range to allow for a little contact resistance noise
  if (5 < abs(k)) return btnNONE;if (adc_key_in > 1000) return btnNONE; // We make this the 1st option for speed reasons since it will be the most likely result
  if (adc_key_in < 50)   return btnRIGHT;  
  if (adc_key_in < 220)  return btnUP; 
  if (adc_key_in < 420)  return btnDOWN; 
  if (adc_key_in < 640)  return btnLEFT; 
  if (adc_key_in < 790)  return btnSELECT;   /* N'est pas implémenté (et ne marche pas) */
  return btnNONE;  
}

/* A l'ouverture de la websocket, envoie une trame json concernant l'identifiant */
void onOpen(WebSocketClient client){
  Serial.println("onOpen");
  String idtmpS = "{\"id_cab\": ";
  char idtmpC[30];
  idtmpS += tmp.id;
  idtmpS += "}";
  idtmpS.toCharArray(idtmpC,30);
  client2.send(idtmpC);
  Serial.println(idtmpC);
}

/* Récupère les messages */
void onMessage(WebSocketClient client, char* message) {
  Serial.println("onMessage");
  Serial.println(String(message));
  tmp = ComProcess(message,tmp);
}

/* Récupère les erreurs */
void onError(WebSocketClient client, char* message) {
  Serial.println("onError");
  Serial.print("ERROR: "); Serial.println(message);
}

/* Fonction de parse */
struct comDatas ComProcess(String in,struct comDatas Datas){ 
    //struct comDatas Datas;
    
    if(in.indexOf("\'odometer\':") != -1){ 
        String tmp_in = in.substring(in.indexOf("\'odometer\':"));
        String tmp = tmp_in.substring(12, tmp_in.indexOf("}"));
        Datas.km = tmp;
    }
    if(in.indexOf("\"id_cab\":") != -1){
        String tmp_in = in.substring(in.indexOf("\"id_cab\":"));
        String tmp = tmp_in.substring(9, tmp_in.indexOf("\n")); 
        Datas.id = tmp;
    }
    if(in.indexOf("\'is_busy\':") != -1){
        String tmp_in = in.substring(in.indexOf("\'is_busy\':"));
        String tmp = tmp_in.substring(11,tmp_in.indexOf(","));
        Datas.busy = tmp;
        Serial.println(tmp);
    }
    if(in.indexOf("\"channel\":") != -1){
        String tmp_in = in.substring(in.indexOf("\"channel\":"));
        String tmp = tmp_in.substring(12,tmp_in.indexOf("\","));
        Datas.channel = tmp;
    }
    if(in.indexOf("\'queue\':") != -1){
        String tmp_in = in.substring(in.indexOf("\'queue\':"));
        String tmp = tmp_in.substring(9,tmp_in.indexOf(","));
        Datas.queue = tmp;
    }
    
    return Datas;
}
