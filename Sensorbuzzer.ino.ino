
//Include the module so we don't have to use the default Serial so the Arduino can be plugged in to a computer and still use bluetooth
#include <SoftwareSerial.h>

boolean NL = true;
int q= 0;
int buzzerPin = 13;

SoftwareSerial BTserial(9, 10);         //Tells Redboard which pins the are RX and TX from the BT module

void setup()
  {
  Serial.begin(9600);                   //Send data to the serial monitor when connected via cable
  Serial.println("Serial ready");
  BTserial.begin(38400);                //Initialize the bluetooth
  Serial.println("BTserial started ");
  pinMode(buzzerPin, OUTPUT);
  }

void loop()
  {
  q = analogRead(A0);      //Reads sensor value
  BTserial.write(q/8);     //Sends it to RX/TX pins (referenced as 9 and 10 above)
  Serial.println(q);       //Displays it on serial monitor
  delay(50);               //Pause so it's not continuous
  if (q>=550) 
    {
    tone(buzzerPin, 262);
    delay(250);
    noTone(buzzerPin);
    }
  }
