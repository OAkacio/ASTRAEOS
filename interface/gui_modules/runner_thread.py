"""
Módulo de Execução Assíncrona (Runner Thread)
=============================================

Este módulo é responsável por isolar a execução das integrações numéricas
e da física pesada em uma thread paralela. Ele garante que a Interface
Gráfica (GUI) permaneça responsiva durante o processamento de longas
simulações, evitando o congelamento da janela.

Utiliza um padrão de "Callbacks" para comunicar o resultado (sucesso ou
falha) de volta à thread principal (Tkinter) de forma segura.
"""

# * ============================================
# * Importações
# * ============================================
import threading
from astraeos_core.main import main as simulation
import multiprocessing


# * ============================================
# * Funções de Orquestração Paralela
# * ============================================
def motor_isolado(parametros, fila_de_mensagens):
    try:
        # Roda a simulação bruta e pesada
        x_tot, y_tot, x_crit, y_crit, x_t, ve0 = simulation(**parametros)
        
        # Coloca os resultados na fila de comunicação para a interface pegar
        fila_de_mensagens.put({"sucesso": True, "dados": (x_crit, y_crit)})
    except Exception as e:
        fila_de_mensagens.put({"sucesso": False, "erro": str(e)})

def run(parametros, callback_sucesso, callback_erro):
    """
    Inicia a simulação em uma thread separada em background.

    Args:
        parametros (dict): Dicionário contendo os argumentos físicos e numéricos
            (gerado pelo AppState.parameters_input()).
        callback_sucesso (function): Função da GUI a ser chamada se a simulação
            terminar sem erros. Deve aceitar os argumentos retornados pela física
            (ex: x_crit, y_crit).
        callback_erro (function): Função da GUI a ser chamada caso ocorra uma
            exceção. Deve aceitar uma string com a mensagem de erro.
    """

    def vigia_de_processo():
        # Cria um "tubo" de comunicação entre a Interface e o Processo do Julia
        fila = multiprocessing.Queue()
        
        # Instancia um PROCESSO (outro núcleo), não apenas uma thread
        p = multiprocessing.Process(target=motor_isolado, args=(parametros, fila))
        p.start()
        
        # A thread espera pacientemente o processo terminar.
        # (A interface continua lisa porque quem está esperando é a thread vigia!)
        p.join()
        
        # Quando termina, lemos o que o Julia deixou na fila
        if not fila.empty():
            resposta = fila.get()
            if resposta["sucesso"]:
                x_crit, y_crit = resposta["dados"]
                callback_sucesso(x_crit, y_crit)
            else:
                callback_erro(resposta["erro"])
        else:
            callback_erro("O núcleo de cálculo falhou silenciosamente (Crash no Julia).")

    # Iniciamos a thread vigia
    thread = threading.Thread(target=vigia_de_processo, daemon=True)
    thread.start()