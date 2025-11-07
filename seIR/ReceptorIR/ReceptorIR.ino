#include <IRremote.hpp>

// Pino onde o sensor IR está conectado
#define IR_RECEIVE_PIN 11

void setup() {
  // Script Python DEVE usar essa mesma velocidade.
  Serial.begin(9600);
  
  // Inicia o receptor
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
  
  delay(500);
}

void loop() {
  if (IrReceiver.decode()) {
    
    // Envia APENAS o código do comando, em formato HEXADECIMAL.
    // O "println" envia o número e uma quebra de linha (\n),
    // o que é perfeito para o Python ler com "readline()".
    Serial.println(IrReceiver.decodedIRData.command, HEX);
    
    IrReceiver.resume();
  }
}