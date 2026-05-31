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
import re
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
caminho_icone = os.path.join(ASSETS_PATH, "icon.ico")

from gui_modules.app_state import AppState
from gui_modules.pages.config_page import ConfigPage
from gui_modules.runner_thread import run
from astraeos_core.plot_curve import plot_perfil_output


# * ============================================
# * Controlador Principal
# * ============================================
class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ? --- Identificação ---
        self.title("ASTRAEOS v0.1.0")

        # ? --- Configurações de Janela ---
        self.geometry("1280x720")
        self.minsize(1024, 768)
        self.after(0, lambda: self.state("zoomed"))

        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicativo)

        try:
            self.iconbitmap(caminho_icone)
        except:
            pass

        self.app_state = AppState()

        # ? --- Barra de Status ---
        self.status_bar = ctk.CTkFrame(
            self, height=30, corner_radius=0, fg_color="#1E1E1E"
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)
        self.lbl_status = ctk.CTkLabel(
            self.status_bar,
            text="Welcome!",
            text_color="#E5C07B",
            font=("Consolas", 12),
        )
        self.lbl_status.pack(side="left", padx=10)

        # ? --- Layout Principal (Grid Dinâmico) ---
        self.main_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=2
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=85)
        self.main_container.grid_rowconfigure(1, weight=15)
        self.main_container.grid_columnconfigure(0, weight=7, uniform="colunas")
        self.main_container.grid_columnconfigure(1, weight=3, uniform="colunas")

        # ? --- Painel Esquerdo Superior: Área do Gráfico ---
        self.painel_graficos = ctk.CTkFrame(self.main_container, corner_radius=2)
        self.painel_graficos.grid(
            row=0, column=0, sticky="nsew", padx=(0, 20), pady=(0, 10)
        )

        self.lbl_grafico_vazio = ctk.CTkLabel(
            self.painel_graficos,
            text="[ Visualization Area ]\nWaiting for simulation data...",
            text_color="#5c5c5c",
            font=("Consolas", 16, "italic"),
        )
        self.lbl_grafico_vazio.place(relx=0.5, rely=0.5, anchor="center")

        # ? --- Painel Esquerdo Inferior: Console Integrado ---
        self.console_box = ctk.CTkTextbox(
            self.main_container,
            font=ctk.CTkFont(family="Consolas", size=16),
            fg_color="#1E1E1E",
            text_color="#ABB2BF",
            wrap="none",
            corner_radius=4,
        )
        self.console_box.grid(row=1, column=0, sticky="nsew", padx=(0, 20))

        self.cores_ansi = {
            "30": "#282C34",
            "31": "#E06C75",
            "32": "#98C379",
            "33": "#E5C07B",
            "34": "#61AFEF",
            "35": "#C678DD",
            "36": "#56B6C2",
            "37": "#ABB2BF",
            "90": "#5C6370",
            "91": "#E06C75",
            "92": "#98C379",
            "93": "#E5C07B",
            "94": "#61AFEF",
            "95": "#C678DD",
            "96": "#56B6C2",
            "97": "#FFFFFF",
        }
        for codigo, hex_cor in self.cores_ansi.items():
            self.console_box._textbox.tag_config(f"color_{codigo}", foreground=hex_cor)

        self.console_box.insert("0.0", "ASTRAEOS Console log initialized...\n")
        self.console_box.configure(state="disabled")

        # ? --- Painel Direito: Página de Configuração ---
        self.pagina_atual = ConfigPage(
            master=self.main_container,
            state=self.app_state,
            on_run_click=self.executar_fisica,
            on_update_click=self.atualizar_somente_grafico,
        )
        self.pagina_atual.grid(row=0, column=1, rowspan=2, sticky="nsew")

    # * ============================================
    # * Lógica Interna e Rotinas
    # * ============================================
    # ? --- Lógica Interna do Console ---
    def escrever_console(self, texto):
        self.console_box.configure(state="normal")

        partes = re.split(r"(\x1b\[[0-9;]*m)", texto)
        tag_atual = None

        for parte in partes:
            if parte.startswith("\x1b["):
                codigos = parte[2:-1].split(";")
                for cod in codigos:
                    if cod in self.cores_ansi:
                        tag_atual = f"color_{cod}"
                    elif cod == "0":
                        tag_atual = None
            elif parte:
                if tag_atual:
                    self.console_box.insert("end", parte, tag_atual)
                else:
                    self.console_box.insert("end", parte)

        self.console_box.see("end")
        self.console_box.configure(state="disabled")

    # ? --- Atualização de Status Bar ---
    def set_status(self, mensagem, cor="#858585"):
        self.lbl_status.configure(text=f" {mensagem}", text_color=cor)

    # ? --- Configuração de Gráficos (MODO INTERATIVO) ---
    def exibir_grafico(self, figura_matplotlib):
        try:
            # 1. Limpa o painel atual (remove o texto "Waiting..." ou o gráfico antigo)
            for widget in self.painel_graficos.winfo_children():
                widget.destroy()

            # 2. Renderiza a figura matemática interativa no CustomTkinter
            canvas = FigureCanvasTkAgg(figura_matplotlib, master=self.painel_graficos)
            canvas.draw()

            # 3. Adiciona a Barra de Ferramentas (Zoom, Salvar, Pan) - Estilizada para Dark Mode
            toolbar = NavigationToolbar2Tk(canvas, self.painel_graficos)
            toolbar.config(background="#1E1E1E")

            # Aplica a cor apenas aos elementos que suportam (ignora separadores)
            for widget in toolbar.winfo_children():
                try:
                    widget.config(background="#1E1E1E")
                    widget.config(activebackground="#2C313A")
                except:
                    pass  # Se o widget não for um botão, apenas ignora o erro e continua

            toolbar.update()

            # 4. Posiciona tudo na tela
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        except Exception as e:
            self.set_status(f"Erro ao renderizar gráfico interativo: {e}", "#E06C75")

    def atualizar_somente_grafico(self):
        try:
            self.set_status("Updating plot styling...", "#61AFEF")

            # 1. Pega os novos parâmetros visuais da interface
            p = self.app_state.parameters_plot()

            # 2. Roda a função com TODOS os argumentos necessários
            minha_figura = plot_perfil_output(
                x_ref=p["x_ref"],
                linestyle_ref=p["linestyle_ref"],
                color_ref=p["color_ref"],
                nome_ref=p["nome_ref"],
                sigmas_ref=p["sigmas_ref"],
                sigmas_color_ref=p["sigmas_color_ref"],
                sigmas_nome_ref=p["sigmas_nome_ref"],
                x_scale=p["x_scale"],
                y_scale=p["y_scale"],
            )

            # 3. Atualiza a imagem interativa na tela
            self.exibir_grafico(minha_figura)
            self.set_status("Plot updated successfully!", "#98C379")

        except Exception as e:
            self.set_status(f"Error updating plot: {e}", "#E06C75")

        finally:
            # Destrava o botão novamente
            self.pagina_atual.btn_update_plot.configure(
                state="normal", text="Update Plot"
            )

    def fechar_aplicativo(self):
        self.set_status("Shutting down ASTRAEOS and clearing memory...", "#E06C75")
        self.update()  # Força a interface a mostrar a mensagem antes de travar

        # Procura qualquer processo filho solto e atira a matar
        processos_ativos = multiprocessing.active_children()
        for processo in processos_ativos:
            processo.terminate()
            processo.join(timeout=1.0)  # Dá 1 segundo pro processo morrer com dignidade

        # Destrói a janela e encerra o Python
        self.destroy()
        sys.exit(0)

    # ? --- Rotina ao Iniciar Simulação ---
    def executar_fisica(self):
        parametros_fisica = self.app_state.parameters_input()
        parametros_plot = self.app_state.parameters_plot()
        parametros_completos = {**parametros_fisica, **parametros_plot}
        self.set_status(
            "Starting simulation... Check the console for more details.",
            "#E5C07B",
        )
        self.console_box.configure(state="normal")
        self.console_box.delete("0.0", "end")
        self.console_box.insert("end", "--- Initiating Execution ---\n")
        self.console_box.configure(state="disabled")

        run(
            parametros=parametros_completos,
            callback_sucesso=self.ao_terminar_com_sucesso,
            callback_erro=self.ao_dar_erro,
            callback_log=self.ao_receber_log,
        )

    # * ============================================
    # * Callbacks
    # * ============================================
    # ? --- Simulação Finalizada com Sucesso ---
    def ao_terminar_com_sucesso(self):
        self.after(0, self._atualizar_ui_sucesso)

    def _atualizar_ui_sucesso(self):
        self.set_status(
            f"Task completed successfully!",
            "#98C379",
        )
        self.pagina_atual.btn_run.configure(state="normal", text="Run Simulation")
        self.pagina_atual.btn_update_plot.configure(state="normal", text="Update Plot")

        p = self.app_state.parameters_plot()
        i = self.app_state.parameters_input()
        figura_inicial = plot_perfil_output(
            x_ref=p["x_ref"],
            linestyle_ref=p["linestyle_ref"],
            color_ref=p["color_ref"],
            nome_ref=p["nome_ref"],
            sigmas_ref=p["sigmas_ref"],
            sigmas_color_ref=p["sigmas_color_ref"],
            sigmas_nome_ref=p["sigmas_nome_ref"],
            x_scale=p["x_scale"],
            y_scale=p["y_scale"],
            cte=i["cte"],
        )

        # Exibe o gráfico interativo
        self.exibir_grafico(figura_inicial)

    # ? --- Simulação Finalizada com Erro ---
    def ao_dar_erro(self, mensagem_erro):
        self.after(0, self._atualizar_ui_erro, mensagem_erro)

    def _atualizar_ui_erro(self, erro):
        self.set_status(f"Execution error | {erro}", "#E06C75")
        self.pagina_atual.btn_run.configure(state="normal", text="Run Simulation")

    # ? --- Recebimento de Log ---
    def ao_receber_log(self, texto_bruto):
        self.after(0, lambda: self.escrever_console(texto_bruto))


# * ============================================
# * Execução do Aplicativo
# * ============================================
if __name__ == "__main__":
    multiprocessing.freeze_support()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = AppWindow()
    app.mainloop()
