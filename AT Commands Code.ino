#include <SoftwareSerial.h>
SoftwareSerial BTserial(9, 10); // RX | TX

//AT Commands: Help setup the bluetooth module and its certain parameters/configurations
//Serial monitor should be set to Both NL & CR and 9600 Baud
//Once running the code, the words "BTserial started, type AT, and the word OK should appear. After type the AT Command you want. 
char c=' ';
boolean NL = true;

void setup() 
{
   Serial.begin(9600);
   BTserial.begin(38400);  
   Serial.println("BTserial started ");
}

void loop()
{
    // Read from the Bluetooth module and send to the Arduino Serial Monitor
   if (BTserial.available())
   {
       c = BTserial.read();
       Serial.write(c);
   }
 
   // Read from the Serial Monitor and send to the Bluetooth module
   if (Serial.available())
   {
       c = Serial.read();
       BTserial.write(c);   

       // Echo the user input to the main window. The ">" character indicates the user entered text.
       if (NL) { Serial.print(">");  NL = false; }
       Serial.write(c);
   }
}

//
