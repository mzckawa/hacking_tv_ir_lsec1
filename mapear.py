import serial

#Configuração da porta
PORTA_SERIAL = 'COM5'  
BAUD_RATE = 9600    


try:
    ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    print("Conectado! Pressione os botões do seu controle remoto.")
    print("Anote os códigos hexadecimais para cada ação.\n")

    while True:
        linha_bytes = ser.readline()
        if linha_bytes:
            # Limpa o dado recebido (ex: b'38\r\n' -> '38')
            dado_recebido = linha_bytes.decode('utf-8').strip()
            print(f"Código recebido: 0x{dado_recebido}")

except serial.SerialException as e:
    print(f"\n--- ERRO ---")
    print(f"Não foi possível abrir a porta {PORTA_SERIAL}.")
    print("Verifique se a IDE do Arduino (Monitor Serial) está fechada.")
except KeyboardInterrupt:
    print("\nMapeamento interrompido.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Porta serial fechada.")