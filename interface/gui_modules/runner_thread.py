"""
Módulo de Execução Assíncrona (Runner Multiprocess)
===================================================

Este módulo isola a execução das integrações numéricas em uma thread
paralela para manter a Interface Gráfica responsiva, roteando os logs
do console para a exibição visual.
"""

# * ============================================
# * Importações
# * ============================================
import sys
import queue
import threading
import multiprocessing
from astraeos_core.main import main as simulation


# * ============================================
# * Classes Auxiliares
# * ============================================
# ? --- Redirecionador de Console ---
class RedirecionadorPrint:
    def __init__(self, fila):
        self.fila = fila

    def write(self, mensagem):
        self.fila.put(mensagem)

    def flush(self):
        pass

    def isatty(self):
        return False


# * ============================================
# * Funções de Orquestração Paralela
# * ============================================
# ? --- Motor Físico Isolado ---
def motor_isolado(parametros, fila_de_mensagens, fila_de_logs):
    sys.stdout = RedirecionadorPrint(fila_de_logs)
    sys.stderr = RedirecionadorPrint(fila_de_logs)

    try:
        simulation(**parametros)
        fila_de_mensagens.put({"sucesso": True})
    except Exception as e:
        fila_de_mensagens.put({"sucesso": False, "erro": str(e)})


# ? --- Vigia de Processo (Thread) ---
def run(parametros, callback_sucesso, callback_erro, callback_log):
    def vigia_de_processo():
        fila_msg = multiprocessing.Queue()
        fila_logs = multiprocessing.Queue()

        p = multiprocessing.Process(
            target=motor_isolado, args=(parametros, fila_msg, fila_logs)
        )
        
        # --- AVISO AO SISTEMA OPERACIONAL ---
        # Garante que este processo filho seja exterminado automaticamente 
        # caso o processo pai (a janela do Tkinter) seja encerrado.
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