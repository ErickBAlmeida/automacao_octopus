import pyautogui as pag
import time
import os
import shutil
import pyperclip
import pygetwindow as gw

#coordenadas dos elementos da tela
LUPA = (1415, 180) #Apenas na página de inclusão de anexos
PESQUISA_INPUT = (728, 339)
PRESQUISA_BUTTON = (1270, 339)
LINK_GCPJ = (378, 586)
ACESSAR_BUTTON = (1729, 593)
ANEXOS_BUTTON = (1241, 809)
CATEGORIAS_ANEXOS = (792, 516)
ARQUIVOS_BUTTON = (868, 1042)
PRIMEIRO_ARQUIVO = (431, 263)
ANEXOS_AREA =(1198, 599)

#abre o diretorio pai ✅
diretorio_pai = 'A:/TI/Processamento Cadastro DRC/Anexos parte 2 - 22.01'

diretorio_feito = os.path.join(diretorio_pai, 'Anexos feitos')
itens = os.listdir(diretorio_pai)
diretorios_filhos = [item for item in itens if os.path.isdir(os.path.join(diretorio_pai, item))]


# Cria o diretório "Anexos feitos" se não existir
os.makedirs(diretorio_feito, exist_ok=True)

def ponteiro_de_anexos():
    for i in range(len(diretorios_filhos)):
        try:
            diretorio = diretorios_filhos[i] #escolhe um diretorio
            global nome_gcpj
            nome_gcpj = diretorio #nome da janela do explorer

            time.sleep(.5)
            
            # (AQUI) função para rodar o robo
            rodar_robo()

            # Move o diretório processado para o diretório "Anexos feitos" 
            shutil.move(os.path.join(diretorio_pai, diretorio), diretorio_feito)
            print(f"Anexos do {diretorio} movidos para {diretorio_feito}")
            
        except Exception as e:
            print(f"Erro ao processar o diretório {diretorio}: {e}")
            print("Deseja continuar com o próximo diretório? (s/n)")
            if input().lower() != 's':
                print("Processamento interrompido pelo usuário.")
                break
            print("Continuando com o próximo diretório...")
            time.sleep(2)
            continue

#pesquisa o GCPJ e clica no link do processo
def pesquisar_gcpj(nome_gcpj):
    time.sleep(1)
    # pag.hotkey("alt", "tab")
    time.sleep(1)
    pag.click(LUPA, duration=.5)
    time.sleep(1)
    pag.click(PESQUISA_INPUT, duration=.5)
    time.sleep(1)
    pag.doubleClick(PESQUISA_INPUT, duration=.5)
    time.sleep(1)
    pag.write(nome_gcpj, interval=0.1)
    pag.press("enter")
    time.sleep(7)
    pag.click(LINK_GCPJ, duration=.5)
    # scroll_down()
    # anexar()

#procura o botão pra seguir para a página de anexos
def scroll_down():
    time.sleep(1)
    pag.click(ACESSAR_BUTTON, duration=.5)
    time.sleep(3)
    pag.scroll(-20000)
    time.sleep(1)
    pag.scroll(500)
    pag.click(ACESSAR_BUTTON, duration=.5)

#clica no botão de anexos e seleciona o tipo de anexo
def anexar():
    time.sleep(3)
    pag.click(ANEXOS_BUTTON, duration=.5)
    time.sleep(1)
    pag.click(CATEGORIAS_ANEXOS, duration=.5)
    time.sleep(1)
    pag.press("down", presses=11)
    pag.press("enter")
    time.sleep(1)

#arrasta os arquivos para a área de anexos
def arrastar(diretorio_pai,nome_gcpj):
    time.sleep(1)
    os.startfile(diretorio_pai+'/'+ nome_gcpj) #abre o diretorio dos anexos
    time.sleep(2)
    pag.click(957, 514, duration=.1)
    pag.hotkey("ctrl", "a")
    time.sleep(1)
    pag.moveTo(PRIMEIRO_ARQUIVO, duration=.5)
    time.sleep(1)
    pag.mouseDown()
    time.sleep(1)
    pag.moveTo(ANEXOS_AREA, duration=.5)
    pag.hotkey("alt", "tab")
    pag.mouseUp()
    time.sleep(3)
    pag.click(LUPA, duration=.5)

#fechar janela de anexos ✅
def fechar_janela(nome_gcpj):
    janelas = gw.getWindowsWithTitle(nome_gcpj) 
    if janelas:
        janelas[0].close()
        print(f"Janela {janelas[0]} fechada com sucesso.")
    else:
        print("janela não encontrada")

def rodar_robo():
    pesquisar_gcpj(nome_gcpj)
    scroll_down()
    anexar()
    arrastar(diretorio_pai,nome_gcpj)
    fechar_janela(nome_gcpj)

#play
pag.hotkey("alt", "tab")
ponteiro_de_anexos()