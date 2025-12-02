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
    
    // --- SOLUÇÃO DE REPETIÇÃO ---
    
    // 1. Verificamos se esse sinal é apenas uma "repetição" automática do protocolo.
    // A biblioteca IRremote já sabe identificar isso. Se for repetição, ignoramos.
    if (!(IrReceiver.decodedIRData.flags & IRDATA_FLAGS_IS_REPEAT)) {
        
        // 2. Verificação extra: Se o comando for "0", geralmente é ruído ou erro de leitura.
        if (IrReceiver.decodedIRData.command != 0) {
            
            Serial.println(IrReceiver.decodedIRData.command, HEX);
            
            // 3. O Delay Mágico:
            // Pausa o Arduino por 250 milissegundos (0.25 segundos).
            // Isso impede que um "clique rápido" seja lido como dois cliques.
            // Se sentir que o controle ficou "lento", diminua para 150 ou 200.
            delay(150); 
        }
    }
    
    // Prepara para receber o próximo sinal
    IrReceiver.resume();
  }
}