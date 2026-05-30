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
from gui_modules.app_state import AppState
from gui_modules.pages.config_page import ConfigPage
from gui_modules.runner_thread import run


# * ============================================
# * Controlador Principal (Janela)
# * ============================================
class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ASTRAEOS")
        self.geometry("1280x720")
        self.minsize(1024, 768)
        self.after(0, lambda: self.state('zoomed'))

        self.app_state = AppState()

        self.pagina_atual = ConfigPage(
            master=self,
            state=self.app_state,
            on_run_click=self.executar_fisica,
        )
        self.pagina_atual.pack(fill="both", expand=True, padx=20, pady=20)

    def executar_fisica(self):
        # 2. Puxamos os dados da variável renomeada
        parametros = self.app_state.parameters_input()

        run(
            parametros=parametros,
            callback_sucesso=self.ao_terminar_com_sucesso,
            callback_erro=self.ao_dar_erro,
        )

    # * ============================================
    # * Callbacks Seguros (Thread-Safe)
    # * ============================================
    def ao_terminar_com_sucesso(self, x_crit, y_crit):
        """
        Ponte segura: Redireciona a resposta da thread paralela para a thread principal.
        """
        self.after(0, self._atualizar_ui_sucesso, x_crit, y_crit)

    def _atualizar_ui_sucesso(self, x_crit, y_crit):
        """Atualiza a UI após sucesso. (Executado SOMENTE pela thread principal)"""
        # Exemplo de cor verde suave que harmoniza com temas escuros
        self.pagina_atual.lbl_status.configure(
            text=f"Concluído! Ponto crítico (Z/r) encontrado em {x_crit:.3f} r0.",
            text_color="#98C379",
        )
        self.pagina_atual.btn_run.configure(state="normal", text="Rodar Novamente")

        # TODO: Implementar aqui a lógica para abrir a aba/página de Resultados
        # e carregar o arquivo .png gerado pelo PyTools Matplotlib.

    def ao_dar_erro(self, mensagem_erro):
        """
        Ponte segura para tratamento de falhas.
        """
        self.after(0, self._atualizar_ui_erro, mensagem_erro)

    def _atualizar_ui_erro(self, erro):
        """Atualiza a UI alertando falhas de integração ou física."""
        self.pagina_atual.lbl_status.configure(
            text=f"Erro na simulação: {erro}", text_color="#E06C75"
        )
        self.pagina_atual.btn_run.configure(state="normal", text="Tentar Novamente")


# * ============================================
# * Execução do Aplicativo
# * ============================================
if __name__ == "__main__":
    # Comando de segurança OBRIGATÓRIO no Windows para Multiprocessing:
    multiprocessing.freeze_support()

    # Configuração de design global
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = AppWindow()
    app.mainloop()
