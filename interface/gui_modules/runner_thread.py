#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Importações                                                              │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
import os
import sys
import queue
import threading
import multiprocessing


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Classes de Controle de Fluxo                                             │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
class RedirecionadorPrint:
    def __init__(self, fila):
        self.fila = fila
        self.buffer = ""

    def write(self, mensagem):
        self.buffer += str(mensagem)
        while "\n" in self.buffer:
            linha, self.buffer = self.buffer.split("\n", 1)
            self.fila.put(linha + "\n")

    def flush(self):
        if self.buffer:
            self.fila.put(self.buffer)
            self.buffer = ""

    def isatty(self):
        return False


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Rotinas de Execução Isolada                                              │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
def motor_isolado(parametros, fila_de_mensagens, fila_de_logs):
    #
    # ? ╭────────────────────────────────────────────────────╮
    # ? │   Mapeamento e Segurança de Caminhos               │
    # ? ╰────────────────────────────────────────────────────╯
    #
    ARQUIVO_ATUAL = os.path.abspath(__file__)
    DIR_GUI = os.path.dirname(ARQUIVO_ATUAL)
    DIR_SRC = os.path.dirname(DIR_GUI)
    DIR_RAIZ = os.path.dirname(DIR_SRC)
    if DIR_SRC not in sys.path:
        sys.path.insert(0, DIR_SRC)
    if DIR_RAIZ not in sys.path:
        sys.path.insert(0, DIR_RAIZ)
    sys.stdout = RedirecionadorPrint(fila_de_logs)
    sys.stderr = RedirecionadorPrint(fila_de_logs)
    script_type = parametros.pop("script_type", "main")
    try:
        #
        # ? ╭────────────────────────────────────────────────────╮
        # ? │   Roteamento Dinâmico de Scripts                   │
        # ? ╰────────────────────────────────────────────────────╯
        #
        if script_type == "multicurve":
            from scripts.multiCURVE import main_mc as simulation

            simulation(**parametros)
        elif script_type == "searchdv2":
            from scripts.searchDV2 import main_sd as simulation

            simulation(**parametros)
        elif script_type == "exoplanet":
            import numpy as np
            from astraeos_core.habitability import main_hab
            from astropy import constants as const

            rsun = const.R_sun.cgs.value
            cte = parametros["cte"]
            dados = np.load(f"data/curve_{cte}.npz")
            r0 = parametros["Rstar"] * rsun
            main_hab(
                Lstar=parametros["Lstar"],
                Teff=parametros["Teff"],
                e=parametros["e"],
                Rstar=parametros["Rstar"],
                Ab=parametros["Ab"],
                Dorb=parametros["Dorb"],
                Mmag=parametros["Mmag"],
                f0=parametros["f0"],
                x_tot=dados["x_tot"],
                y_tot=dados["y_tot"],
                rho_total=dados["rho_total"],
                ve0=dados["ve0"].item(),
                Rplan=parametros["Rplan"],
                r0=r0,
                cte=cte,
                exoplanet_name=parametros["exoplanet_name"],
                k_cme=parametros["k_cme"],
                hion=parametros["hion"],
            )
        else:
            from astraeos_core.main import main as simulation

            simulation(**parametros)
        fila_de_mensagens.put({"success": True})
    except Exception as err:
        fila_de_mensagens.put({"success": False, "error": str(err)})


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Orquestrador de Threads                                                  │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
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
            if resposta["success"]:
                callback_sucesso()
            else:
                callback_erro(resposta["error"])
        else:
            callback_erro("Error: Calculation core terminated unexpectedly.")

    thread = threading.Thread(target=vigia_de_processo, daemon=True)
    thread.start()
