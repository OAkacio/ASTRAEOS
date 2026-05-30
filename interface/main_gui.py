"""
Módulo Principal da Interface (Entry Point)
===========================================

Este é o arquivo executável que inicializa a aplicação ASTRAEOS.
Ele atua como o Controlador Central, orquestrando a injeção de
dependências entre o Gerenciador de Estado, a Interface Visual
e o Motor de Execução Paralela.

"""

# * ============================================
# * Importações e Configuração de Caminhos
# * ============================================
import os
import sys
import customtkinter as ctk
import multiprocessing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
caminho_icone = os.path.join(ASSETS_PATH, "icon.ico")
from gui_modules.app_state import AppState
from gui_modules.pages.config_page import ConfigPage
from gui_modules.runner_thread import run


# * ============================================
# * Controlador Principal
# * ============================================
class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ? --- Identificação ---
        self.title("ASTRAEOS v0.1.0")

        # ? --- Configuirações de Janela ---
        self.geometry("1280x720")
        self.minsize(1024, 768)
        self.after(0, lambda: self.state("zoomed"))
        self.iconbitmap(caminho_icone)

        # ? --- Janela Principal ---
        self.app_state = AppState()

        # ? --- Barra de Status ---
        self.status_bar = ctk.CTkFrame(
            self, height=30, corner_radius=0, fg_color="#1E1E1E"
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)
        self.lbl_status = ctk.CTkLabel(
            self.status_bar,
            text="",
            text_color="#858585",
            font=("Consolas", 12),
        )
        self.lbl_status.pack(side="left", padx=10)

        # ? --- Inicializa Página Principal ---
        self.pagina_atual = ConfigPage(
            master=self, state=self.app_state, on_run_click=self.executar_fisica
        )
        self.pagina_atual.pack(fill="both", expand=True, padx=20, pady=20)

    # ? --- Atualização de Status Bar ---
    def set_status(self, mensagem, cor="#858585"):
        self.lbl_status.configure(text=f" {mensagem}", text_color=cor)

    # ? --- Rotina ao Iniciar Simulação ---
    def executar_fisica(self):
        parametros = self.app_state.parameters_input()
        self.set_status(
            "Iniciando simulação... Acompanhe o console para mais informações.",
            "#E5C07B",
        )
        run(
            parametros=parametros,
            callback_sucesso=self.ao_terminar_com_sucesso,
            callback_erro=self.ao_dar_erro,
        )

    # * ============================================
    # * Callbacks
    # * ============================================
    # ? --- Simulação Finalizada com Sucesso ---
    def ao_terminar_com_sucesso(self, x_crit, y_crit):
        self.after(0, self._atualizar_ui_sucesso, x_crit, y_crit)

    def _atualizar_ui_sucesso(self):
        self.set_status(
            f"Concluído com sucesso!",
            "#98C379",
        )
        self.pagina_atual.btn_run.configure(state="normal", text="Rodar Novamente")

    # ? --- Simulação Finalizada com Erro ---
    def ao_dar_erro(self, mensagem_erro):
        self.after(0, self._atualizar_ui_erro, mensagem_erro)

    def _atualizar_ui_erro(self, erro):
        self.set_status(f"ERRO: {erro}", "#E06C75")
        self.pagina_atual.btn_run.configure(state="normal", text="Tentar Novamente")


# * ============================================
# * Execução do Aplicativo
# * ============================================
if __name__ == "__main__":
    multiprocessing.freeze_support()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = AppWindow()
    app.mainloop()
