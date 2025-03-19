from win10toast import ToastNotifier
import pygetwindow as gw
import pyautogui as pag
import shutil
import time
import os

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

#DIGITE AQUI O CAMINHO DO DIRETORIO DE ORIGEM ✅
diretorio_pai = ''

diretorio_feito = os.path.join(diretorio_pai, 'Anexos feitos')
itens = os.listdir(diretorio_pai)
diretorios_filhos = [item for item in itens if os.path.isdir(os.path.join(diretorio_pai, item))]

# Cria o diretório "Anexos feitos" se não existir
os.makedirs(diretorio_feito, exist_ok=True)

mensagem = ToastNotifier()

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
                mensagem.show_toast("Anexos Concluídos",f"Diretorio {nome_gcpj} não é um GCPJ válido", duration=2)
                print(f"Diretorio {nome_gcpj} não é um GCPJ válido")
                break
            
            time.sleep(.5)
            rodar_robo() #função para navegar no Octopus

            # Move o diretório processado para o diretório "Anexos feitos" 
            shutil.move(os.path.join(diretorio_pai, diretorio), diretorio_feito)
            print(f"\n{diretorio} concluído e movido para {diretorio_feito}\n")
            
        except Exception as e:
            mensagem.show_toast("ERROR",f"Erro ao processar o diretório {diretorio}", duration=2)
            print(f"Erro ao processar o diretório {diretorio}: {e}")
            print("Continuando com o próximo diretório...")
            time.sleep(2)
            continue

#pesquisa o GCPJ e clica no link do processo
def pesquisar_gcpj(nome_gcpj):
    time.sleep(1)
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
    time.sleep(3)
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
    time.sleep(5)
    pag.click(LUPA, duration=.5)

#fechar janela de anexos ✅
def fechar_janela(nome_gcpj):
    janelas = gw.getWindowsWithTitle(nome_gcpj) 
    if janelas:
        janelas[0].close()
    else:
        mensagem.show_toast("ERROR",f"janela '{nome_gcpj}' não encontrada", duration=2)
        print("Erro: janela não encontrada")

#Navegar no Octopus
def rodar_robo():
    pesquisar_gcpj(nome_gcpj)
    scroll_down()
    anexar()
    arrastar(diretorio_pai,nome_gcpj)
    fechar_janela(nome_gcpj)

#Run
pag.hotkey("alt", "tab")
ponteiro_de_anexos()