from win10toast import ToastNotifier
import pyautogui as pag
import pytesseract
import shutil
import time
import sys
import os

# Configurações
DIR_ORIGEM = r'C:\Users\ealmeida\Desktop\CADASTRO 08.01.2025'  #DIGITE AQUI O CAMINHO DO DIRETORIO DE ORIGEM ✅
DIR_TESSERACT = r'C:\Users\ealmeida\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
OFFSET_X = 40
OFFSET_Y = 5
OFFSET_UPLOAD_X = 142
OFFSET_UPLOAD_Y = 4

#coordenadas dos elementos da tela
LUPA = (1433, 180)
LINK_GCPJ = (378, 586)
PESQUISA_INPUT = (728, 339)
PRIMEIRO_ARQUIVO = (431, 263)
NOME_DA_PASTA = (902, 501)
ANEXOS_AREA =(991, 517)
PONTO_NEUTRO = (398, 379)

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = DIR_TESSERACT

diretorio_feito = os.path.join(DIR_ORIGEM, 'Anexos feitos')
itens = os.listdir(DIR_ORIGEM)
diretorios_filhos = [item for item in itens if os.path.isdir(os.path.join(DIR_ORIGEM, item))]

# Cria o diretório "Anexos feitos" se não existir
os.makedirs(diretorio_feito, exist_ok=True)

mensagem = ToastNotifier()

def capturar_tela():
    try:
        time.sleep(1)
        screenshot = pag.screenshot()
        screenshot.save("screenshot.png")
        print("\nCaptura de tela salva como screenshot.png\n")
        text = pytesseract.image_to_string(screenshot)
        return screenshot, text
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        sys.exit(1)

def mover(coordenadaX, coordenadaY):
    try:
        pag.moveTo(coordenadaX, coordenadaY, duration=.5)
        pag.click()
    except Exception as e:
        print(f"Erro ao mover o mouse: {e}")
        sys.exit(1)

#encontra as coordenadas da palavra na tela
def encontrar_palavra(text, palavra, boxes):
    for i in range(len(boxes['text'])):
        if boxes['text'][i].lower() == palavra.lower():
            return (boxes['left'][i], boxes['top'][i])
    return None

#procura o botão pra seguir para a página de anexos
def scroll_down():
    pag.click(PONTO_NEUTRO, duration=.5)
    time.sleep(1.5)
    pag.scroll(-5500)
    time.sleep(.5)
    pag.scroll(150)

#clica no ícone de subir arquivos
def subir_documento(coordenadaX, coordenadaY):
    pag.moveTo(coordenadaX, coordenadaY, duration=.5)
    pag.click()

def fechar_janela():
    pag.click(957, 514, duration=.5)
    time.sleep(1)
    pag.hotkey("alt", "f4")

def arrastar(nome_gcpj):
    try:
        time.sleep(.1)
        os.startfile(DIR_ORIGEM+'/'+ nome_gcpj) #abre o diretorio dos anexos
        time.sleep(2)
        pag.click(957, 514, duration=.5)
        pag.hotkey("ctrl", "a")
        pag.moveTo(PRIMEIRO_ARQUIVO, duration=.5)
        time.sleep(1)
        pag.mouseDown()
        time.sleep(.5)
        pag.moveTo(ANEXOS_AREA, duration=.5)
        pag.hotkey("alt", "tab")
        time.sleep(0.5)  # Pequena pausa antes de soltar o mouse
        pag.mouseUp()
        time.sleep(5)
        pag.hotkey("alt", "tab")
        fechar_janela()
        pag.click(LUPA, duration=.5)
        
    except Exception as e:
        print(f"Erro durante o arrasto: {e}")
        mensagem.show_toast("ERROR", f"Erro durante o arrasto: {str(e)}", duration=2)
        raise

def verificar_diretorio():
    try:
        caminho = DIR_ORIGEM+'/'+ nome_gcpj
        itens = os.listdir(caminho)
        if len(itens) > 0:
            print("="*80)
            print(f"\nDiretório {nome_gcpj} contém {len(itens)} itens")
            return True
        else:
            mensagem.show_toast("Aviso", f"Diretório {nome_gcpj} está vazio", duration=2)
            print(f"Diretório {nome_gcpj} está vazio")
            return False
    except Exception as e:
        print(f"Erro ao verificar diretório: {e}")
        return False

def ponteiro_de_anexos():
    for i in range(len(diretorios_filhos)):
        try:
            diretorio = diretorios_filhos[i] #escolhe um diretorio
            global nome_gcpj
            nome_gcpj = diretorio #nome do diretorio

            #checa se é o diretório de um GCPJ
            if nome_gcpj.isnumeric():
                pass
            else:
                mensagem.show_toast("ERRO:",f"Diretorio {nome_gcpj} não é um GCPJ válido", duration=2)
                print(f"Diretorio {nome_gcpj} não é um GCPJ válido")
                print("Finalizando a tarefa...\n\n")
                break
            
            time.sleep(.5)
            #verificar_diretorio()
            if verificar_diretorio() == True:
                main() #rodar o robo
                # Move o diretório processado para o diretório "Anexos feitos" 
                shutil.move(os.path.join(DIR_ORIGEM, diretorio), diretorio_feito)
                print(f"\nDiretório {diretorio} concluído e movido para {diretorio_feito}\n")
                print(f'Restam {len(diretorios_filhos)-(int(i)-1)} diretórios para processar')
            else:
                mensagem.show_toast("Erro:",f"Diretorio {nome_gcpj} está vazio", duration=2)
                print(f"Diretório {nome_gcpj} está vazio")
                
                # Move o diretório processado para o diretório "Anexos Vazios" 
                diretorio_vazio = os.path.join(DIR_ORIGEM, 'Anexos Vazios')
                os.makedirs(diretorio_vazio, exist_ok=True)
                shutil.move(os.path.join(DIR_ORIGEM, diretorio), diretorio_vazio)

                print(f"\nDiretório {diretorio} movido para {diretorio_vazio}\n")
                print("="*80)
            
        except Exception as e:
            mensagem.show_toast("ERROR",f"Erro ao processar o diretório {diretorio}", duration=2)
            print(f"Erro ao processar o diretório {diretorio}: {e}")
            print("Continuando com o próximo diretório...")
            time.sleep(2)
            continue

def pesquisar_gcpj(nome_gcpj):
    pag.click(LUPA, duration=.5)
    pag.click(PESQUISA_INPUT, duration=1.5)
    pag.doubleClick(PESQUISA_INPUT, duration=1.5)
    pag.write(nome_gcpj, interval=.05)
    pag.press("enter")
    time.sleep(7)
    pag.click(LINK_GCPJ, duration=.5)
    time.sleep(1.5)
    scroll_down()

def main():
    pesquisar_gcpj(nome_gcpj)
    time.sleep(.5)
    try:

        # Procura por "Arquivos"
        screenshot, text = capturar_tela()
        if "Arquivos" in text:
            boxes = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            coords = encontrar_palavra(text, "arquivos", boxes)
            if coords:
                x, y = coords
                print(f"Coordenadas da palavra 'arquivos': ({x}, {y})")
                mover(x + OFFSET_X, y + OFFSET_Y)
            else:
                mensagem.show_toast("ERROR",f"Coordenadas da palavra 'arquivos' não encontradas.", duration=2)
                print("ERRO: Coordenadas da palavra 'arquivos' não encontradas.")
        else:
            mensagem.show_toast("ERROR",f"A palavra 'arquivos' não foi encontrada na tela.", duration=2)
            raise Exception("A palavra 'arquivos' não foi encontrada na tela.")
        time.sleep(.1)

        # Procura por "Pasta"
        screenshot, text = capturar_tela()
        if "Pasta" in text:
            boxes = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            coords = encontrar_palavra(text, "pasta", boxes)
            if coords:
                x, y = coords
                print(f"Coordenadas da palavra 'pasta': ({x}, {y})")
                mover(x + OFFSET_X, y + OFFSET_Y)
                time.sleep(.5)
                pag.click(NOME_DA_PASTA[0], NOME_DA_PASTA[1], duration=.3)
                time.sleep(.5)
                pag.write(r'DOCUMENTOS DIVERSOS', interval=.05)
                pag.press('enter')
            else:
                mensagem.show_toast("ERROR",f"Coordenadas da palavra 'pasta' não encontradas.", duration=2)
                print("ERRO: Coordenadas da palavra 'pasta' não encontradas.")
        else:
            mensagem.show_toast("ERROR",f"A palavra 'pasta' não foi encontrada na tela.", duration=2)
            raise Exception("A palavra 'pasta' não foi encontrada na tela.")
        time.sleep(.5)
        
        # Procura por "DIVERSOS"
        screenshot, text = capturar_tela()
        if "DIVERSOS" in text:
            boxes = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            coords = encontrar_palavra(text, "diversos", boxes)
            if coords:
                x, y = coords
                print(f"Coordenadas da palavra 'diversos': ({x}, {y})")
                mover(x + OFFSET_X, y + OFFSET_Y)
                subir_documento(x + OFFSET_UPLOAD_X, y + OFFSET_UPLOAD_Y)
                arrastar(nome_gcpj)
            else:
                mensagem.show_toast("ERROR",f"Coordenadas da palavra 'diversos' não encontradas.", duration=2)
                print("ERRO: Coordenadas da palavra 'diversos' não encontradas.")
        else:
            mensagem.show_toast("ERROR",f"A palavra 'diversos' não foi encontrada na tela.", duration=2)
            raise Exception("A palavra 'diversos' não foi encontrada na tela.")

    except Exception as e:
        print(f"Erro durante a execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    pag.hotkey("alt","tab")
    ponteiro_de_anexos()