/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */

#define IBUFF_LEN 50
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;
int rbytes=0; // bytes read
byte ibuff[IBUFF_LEN];


// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);     
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  if(Serial.available() > 0) { 
    rbytes=Serial.readBytes(ibuff,IBUFF_LEN);
    String mystring= String((char *) ibuff);
    Serial.print("ho ricevuto:");
    Serial.print(mystring);
    Serial.print("\n");
  }
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)

  delay(1000);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW

  Serial.print("id=ID0001;ext_temp=107;body_temp=026876;opt=RESERVED\n");
  
  delay(1000);  // wait for a second
  
}
