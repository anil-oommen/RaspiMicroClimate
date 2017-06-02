/*
 * Recieve IR Details and Sent to Serial in the Format required 
 * for RaspiClimate 
 * 
 * IRemote Copyright Details. 
 * 
 * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */

#include <IRremote.h>
 
int RECV_PIN = 11;

IRrecv irrecv(RECV_PIN);

decode_results results;

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}
int LED_TOGGLE_ON =0;

void loop() {
  if (irrecv.decode(&results)) {
    Serial.print("IR/bin[");
    String IRValues = String(results.value,BIN);
    Serial.print(IRValues);
    Serial.println("]");
    irrecv.resume(); // Receive the next value
    if(LED_TOGGLE_ON == 0){
      digitalWrite(LED_BUILTIN, HIGH);
      LED_TOGGLE_ON =1;
    }else{
      digitalWrite(LED_BUILTIN, HIGH);
      LED_TOGGLE_ON =0;
    }
  }
}



