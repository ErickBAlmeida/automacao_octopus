import pyautogui as pag
import time
import os
import shutil
import pyperclip

#abre o diretorio pai ✅
diretorio_pai = 'A:\TI\Processamento Cadastro DRC\Anexos parte 2 - 22.01'

diretorio_feito = os.path.join(diretorio_pai, 'feito')
itens = os.listdir(diretorio_pai)
diretorios_filhos = [item for item in itens if os.path.isdir(os.path.join(diretorio_pai, item))]


# Cria o diretório "feito" se não existir
os.makedirs(diretorio_feito, exist_ok=True)

def ponteiro_de_anexos():
    for i in range(len(diretorios_filhos)):
        try:
            diretorio = diretorios_filhos[i] #escolhe um diretorio
            #nome da janela do explorer
            global nome_janela
            nome_janela = diretorio.copy()
            os.startfile(diretorio_pai+'/'+diretorio) #abre o diretorio dos anexos
            # (AQUI) função para rodar o robo
            time.sleep(.5)
        except Exception as e:
            print(f"Erro ao abrir o diretório {diretorio}: {e}")
            time.sleep(1)
            break

#fechar janela de anexos ✅
def fechar_janela(nome_janela):
    janelas = nome_janela
    if janelas:
        janelas[0].close()
        print(f"Janela {janelas[0]} fechada com sucesso.")
    else:
        print("janela não encontrada")

