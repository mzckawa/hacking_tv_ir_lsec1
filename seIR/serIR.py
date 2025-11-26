import serial
import time

# --- Seus Códigos IR (Exemplos) ---
CODIGO_CIMA = "58"
CODIGO_BAIXO = "59"
CODIGO_ESQUERDA = "5A"
CODIGO_DIREITA = "5B"
CODIGO_CONFIRM = "5C" # Botão confirmar
CODIGO_SAIR = "A"   # Botão de voltar

# --- Configuração da Porta ---
PORTA_SERIAL = 'COM4' 
BAUD_RATE = 9600

# --- Teclas Especiais (Constantes para facilitar a lógica) ---
KEY_SPACE = "[ESP]"
KEY_BACKSPACE = "[DEL]"
KEY_ENTER = "[ENTER]"
KEY_CAPSLOCK = "[CAPS]"
KEY_KEYBOARD_SWITCH = "[SWITCH]"
KEY_KEYBOARD_SPECIAL = "[SWITCH_SPECIAL]"
KEY_DOTCOM = "[.COM]"

# --- Layout do Teclado Virtual ---
# Adicionei uma nova linha com as teclas especiais
MAIN_KEYBOARD_TV = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", KEY_ENTER],
    ["z", "x", "c", "v", "b", "n", "m", "!", "?"],
    [KEY_KEYBOARD_SWITCH, "/", KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, ".", KEY_DOTCOM] # Linha de Comandos
]

# --- Teclado com chars especias e numericos ---
SPECIAL_KEYBOARD1_TV = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "8", "9"],
    ["@", "#", "$", "%", "&", "-", "+", "(", ")", KEY_ENTER],
    [KEY_KEYBOARD_SPECIAL, "\\", "=", "*", "'", ":", ";", "!", "?", KEY_KEYBOARD_SPECIAL],
    [KEY_KEYBOARD_SWITCH, ",", "_", KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, "/", ".", KEY_DOTCOM]
]

# Tem outro teclado especial porém com teclas que não são muito comuns, a configuração dele é indentica ao "SPECIAL_KEYBOARD1_TV" apenas trocando os chars
# Por isso decidimos por apenas replicar o outro teclado para podermos manter o tracking da posição e para casos decidirmos colocar o outro teclado no futuro
SPECIAL_KEYBOARD2_TV = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "8", "9"],
    ["@", "#", "$", "%", "&", "-", "+", "(", ")", KEY_ENTER],
    [KEY_KEYBOARD_SPECIAL, "\\", "=", "*", "'", ":", ";", "!", "?", KEY_KEYBOARD_SPECIAL],
    [KEY_KEYBOARD_SWITCH, ",", "_", KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, KEY_SPACE, "/", ".", KEY_DOTCOM]
]

# Posição inicial
KEYBOARD_TV = MAIN_KEYBOARD_TV
current_position = [0,0]
current_char = KEYBOARD_TV[0][0]
password = [] 


def move_cursor(position, direction_code):
    global KEYBOARD_TV

    row, col = position[0], position[1]
    max_rows = len(KEYBOARD_TV)
    
    # Movimentação Básica ---
    if direction_code == CODIGO_CIMA:
        
        # saindo da linha 1 e indo para cima, os elementos da coluna i vão para as colunas i+1
        if row == 1:
            col += 1 

        # tratamento da movimentação para cima a partir da tecla de espaço
        elif row == 3 and col in (3, 4, 5, 6, 7):
            col = 3 

        # em todas as situações, a linha diminui em 1, então deixamos o comando abaixo fora das condicionais anteriores
        row -= 1

    elif direction_code == CODIGO_BAIXO:

        # tratamento da movimentação para baixo partindo da linha zero 
        if row == 0:
            if col == 0:
                row += 1 # aumenta uma linha, indo para a coluna zero dela (ou seja, col se mantém)
                
            else: 
                col -= 1 # aumenta uma linha, mas, partindo da coluna i, vai para a coluna i-1 da linha de baixo

        # em todas as situações, a linha aumenta em 1, então deixamos o comando abaixo fora das condicionais anteriores
        row += 1
        
    elif direction_code == CODIGO_ESQUERDA:
        col -= 1
    elif direction_code == CODIGO_DIREITA:
        col += 1

    # --- Tratamento de Limites de Colunas (ESQUERDA/DIREITA) ---
    # Importante: O tamanho da coluna depende da linha atual!
    # O teclado da TVBOX utilizada para demonstração tem um comportamento onde caso passemos o limite de colunas o cursor vai para uma outra linha
    # Se o limite for quebrado para a direita, o cursor vai para linha de baixo na primeira coluna
    # Caso o limte for quebrado para a esquerda, o cursor vai para a linha acima na ultima coluna
    current_row_length = len(KEYBOARD_TV[row])
    if col < 0:
        row -= 1
        current_row_length = len(KEYBOARD_TV[row])
        col = current_row_length - 1 # Vai para o fim da linha
    elif col >= current_row_length:
        col = 0 # Vai para o início da linha
        row +=1 

    # --- Tratamento de Limites de Linhas (CIMA/BAIXO) ---
    if row < 0: 
        row = 0
    elif row >= max_rows: 
        row = max_rows - 1
        
    # --- Correção de Coluna ao mudar de linha ---
    # Se você estava na coluna N da linha de letras e desceu 
    # para uma linha que tenha n itens onde n < N
    # precisamos "puxar" o cursor para o último item válido.
    if col >= len(KEYBOARD_TV[row]):
        col = len(KEYBOARD_TV[row]) - 1

    new_position = [row, col]
    new_char = KEYBOARD_TV[row][col]
    
    return new_position, new_char

def main():
    global current_position, current_char, password
    flag_caps = False
    
    print(f"Iniciando serIR (Python)... Conectando em {PORTA_SERIAL}")
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
        print("Conectado! Aguardando comandos...")
        print(f"Posição Inicial: {current_position} -> '{current_char}'")

        while True:
            linha_bytes = ser.readline()
            if not linha_bytes:
                continue 
                
            received_code = linha_bytes.decode('utf-8').strip().upper()
            
            # --- 1. Navegação ---
            if received_code in [CODIGO_CIMA, CODIGO_BAIXO, CODIGO_ESQUERDA, CODIGO_DIREITA]:
                current_position, current_char = move_cursor(current_position, received_code)
                print(f"Posição: {current_position} | Seleção: '{current_char}'")
            
            # --- 2. Seleção (Botão de Ação do Controle) ---
            elif received_code == CODIGO_CONFIRM:
                
                # Verifica se é uma tecla especial
                if current_char == KEY_SPACE:
                    password.append(" ")
                    print(">> Espaço inserido.")
                
                elif current_char == KEY_BACKSPACE:
                    if len(password) > 0:
                        removed = password.pop()
                        print(f">> Caractere '{removed}' apagado.")
                    else:
                        print(">> Nada para apagar.")
                
                elif current_char == KEY_ENTER:
                    print("\n" + "="*30)
                    print(f"SENHA FINALIZADA: {''.join(password)}")
                    print("="*30 + "\n")
                    break # Encerra o programa

                elif current_char == KEY_DOTCOM:
                    password.append(".com")
                    print(">>'.com' inserido")

                elif current_char == KEY_CAPSLOCK:
                    if flag_caps == False:
                        flag_caps = True
                        # Volta para a posição inicial
                        current_position[0, 0]
                        current_char = KEYBOARD_TV[0][0]
                        continue
                    else:
                        flag_caps = False

                # --- Logica para troca de matriz para os teclados ---

                elif current_char == KEY_KEYBOARD_SWITCH:
                    if KEYBOARD_TV == MAIN_KEYBOARD_TV:
                        KEYBOARD_TV = SPECIAL_KEYBOARD1_TV
                    else:
                        KEYBOARD_TV = MAIN_KEYBOARD_TV
                    # Volta para a posição inicial
                    current_position[0, 0]
                    current_char = KEYBOARD_TV[0][0]

                # --- Logica para troca entre os teclados especiais ---
                elif current_char == KEY_KEYBOARD_SPECIAL:
                    if KEYBOARD_TV == SPECIAL_KEYBOARD1_TV:
                        KEYBOARD_TV = SPECIAL_KEYBOARD2_TV
                    else:
                        KEYBOARD_TV = SPECIAL_KEYBOARD1_TV
                    # Volta para a posição inicial
                    current_position[0, 0]
                    current_char = KEYBOARD_TV[0][0]


                # É um caractere comum
                else:
                    if flag_caps:
                        current_char = current_char.upper()
                    password.append(current_char)
                    print(f">> Letra '{current_char}' adicionada.")
                    if flag_caps:
                        current_char = current_char.lower()

                if flag_caps:
                    flag_caps = False

                # Mostra o estado atual da senha
                print(f"Buffer Atual: [{''.join(password)}]")
            
            # --- 3. Botão Sair (Abortar) ---
            elif received_code == CODIGO_SAIR:
                print("\n--- Cancelado pelo usuário ---")
                break 

    except serial.SerialException:
        print(f"\nErro: Não foi possível abrir a porta {PORTA_SERIAL}.")
    except KeyboardInterrupt:
        print("\nPrograma interrompido via teclado.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    main()