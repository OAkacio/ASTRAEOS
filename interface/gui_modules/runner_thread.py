"""
Módulo de Execução Assíncrona (Runner Multiprocess)
===================================================

Este módulo isola a execução das integrações numéricas em uma thread
paralela para manter a Interface Gráfica responsiva, roteando os logs
do console para a exibição visual.
"""

import os
import sys
import queue
import threading
import multiprocessing


class RedirecionadorPrint:
    def __init__(self, fila):
        self.fila = fila

    def write(self, mensagem):
        self.fila.put(mensagem)

    def flush(self):
        pass

    def isatty(self):
        return False


def motor_isolado(parametros, fila_de_mensagens, fila_de_logs):
    # --- CORREÇÃO DEFINITIVA DE CAMINHOS PARA O WINDOWS ---
    # Como o Windows recria o Python do zero ("spawn"), precisamos 
    # forçar os caminhos exatos da sua arquitetura de pastas.
    ARQUIVO_ATUAL = os.path.abspath(__file__)          # .../src/gui_modules/runner_thread.py
    DIR_GUI = os.path.dirname(ARQUIVO_ATUAL)           # .../src/gui_modules
    DIR_SRC = os.path.dirname(DIR_GUI)                 # .../src
    DIR_RAIZ = os.path.dirname(DIR_SRC)                # .../raiz_do_projeto (onde 'scripts' está)

    # Inserimos a raiz e o src no TOPO da lista de prioridades do Python
    if DIR_SRC not in sys.path:
        sys.path.insert(0, DIR_SRC)
    if DIR_RAIZ not in sys.path:
        sys.path.insert(0, DIR_RAIZ)

    sys.stdout = RedirecionadorPrint(fila_de_logs)
    sys.stderr = RedirecionadorPrint(fila_de_logs)

    # Remove a tag 'script_type' do dicionário para não dar erro na função principal
    script_type = parametros.pop("script_type", "main")

    try:
        # --- Roteamento Dinâmico de Scripts ---
        if script_type == "multicurve":
            from scripts.multiCURVE import main_mc as simulation
        elif script_type == "searchdv2":
            from scripts.searchDV2 import main_sd as simulation
        else:
            from astraeos_core.main import main as simulation

        # Executa a função importada com os parâmetros restantes
        simulation(**parametros)
        fila_de_mensagens.put({"sucesso": True})
        
    except Exception as e:
        fila_de_mensagens.put({"sucesso": False, "erro": str(e)})


def run(parametros, callback_sucesso, callback_erro, callback_log):
    def vigia_de_processo():
        fila_msg = multiprocessing.Queue()
        fila_logs = multiprocessing.Queue()

        p = multiprocessing.Process(
            target=motor_isolado, args=(parametros, fila_msg, fila_logs)
        )
        
        p.daemon = True 
        p.start()

        while p.is_alive():
            while True:
                try:
                    msg = fila_logs.get(timeout=0.01)
                    callback_log(msg)
                except queue.Empty:
                    break
            p.join(0.05)

        while not fila_logs.empty():
            callback_log(fila_logs.get())

        if not fila_msg.empty():
            resposta = fila_msg.get()
            if resposta["sucesso"]:
                callback_sucesso()
            else:
                callback_erro(resposta["erro"])
        else:
            callback_erro("O núcleo de cálculo encerrou inesperadamente.")

    thread = threading.Thread(target=vigia_de_processo, daemon=True)
    thread.start()