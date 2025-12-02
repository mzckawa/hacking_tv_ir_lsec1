#include <IRremote.hpp>

// Pino onde o sensor IR está conectado
#define IR_RECEIVE_PIN 11

void setup() {
  // Script Python DEVE usar essa mesma velocidade.
  Serial.begin(9600);
  
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
  
  delay(500);
}

void loop() {
  if (IrReceiver.decode()) {
    
    if (!(IrReceiver.decodedIRData.flags & IRDATA_FLAGS_IS_REPEAT)) {
        if (IrReceiver.decodedIRData.command != 0) {
            Serial.println(IrReceiver.decodedIRData.command, HEX);
            delay(150); 
        }
    }
    
    // Prepara para receber o próximo sinal
    IrReceiver.resume();
  }
}