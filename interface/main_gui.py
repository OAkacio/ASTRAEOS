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

    # ? --- Configuração de Gráficos ---
    def exibir_grafico(self, nome_arquivo="output.png"):
        caminho_imagem = os.path.join(BASE_DIR, "figures", nome_arquivo)

        if not os.path.exists(caminho_imagem):
            self.set_status(
                f"Erro: Arquivo {nome_arquivo} não encontrado na pasta figures.",
                "#E06C75",
            )
            return

        try:
            img_pil = Image.open(caminho_imagem)
            largura_orig, altura_orig = img_pil.size

            largura_painel = self.painel_graficos.winfo_width() - 20
            altura_painel = self.painel_graficos.winfo_height() - 20

            if largura_painel < 10:
                largura_painel = 800
            if altura_painel < 10:
                altura_painel = 400

            razao_imagem = largura_orig / altura_orig
            razao_painel = largura_painel / altura_painel

            if razao_painel > razao_imagem:
                nova_altura = altura_painel
                nova_largura = int(nova_altura * razao_imagem)
            else:
                nova_largura = largura_painel
                nova_altura = int(nova_largura / razao_imagem)

            img_ctk = ctk.CTkImage(
                light_image=img_pil,
                dark_image=img_pil,
                size=(nova_largura, nova_altura),
            )

            self.lbl_grafico_vazio.configure(text="", image=img_ctk)
            self.lbl_grafico_vazio.image = img_ctk

        except Exception as e:
            self.set_status(f"Erro ao renderizar imagem: {e}", "#E06C75")

    def atualizar_somente_grafico(self):
        try:
            self.set_status("Updating plot styling...", "#61AFEF")

            # 1. Pega os novos parâmetros visuais da interface
            p = self.app_state.parameters_plot()

            # 2. Roda a função de plotagem (ela vai ler o data/curve.npz sozinha!)
            plot_perfil_output(
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

            # 3. Atualiza a imagem na tela
            self.exibir_grafico(nome_arquivo="output.png")
            self.set_status("Plot updated successfully!", "#98C379")

        except Exception as e:
            self.set_status(f"Error updating plot: {e}", "#E06C75")

        finally:
            # Destrava o botão novamente
            self.pagina_atual.btn_update_plot.configure(
                state="normal", text="Update Plot"
            )

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
        self.exibir_grafico(nome_arquivo="output.png")

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
