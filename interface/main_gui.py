# * ============================================
# * Importações e Configuração de Caminhos
# * ============================================
import os
import sys
import re
import multiprocessing
import customtkinter as ctk
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
from astraeos_core.plot_curve import plot_perfil_output, plot_multicurve

# * ============================================
# * Controlador Principal (AppWindow)
# * ============================================
class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ? --- Identificação e Configuração de Janela ---
        self.title("ASTRAEOS v0.1.0")
        self.geometry("1280x720")
        self.minsize(1024, 768)
        self.after(0, lambda: self.state("zoomed"))
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicativo)

        try:
            self.iconbitmap(caminho_icone)
        except Exception:
            pass

        self.app_state = AppState()
        self.skip_next_newline = False

        # ? --- Barra de Status e Barras de Progresso ---
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0, fg_color="#1E1E1E")
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)
        
        self.lbl_status = ctk.CTkLabel(self.status_bar, text="Welcome!", text_color="#E5C07B", font=("Consolas", 12))
        self.lbl_status.pack(side="left", padx=10)

        self.progressbar = ctk.CTkProgressBar(self.status_bar, width=200, height=10, progress_color="#61AFEF", fg_color="#282C34")
        self.progressbar.set(0.0)

        self.micro_bars_frame = ctk.CTkFrame(self.status_bar, fg_color="transparent")
        
        self.u0_progressbar = ctk.CTkProgressBar(self.micro_bars_frame, width=120, height=4, progress_color="#1F618D", fg_color="#282C34")
        self.u0_progressbar.pack(side="top", pady=(0, 2))
        self.u0_progressbar.set(0.0)

        self.int_progressbar = ctk.CTkProgressBar(self.micro_bars_frame, width=120, height=4, progress_color="#E5C07B", fg_color="#282C34")
        self.int_progressbar.pack(side="bottom")
        self.int_progressbar.set(0.0)

        # ? --- Layout Principal e Painéis ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=2)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=85)
        self.main_container.grid_rowconfigure(1, weight=15)
        self.main_container.grid_columnconfigure(0, weight=7, uniform="colunas")
        self.main_container.grid_columnconfigure(1, weight=3, uniform="colunas")

        # ? --- Painel Esquerdo Superior: Área do Gráfico (Tabview) ---
        self.painel_graficos = ctk.CTkTabview(self.main_container)
        self.painel_graficos.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=(0, 10))

        self.tab_velocity = self.painel_graficos.add("Velocity Profile")
        self.tab_charspeeds = self.painel_graficos.add("Characteristic Speeds")
        self.tab_plasmaprop = self.painel_graficos.add("Plasma Properties")
        self.tab_topology = self.painel_graficos.add("Critical Topology")
        self.tab_magnetospheric = self.painel_graficos.add("Magnetospheric Impact")

        self.lbl_grafico_vazio = ctk.CTkLabel(
            self.tab_velocity,
            text="[ Visualization Area ]\nWaiting for simulation data...",
            text_color="#5c5c5c",
            font=("Consolas", 16, "italic"),
        )
        self.lbl_grafico_vazio.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_grafico_vazio2 = ctk.CTkLabel(
            self.tab_charspeeds,
            text="[ Visualization Area ]\nWaiting for simulation data...",
            text_color="#5c5c5c",
            font=("Consolas", 16, "italic"),
        )
        self.lbl_grafico_vazio2.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_grafico_vazio3 = ctk.CTkLabel(
            self.tab_plasmaprop,
            text="[ Visualization Area ]\nWaiting for simulation data...",
            text_color="#5c5c5c",
            font=("Consolas", 16, "italic"),
        )
        self.lbl_grafico_vazio3.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_grafico_vazio4 = ctk.CTkLabel(
            self.tab_topology,
            text="[ Visualization Area ]\nWaiting for simulation data...",
            text_color="#5c5c5c",
            font=("Consolas", 16, "italic"),
        )
        self.lbl_grafico_vazio4.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_grafico_vazio5 = ctk.CTkLabel(
            self.tab_magnetospheric,
            text="[ Visualization Area ]\nWaiting for simulation data...",
            text_color="#5c5c5c",
            font=("Consolas", 16, "italic"),
        )
        self.lbl_grafico_vazio5.place(relx=0.5, rely=0.5, anchor="center")

        # ? --- Console Integrado ---
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
            "30": "#282C34", "31": "#E06C75", "32": "#98C379", "33": "#E5C07B",
            "34": "#61AFEF", "35": "#C678DD", "36": "#56B6C2", "37": "#ABB2BF",
            "90": "#5C6370", "91": "#E06C75", "92": "#98C379", "93": "#E5C07B",
            "94": "#61AFEF", "95": "#C678DD", "96": "#56B6C2", "97": "#FFFFFF",
        }
        for codigo, hex_cor in self.cores_ansi.items():
            self.console_box._textbox.tag_config(f"color_{codigo}", foreground=hex_cor)

        self.console_box.insert("0.0", "ASTRAEOS Console log initialized...\n")
        self.console_box.configure(state="disabled")

        # ? --- Página de Configuração de Parâmetros ---
        self.pagina_atual = ConfigPage(
            master=self.main_container,
            state=self.app_state,
            on_run_click=self.executar_fisica,
            on_update_click=self.atualizar_somente_grafico,
            on_abort_click=self.abortar_execucao,
        )
        self.pagina_atual.grid(row=0, column=1, rowspan=2, sticky="nsew")

    # * ============================================
    # * Rotinas de Interface Visual
    # * ============================================
    # ? --- Gestão do Console e Status ---
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

    def set_status(self, mensagem, cor="#858585"):
        self.lbl_status.configure(text=f" {mensagem}", text_color=cor)

    # ? --- Renderização de Gráficos Dinâmica ---
    def exibir_grafico(self, figura_matplotlib, container=None):
        if container is None:
            container = self.tab_velocity

        try:
            for widget in container.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(figura_matplotlib, master=container)
            canvas.draw()

            toolbar = NavigationToolbar2Tk(canvas, container)
            toolbar.config(background="#1E1E1E")

            for widget in toolbar.winfo_children():
                try:
                    widget.config(background="#1E1E1E")
                    widget.config(activebackground="#2C313A")
                except Exception:
                    pass

            toolbar.update()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        except Exception as e:
            self.set_status(f"Erro ao renderizar gráfico interativo: {e}", "#E06C75")

    def atualizar_somente_grafico(self):
        try:
            self.set_status("Updating plot styling...", "#61AFEF")

            p = self.app_state.parameters_plot()
            i = self.app_state.parameters_input()
            m = self.app_state.parameters_more_options()

            if m["multicurve"]:
                minha_figura = plot_multicurve(
                    x_ref=p["x_ref"], linestyle_ref=p["linestyle_ref"],
                    color_ref=p["color_ref"], nome_ref=p["nome_ref"],
                    sigmas_ref=p["sigmas_ref"], sigmas_color_ref=p["sigmas_color_ref"],
                    sigmas_nome_ref=p["sigmas_nome_ref"], x_scale=p["x_scale"], y_scale=p["y_scale"],
                )
            else:
                minha_figura = plot_perfil_output(
                    x_ref=p["x_ref"], linestyle_ref=p["linestyle_ref"],
                    color_ref=p["color_ref"], nome_ref=p["nome_ref"],
                    sigmas_ref=p["sigmas_ref"], sigmas_color_ref=p["sigmas_color_ref"],
                    sigmas_nome_ref=p["sigmas_nome_ref"], x_scale=p["x_scale"],
                    y_scale=p["y_scale"], cte=i["cte"],
                )

            self.exibir_grafico(minha_figura)
            self.set_status("Plot updated successfully!", "#98C379")

        except Exception as e:
            self.set_status(f"Error updating plot: {e}", "#E06C75")
        finally:
            self.pagina_atual.btn_update_plot.configure(state="normal", text="Update Plot")

    def _atualizar_grafico_parcial(self):
        try:
            p = self.app_state.parameters_plot()
            i = self.app_state.parameters_input()
            
            figura_parcial = plot_perfil_output(
                x_ref=p["x_ref"], linestyle_ref=p["linestyle_ref"],
                color_ref=p["color_ref"], nome_ref=p["nome_ref"],
                sigmas_ref=p["sigmas_ref"], sigmas_color_ref=p["sigmas_color_ref"],
                sigmas_nome_ref=p["sigmas_nome_ref"], x_scale=p["x_scale"],
                y_scale=p["y_scale"], cte=i["cte"],
            )
            self.exibir_grafico(figura_parcial)
        except Exception:
            pass

    def _forcar_animacao_barra(self, widget_barra, valor):
        widget_barra.set(valor)
        widget_barra.update_idletasks()

    # * ============================================
    # * Controle de Execução
    # * ============================================
    # ? --- Iniciar Simulação ---
    def executar_fisica(self):
        parametros_fisica = self.app_state.parameters_input()
        parametros_plot = self.app_state.parameters_plot()
        parametros_more = self.app_state.parameters_more_options()

        parametros_completos = {**parametros_fisica, **parametros_plot}

        if parametros_more["multicurve"]:
            parametros_completos["script_type"] = "multicurve"
            msg_status = "Starting Multicurve Analysis... Check the console."
        elif parametros_more["searchdv2"]:
            parametros_completos["script_type"] = "searchdv2"
            msg_status = "Starting DeltaV0² Optimization Search... Check the console."
            try:
                parametros_completos["min_dv2"] = float(self.app_state.ldv2.get())
                parametros_completos["max_dv2"] = float(self.app_state.hdv2.get())
                parametros_completos["step_dv2"] = float(self.app_state.stepdv2.get())
            except ValueError:
                self.set_status("Erro: Os limites e o step do Search DV2 devem ser números!", "#E06C75")
                self.pagina_atual.btn_run.configure(state="normal", text="Run Simulation")
                return 
        else:
            parametros_completos["script_type"] = "main"
            msg_status = "Starting standard simulation... Check the console."

        self.set_status(msg_status, "#E5C07B")
        self.console_box.configure(state="normal")
        self.console_box.delete("0.0", "end")
        self.console_box.insert("end", f"--- Initiating Execution [{parametros_completos['script_type'].upper()}] ---\n")
        self.console_box.configure(state="disabled")
        
        self.pagina_atual.btn_abort.configure(state="normal", text="Abort")
        self.progressbar.pack(side="right", padx=(10, 20))
        self.micro_bars_frame.pack(side="right")
        self.progressbar.set(0.0)
        self.u0_progressbar.set(0.0)
        self.int_progressbar.set(0.0)

        run(
            parametros=parametros_completos,
            callback_sucesso=self.ao_terminar_com_sucesso,
            callback_erro=self.ao_dar_erro,
            callback_log=self.ao_receber_log,
        )

    # ? --- Abortar e Encerrar ---
    def abortar_execucao(self):
        self.set_status("Sending abort signal...", "#E06C75")
        self.escrever_console("\n\x1b[31m[!] ABORT SIGNAL INITIATED BY USER...\x1b[0m\n")

        processos_ativos = multiprocessing.active_children()
        for processo in processos_ativos:
            processo.terminate()
            processo.join(timeout=1.0)
            
        self.pagina_atual.btn_run.configure(state="normal", text="Run Simulation")
        self.pagina_atual.btn_abort.configure(state="disabled", text="Abort")
        self.set_status("Simulation aborted successfully.", "#E06C75")
        
        self.progressbar.pack_forget()
        self.micro_bars_frame.pack_forget()

    def fechar_aplicativo(self):
        self.set_status("Shutting down ASTRAEOS and clearing memory...", "#E06C75")
        self.update() 

        processos_ativos = multiprocessing.active_children()
        for processo in processos_ativos:
            processo.terminate()
            processo.join(timeout=1.0) 

        self.destroy()
        sys.exit(0)

    # * ============================================
    # * Callbacks e Sinais em Tempo Real
    # * ============================================
    # ? --- Conclusão e Falhas ---
    def ao_terminar_com_sucesso(self):
        self.after(0, self._atualizar_ui_sucesso)

    def _atualizar_ui_sucesso(self):
        self.set_status("Task completed successfully!", "#98C379")
        self.pagina_atual.btn_run.configure(state="normal", text="Run Simulation")
        self.pagina_atual.btn_update_plot.configure(state="normal", text="Update Plot")
        self.pagina_atual.btn_abort.configure(state="disabled", text="Abort")
        self.progressbar.pack_forget()
        self.micro_bars_frame.pack_forget()

        p = self.app_state.parameters_plot()
        i = self.app_state.parameters_input()
        m = self.app_state.parameters_more_options()

        try:
            if m["multicurve"]:
                figura_inicial = plot_multicurve(
                    x_ref=p["x_ref"], linestyle_ref=p["linestyle_ref"], color_ref=p["color_ref"],
                    nome_ref=p["nome_ref"], sigmas_ref=p["sigmas_ref"], sigmas_color_ref=p["sigmas_color_ref"],
                    sigmas_nome_ref=p["sigmas_nome_ref"], x_scale=p["x_scale"], y_scale=p["y_scale"],
                )
            else:
                figura_inicial = plot_perfil_output(
                    x_ref=p["x_ref"], linestyle_ref=p["linestyle_ref"], color_ref=p["color_ref"],
                    nome_ref=p["nome_ref"], sigmas_ref=p["sigmas_ref"], sigmas_color_ref=p["sigmas_color_ref"],
                    sigmas_nome_ref=p["sigmas_nome_ref"], x_scale=p["x_scale"], y_scale=p["y_scale"], cte=i["cte"],
                )
            self.exibir_grafico(figura_inicial)
            
        except FileNotFoundError:
            self.set_status("Erro: O Multicurve exige que você rode o padrão com 'Constante' ON e OFF antes!", "#E06C75")
        except Exception as e:
            self.set_status(f"Erro ao montar gráfico final: {e}", "#E06C75")

    def ao_dar_erro(self, mensagem_erro):
        self.after(0, self._atualizar_ui_erro, mensagem_erro)

    def _atualizar_ui_erro(self, erro):
        self.set_status(f"Execution error | {erro}", "#E06C75")
        self.pagina_atual.btn_run.configure(state="normal", text="Run Simulation")
        self.pagina_atual.btn_abort.configure(state="disabled", text="Abort")
        self.progressbar.pack_forget()
        self.micro_bars_frame.pack_forget()

    # ? --- Stream de Logs e Progressão ---
    def ao_receber_log(self, texto_bruto):
        if self.skip_next_newline and texto_bruto in ("\n", "\r\n"):
            self.skip_next_newline = False
            return
            
        self.skip_next_newline = False
        
        if "___UPDATE_PLOT___" in texto_bruto:
            self.skip_next_newline = True
            self.after(0, self._atualizar_grafico_parcial)
            
        elif "___PROGRESS___|" in texto_bruto:
            self.skip_next_newline = True
            matches = re.findall(r"___PROGRESS___\|([0-9.]+)", texto_bruto)
            if matches:
                try: 
                    self.after(0, self._forcar_animacao_barra, self.progressbar, float(matches[-1]))
                except ValueError: 
                    pass
                
        elif "___U0_PROGRESS___|" in texto_bruto:
            self.skip_next_newline = True
            matches = re.findall(r"___U0_PROGRESS___\|([0-9.]+)", texto_bruto)
            if matches:
                try: 
                    self.after(0, self._forcar_animacao_barra, self.u0_progressbar, float(matches[-1]))
                except ValueError: 
                    pass
                
        elif "___INT_PROGRESS___|" in texto_bruto:
            self.skip_next_newline = True
            matches = re.findall(r"___INT_PROGRESS___\|([0-9.]+)", texto_bruto)
            if matches:
                try: 
                    self.after(0, self._forcar_animacao_barra, self.int_progressbar, float(matches[-1]))
                except ValueError: 
                    pass
                
        else:
            self.after(0, self.escrever_console, texto_bruto)


# * ============================================
# * Inicialização do Aplicativo
# * ============================================
if __name__ == "__main__":
    multiprocessing.freeze_support()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = AppWindow()
    app.mainloop()