
//Include the module so we don't have to use the default Serial so the Arduino can be plugged in to a computer and still use bluetooth
#include <SoftwareSerial.h>

//Variable to store input value initialized with arbitrary value
//char k = 'A';
//char c=' ';

boolean NL = true;
int q= 0;

SoftwareSerial BTserial(9, 10); // RX | TX  //Tells Redboard which pins the BT module is connected to

void setup() {                          //Initialize serial for debugging purposes
  Serial.begin(9600);
  Serial.println("Serial ready");
  BTserial.begin(38400);                //Initialize the bluetooth
  Serial.println("BTserial started ");
}

void loop() {
  q = analogRead(A0);      //Reads sensor value
  BTserial.write(q/8);       //Sends it to RX/TX pins (refernced as 9 and 10 above)
  Serial.println(q);       //Displays it on serial monitor
  delay(50);                          //Pause so it's not continuous
}
