import sys
import queue
import threading
import multiprocessing
from astraeos_core.main import main as simulation

# Classe que finge ser o terminal com todas as funções que o Python exige
class RedirecionadorPrint:
    def __init__(self, fila):
        self.fila = fila
    def write(self, mensagem):
        self.fila.put(mensagem)
    def flush(self):
        pass
    def isatty(self):
        return False  # Evita crash em bibliotecas que checam se é um terminal real

def motor_isolado(parametros, fila_de_mensagens, fila_de_logs):
    # Sequestra os prints e os erros do Python deste núcleo
    sys.stdout = RedirecionadorPrint(fila_de_logs)
    sys.stderr = RedirecionadorPrint(fila_de_logs)
    
    try:
        simulation(**parametros)
        fila_de_mensagens.put({"sucesso": True})
    except Exception as e:
        fila_de_mensagens.put({"sucesso": False, "erro": str(e)})

def run(parametros, callback_sucesso, callback_erro, callback_log):
    def vigia_de_processo():
        fila_msg = multiprocessing.Queue()
        fila_logs = multiprocessing.Queue()
        
        p = multiprocessing.Process(target=motor_isolado, args=(parametros, fila_msg, fila_logs))
        p.start()
        
        # Fica lendo os prints de forma segura
        while p.is_alive():
            while True:
                try:
                    # Tenta pegar um log novo. Se não tiver nada, quebra esse sub-loop.
                    msg = fila_logs.get(timeout=0.01)
                    callback_log(msg)
                except queue.Empty:
                    break
            p.join(0.05) # Pausa mínima para o computador respirar
            
        # Esvazia a fila de logs caso tenha sobrado algum print após fechar o processo
        while not fila_logs.empty():
            callback_log(fila_logs.get())
            
        # Verifica o resultado da matemática
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