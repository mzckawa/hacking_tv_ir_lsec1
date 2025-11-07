import serial
import time

## --- CONFIGURAÇÃO (VOCÊ PRECISA MUDAR ISSO) ---
# Cole aqui os códigos (sem o '0x') que você 
# descobriu com o script 'mapeador_botoes.py'.
# Os valores abaixo são SÓ EXEMPLOS.
# ----------------------------------------------------
CODIGO_CIMA = "40"      # Mude para o seu código de "Cima"
CODIGO_BAIXO = "41"   # Mude para o seu código de "Baixo"
CODIGO_ESQUERDA = "07" # Mude para o seu código de "Esquerda"
CODIGO_DIREITA = "06"  # Mude para o seu código de "Direita"
CODIGO_ENTER = "44"     # Mude para o seu código de "Enter/OK"
CODIGO_SAIR = "5B"      # Mude para o seu código de "Sair/Power"
# ----------------------------------------------------

# --- Configuração da Porta ---
PORTA_SERIAL = 'COM3'  # Porta fixada conforme sua solicitação
BAUD_RATE = 9600     # O mesmo do Serial.begin(9600) no Arduino
# -----------------------------

# O teclado virtual, traduzido do Go
KEYBOARD_TV = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "?"],
    ["@", "z", "x", "c", "v", "b", "n", "m", ",", "."]
]

# Posição inicial (linha 2, coluna 4), que é a letra 'g'
current_position = [2, 4] 
current_char = "g"
password = [] # Lista para armazenar os caracteres "digitados"

def move_cursor(position, direction_code):
    """
    Calcula a nova posição do cursor no teclado virtual.
    """
    global KEYBOARD_TV
    
    row, col = position[0], position[1]
    
    if direction_code == CODIGO_ESQUERDA:
        col -= 1
    elif direction_code == CODIGO_DIREITA:
        col += 1
    elif direction_code == CODIGO_CIMA:
        row -= 1
    elif direction_code == CODIGO_BAIXO:
        row += 1
        
    # --- Verificação de Limites (Impede que o cursor "caia" da matriz) ---
    max_rows = len(KEYBOARD_TV)
    max_cols = len(KEYBOARD_TV[0])

    if row < 0: row = max_rows - 1 # Permite "dar a volta" por cima
    if row >= max_rows: row = 0      # Permite "dar a volta" por baixo
    
    if col < 0: col = max_cols - 1 # Permite "dar a volta" pela esquerda
    if col >= max_cols: col = 0      # Permite "dar a volta" pela direita
    # -----------------------------------------------------------------

    new_position = [row, col]
    new_char = KEYBOARD_TV[row][col]
    
    return new_position, new_char

# --- Função Principal (Tradução da 'main' do Go) ---
def main():
    global current_position, current_char, password
    
    print(f"Iniciando serIR (Python)... Conectando em {PORTA_SERIAL}")
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
        print("Conectado! Use os botões direcionais do controle.")
        print(f"Posição Inicial: {current_position} -> '{current_char}'")

        while True:
            linha_bytes = ser.readline()
            if not linha_bytes:
                continue # Pula se não recebeu nada (timeout)
                
            received_code = linha_bytes.decode('utf-8').strip().upper() # .upper() para garantir
            
            # É um botão direcional?
            if received_code in [CODIGO_CIMA, CODIGO_BAIXO, CODIGO_ESQUERDA, CODIGO_DIREITA]:
                current_position, current_char = move_cursor(current_position, received_code)
                print(f"Posição: {current_position}  Tecla: '{current_char}'")
            
            # É o botão de ENTER?
            elif received_code == CODIGO_ENTER:
                password.append(current_char)
                print(f"--- ENTER! --- Letra '{current_char}' adicionada.")
                print(f"Senha atual: {''.join(password)}")
            
            # É o botão de SAIR?
            elif received_code == CODIGO_SAIR:
                print("\n--- SAINDO ---")
                print(f"A senha final capturada foi: {''.join(password)}")
                break # Sai do loop while
                
            # Ignora qualquer outro botão
            else:
                pass # Não faz nada com códigos desconhecidos

    except serial.SerialException as e:
        print(f"\n--- ERRO ---")
        print(f"Não foi possível abrir a porta {PORTA_SERIAL}.")
        print("Verifique se a IDE do Arduino (Monitor Serial) está fechada.")
    except KeyboardInterrupt:
        print("\nPrograma interrompido.")
        if password:
            print(f"A senha capturada foi: {''.join(password)}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Porta serial fechada.")

# Inicia o programa
if __name__ == "__main__":
    main()