import pyautogui as pag
import time
import pandas as pd
import pyperclip

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

#pesquisa o GCPJ e clica no link do processo
def pesquisar_gcpj(val_gcpj):
    time.sleep(1)
    pag.hotkey("alt", "tab")
    time.sleep(1)
    pag.click(LUPA, duration=.5)
    time.sleep(1)
    pag.click(PESQUISA_INPUT, duration=.5)
    time.sleep(1)
    pag.doubleClick(PESQUISA_INPUT, duration=.5)
    time.sleep(1)
    pag.write(val_gcpj, interval=0.1)
    pag.press("enter")
    time.sleep(7)
    pag.click(LINK_GCPJ, duration=.5)
    scroll_down()
    anexar()

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
def arrastar():
    time.sleep(1)
    pag.click(ARQUIVOS_BUTTON, duration=.5)
    pag.hotkey("ctrl", "a")
    time.sleep(1)
    pag.moveTo(PRIMEIRO_ARQUIVO, duration=.5)
    time.sleep(1)
    pag.mouseDown()
    time.sleep(1)
    pag.moveTo(ANEXOS_AREA, duration=.5)
    pag.hotkey("alt", "tab")
    pag.mouseUp()
    pag.click(LUPA, duration=.5)

# pesquisar_gcpj(gcpj)
# scroll_down()
# anexar()
# abrir_arquivos()

def teste():
    anexar()
    arrastar()
teste()