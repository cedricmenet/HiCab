#include <WebSocketClient.h>

#include <LiquidCrystal.h>
#include <Ethernet.h>
#include <SPI.h>

LiquidCrystal lcd(8,9,4,5,6,7);

#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

int lcd_key       = 0;
int adc_key_in    = 0;
int adc_key_prev  = 0;

byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x34, 0x15 };
//IPAddress server(192,168,10,1);
char server[] = "www.google.com";
IPAddress ip(192,168,10,2);

EthernetClient client;
WebSocketClient client2;

struct comDatas{
  String km;
  String id;
  String queue;
  String busy;
};

void setup(){
    lcd.begin(16,2);        //initialisation du lcd
    Serial.begin(9600);     //initialisation du terminal
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("   En attente   ");
    lcd.setCursor(0,1);
    lcd.print("  de connexion  ");
    lcd.display();
    Ethernet.begin(mac,ip); //Affecte l'adresse IP au Galileo
    Serial.println("Affectation réussie");
    delay(1000);
    client2.connect(server);
    Serial.println("Did it !");
    client2.onOpen(onOpen);
//    client2.onMessage(onMessage);
//    client2.onError(onError);
    if(client.connect(server,80)){
      Serial.println("Connected");
    }
    else{
      Serial.println("Connection failed");
    }
}

void loop(){
  Serial.println("Waiting a message");
  //while(Serial.read()<=0){}
  adc_key_prev = lcd_key ;       // Looking for changes
  lcd_key = read_LCD_buttons();  // read the buttons

  switch (lcd_key)               // depending on which button was pushed, we perform an action
  {
  case btnRIGHT:
    {
      break;
    }
  case btnLEFT:
    {
      break;
    }
  case btnUP:
  case btnDOWN:
    {
      IPAddress myAddr = Ethernet.localIP();
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Mon IP HiCab :");
      lcd.setCursor(0,1);
      byte first_octet = myAddr[0];
      byte second_octet = myAddr[1];
      byte third_octet = myAddr[2];
      byte fourth_octet = myAddr[3];
      //String monIP = first_octet + "." + second_octet + "." + third_octet + "." + fouth_octet;
      lcd.print(first_octet);
      lcd.setCursor(3,1);
      lcd.print(".");
      lcd.setCursor(4,1);
      first_octet = myAddr[1];
      lcd.print(first_octet);
      lcd.setCursor(7,1);
      lcd.print(".");      
      lcd.setCursor(8,1);
      first_octet = myAddr[2];
      lcd.print(first_octet);
      lcd.setCursor(11,1);
      lcd.print(".");
      lcd.setCursor(12,1);
      first_octet = myAddr[3];
      lcd.print(first_octet);
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
  
  struct comDatas tmp = ComProcess(Serial.readString());
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("km:");
  lcd.setCursor(3,0);
  lcd.print(tmp.km);
  lcd.setCursor(0,1);
  lcd.print("id:");
  lcd.setCursor(3,1);
  lcd.print(tmp.id);
  lcd.setCursor(12,0);
  if(tmp.busy == "false")
  {
    lcd.print("FREE");
  }
  else
  {
    lcd.print("BUSY");
    Serial.println(tmp.busy);
  }

  lcd.setCursor(13,1);
  lcd.print(tmp.queue);
}

struct comDatas ComProcess(String in){ //Pour parser le string
    struct comDatas Datas;
    
    if(in.indexOf("\"odometer\":") != -1){ 
        String tmp_in = in.substring(in.indexOf("\"odometer\":"));
        String tmp = tmp_in.substring(12, tmp_in.indexOf(";"));
        Datas.km = tmp;
    }
    if(in.indexOf("\"idCab\":") != -1){
        String tmp_in = in.substring(in.indexOf("\"idCab\":"));
        String tmp = tmp_in.substring(9, tmp_in.indexOf(";"));
        Datas.id = tmp;
    }
    if(in.indexOf("\"isBusy\":") != -1){
        String tmp_in = in.substring(in.indexOf("\"isBusy\":"));
        String tmp = tmp_in.substring(10,tmp_in.indexOf(";"));
        Datas.busy = tmp;
        Serial.println(tmp);
    }

    return Datas;
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
  Serial.println("Example: onOpen()");
}

void onMessage(){
  
}

void onError(){
  
}

