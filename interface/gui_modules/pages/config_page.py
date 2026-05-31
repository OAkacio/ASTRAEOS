# * ============================================
# * Importações
# * ============================================
import tkinter as tk
import customtkinter as ctk


# * ============================================
# * Componentes de Interface Auxiliares
# * ============================================
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.mostrar_tooltip)
        self.widget.bind("<Leave>", self.ocultar_tooltip)

    def mostrar_tooltip(self, event):
        x = event.x_root + 15
        y = event.y_root + 15

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#282C34",
            foreground="#ABB2BF",
            relief="solid",
            borderwidth=1,
            font=("Roboto", 10, "normal"),
            padx=8,
            pady=4,
            justify="left",
        )
        label.pack()

    def ocultar_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# * ============================================
# * Classe Principal: Página de Configuração
# * ============================================
class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, state, on_run_click, on_update_click, on_abort_click):
        super().__init__(master, corner_radius=0)

        # ? --- Injeção de Dependências ---
        self.app_state = state
        self.on_run_click = on_run_click
        self.on_update_click = on_update_click
        self.on_abort_click = on_abort_click

        # ? --- Configuração de Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.lbl_titulo = ctk.CTkLabel(
            self, text="Simulation Settings", font=("Consolas", 18, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, pady=(10, 2), sticky="w", padx=20)

        # ? --- Gestor de Abas ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        aba_astro = self.tabview.add("Star & Corona")
        aba_onda = self.tabview.add("Wind & Wave")
        aba_num = self.tabview.add("Numerical Setup")
        aba_gp = self.tabview.add("Plot Preferences")
        aba_more = self.tabview.add("More Options")

        self._construir_aba_astro(aba_astro)
        self._construir_aba_onda(aba_onda)
        self._construir_aba_numerico(aba_num)
        self._construir_aba_gp(aba_gp)
        self._construir_aba_more(aba_more)

        # ? --- Rodapé e Botões de Controle ---
        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.frame_rodape.grid_columnconfigure(0, weight=1)
        self.frame_rodape.grid_columnconfigure(1, weight=1)

        self.btn_run = ctk.CTkButton(
            self.frame_rodape,
            text="Run Simulation",
            command=self.iniciar_processo,
            fg_color="#5C7174",
            font=("Consolas", 14, "bold"),
            height=30,
        )
        self.btn_run.grid(row=0, column=0, sticky="ew")

        self.btn_abort = ctk.CTkButton(
            self.frame_rodape,
            text="Abort",
            command=self.abortar_processo,
            fg_color="#75353A",
            hover_color="#77312A",
            font=("Consolas", 14, "bold"),
            height=30,
            state="disabled",
        )
        self.btn_abort.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    # * ============================================
    # * Construtores de Abas
    # * ============================================
    # ? --- Aba: Star & Corona ---
    def _construir_aba_astro(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Star name:", self.app_state.nome, ""),
            (1, "Star Mass ( M ) :", self.app_state.Mstar, "[ Msun ]"),
            (2, "Star Radius ( R ) :", self.app_state.Rstar, "[ Rsun ]"),
            (3, "Effective Temperature ( Teff ) :", self.app_state.Teff, "[ K ]"),
            (4, "Coronal Temperature ( T ) :", self.app_state.T, "[ K ]"),
            (5, "Coronal Density ( rho0 ) :", self.app_state.rho0, "[ g/cm³ ]"),
            (6, "Surface Magnetic Field ( B0 ) :", self.app_state.B0, "[ G ]"),
            (7, "Average Molecular Weight ( mu ) :", self.app_state.mu, "[ dim ]"),
        ]

        for linha, texto, var, uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10, 0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0, 50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    # ? --- Aba: Wind & Wave ---
    def _construir_aba_onda(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Expansion Factor ( S ) :", self.app_state.S_divergencia, "[ dim ]"),
            (1, "Initial Amplitude ( DeltaV0² ) :", self.app_state.deltav0, "[ ve0² ]"),
            (2, "Initial Flux ( phi0 ) :", self.app_state.phi0, "[ erg/cm²/s ]"),
            (3, "Damping Length ( L0 ) :", self.app_state.L0, "[ r0 ]"),
        ]

        for linha, texto, var, uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10, 0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0, 50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

        ctk.CTkCheckBox(
            aba, text="Use Constant Damping (Non-Resonant)", variable=self.app_state.cte
        ).grid(row=6, column=0, columnspan=3, pady=15)

    # ? --- Aba: Numerical Setup ---
    def _construir_aba_numerico(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Simulation Distance :", self.app_state.x_sim, "[ Rstar ]"),
            (1, "Integration Step :", self.app_state.h_rk, "[ Rstar ]"),
            (2, "u0 Search - Lower Limit :", self.app_state.u0_ini, "[ ve0 ]"),
            (3, "u0 Search - Step :", self.app_state.u0_step, "[ ve0 ]"),
            (4, "Jump Size :", self.app_state.tamanho_pulo, "[ Rstar ]"),
            (5, "Backwards Steps :", self.app_state.recuo_pulo, "[ 1e-5 Rstar ]"),
        ]

        for linha, texto, var, uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10, 0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0, 50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    # ? --- Aba: Plot Preferences ---
    def _construir_aba_gp(self, aba):
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        headers = ["Distance [r0]", "Label", "Color [Hex]", "Line Style"]
        for col, text in enumerate(headers):
            aba.grid_columnconfigure(col, weight=1)
            ctk.CTkLabel(aba, text=text, font=fonte, text_color="#E5C07B").grid(
                row=0, column=col, pady=(5, 5)
            )

        for i, ref in enumerate(self.app_state.refs):
            row = i + 1
            ctk.CTkEntry(
                aba, textvariable=ref["x"], font=fonte_var, width=65, justify="center"
            ).grid(row=row, column=0, padx=5, pady=5)
            ctk.CTkEntry(
                aba,
                textvariable=ref["nome"],
                font=fonte_var,
                width=65,
                justify="center",
            ).grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkEntry(aba, textvariable=ref["cor"], width=80, justify="center").grid(
                row=row, column=2, padx=5, pady=5
            )

            estilos = ["-", "--", "-.", ":"]
            ctk.CTkComboBox(
                aba,
                variable=ref["estilo"],
                font=fonte_var,
                values=estilos,
                width=70,
                state="readonly",
            ).grid(row=row, column=3, padx=5, pady=5)

        row_offset = len(self.app_state.refs) + 1

        ctk.CTkLabel(aba, text="Sigma Zone", font=fonte, text_color="#E5C07B").grid(
            row=row_offset, column=0, columnspan=4, pady=(10, 5)
        )
        frame_sigma = ctk.CTkFrame(aba, fg_color="transparent")
        frame_sigma.grid(row=row_offset + 1, column=0, columnspan=4, pady=5)

        ctk.CTkLabel(frame_sigma, text="From:").grid(row=0, column=0, padx=5)
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_ini, font=fonte_var, width=55
        ).grid(row=0, column=1, padx=5)

        ctk.CTkLabel(frame_sigma, text="To:").grid(row=0, column=2, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_fim, font=fonte_var, width=55
        ).grid(row=0, column=3, padx=5)

        ctk.CTkLabel(frame_sigma, text="Label:").grid(row=0, column=4, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma,
            textvariable=self.app_state.sigma_nome,
            font=fonte_var,
            width=50,
        ).grid(row=0, column=5, padx=5)

        ctk.CTkLabel(frame_sigma, text="Color:").grid(row=0, column=6, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_cor, font=fonte_var, width=75
        ).grid(row=0, column=7, padx=5)

        row_offset += 2
        ctk.CTkLabel(aba, text="Axis Scales", font=fonte, text_color="#E5C07B").grid(
            row=row_offset, column=0, columnspan=4, pady=(10, 5)
        )

        frame_axis = ctk.CTkFrame(aba, fg_color="transparent")
        frame_axis.grid(row=row_offset + 1, column=0, columnspan=4, pady=5)

        estilos_escala = ["log", "linear"]

        ctk.CTkLabel(frame_axis, text="X Axis Scale:").grid(row=0, column=0, padx=5)
        ctk.CTkComboBox(
            frame_axis,
            variable=self.app_state.axis["X Axis"],
            font=fonte_var,
            values=estilos_escala,
            width=100,
            state="readonly",
        ).grid(row=0, column=1, padx=5)

        ctk.CTkLabel(frame_axis, text="Y Axis Scale:").grid(
            row=0, column=2, padx=(30, 5)
        )
        ctk.CTkComboBox(
            frame_axis,
            variable=self.app_state.axis["Y Axis"],
            font=fonte_var,
            values=estilos_escala,
            width=100,
            state="readonly",
        ).grid(row=0, column=3, padx=5)

        row_offset += 2
        self.btn_update_plot = ctk.CTkButton(
            aba,
            text="Update Plot",
            command=self.iniciar_replot,
            fg_color="#5C7174",
            state="disabled",
        )
        self.btn_update_plot.grid(row=row_offset, column=0, columnspan=4, pady=(20, 10))

    # ? --- Aba: More Options ---
    def _construir_aba_more(self, aba):
        aba.grid_columnconfigure(0, weight=1)

        fonte_titulo = ctk.CTkFont(family="Consolas", size=14, weight="bold")
        fonte_check = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        ctk.CTkLabel(
            aba,
            text="Advanced Execution Scripts",
            font=fonte_titulo,
            text_color="#E5C07B",
        ).grid(row=0, column=0, pady=(20, 15), sticky="w", padx=30)

        cb_multicurve = ctk.CTkCheckBox(
            aba,
            text="Run Multicurve Analysis (Resonant vs Constant Damping)",
            variable=self.app_state.multicurve,
            font=fonte_check,
            fg_color="#61AFEF",
            hover_color="#56B6C2",
            command=self._on_multicurve_toggle,
        )
        cb_multicurve.grid(row=1, column=0, padx=30, pady=10, sticky="w")
        ToolTip(
            cb_multicurve,
            "Executa a simulação duas vezes e sobrepõe os perfis\n de velocidade no mesmo gráfico.",
        )

        cb_searchdv2 = ctk.CTkCheckBox(
            aba,
            text="Run DeltaV0² Search Script",
            variable=self.app_state.searchdv2,
            font=fonte_check,
            fg_color="#61AFEF",
            hover_color="#56B6C2",
            command=self._alternar_parametros_dv2,
        )
        cb_searchdv2.grid(row=2, column=0, padx=30, pady=(10, 0), sticky="w")
        ToolTip(
            cb_searchdv2,
            "Ativa o algoritmo de otimização para encontrar o melhor\n valor de amplitude inicial para as ondas de Alfvén. \nPode ser muito demorado.",
        )

        self.frame_dv2 = ctk.CTkFrame(aba, fg_color="transparent")
        self.frame_dv2.grid(row=3, column=0, padx=(60, 30), pady=(5, 15), sticky="w")

        self.lbl_ldv2 = ctk.CTkLabel(
            self.frame_dv2, text="Lower limit:", font=fonte_check
        )
        self.lbl_ldv2.grid(row=0, column=0, padx=(0, 5))
        self.entry_ldv2 = ctk.CTkEntry(
            self.frame_dv2, textvariable=self.app_state.ldv2, font=fonte_var, width=60
        )
        self.entry_ldv2.grid(row=0, column=1, padx=(0, 20))

        self.lbl_hdv2 = ctk.CTkLabel(
            self.frame_dv2, text="Upper limit:", font=fonte_check
        )
        self.lbl_hdv2.grid(row=0, column=2, padx=(0, 5))
        self.entry_hdv2 = ctk.CTkEntry(
            self.frame_dv2, textvariable=self.app_state.hdv2, font=fonte_var, width=60
        )
        self.entry_hdv2.grid(row=0, column=3, padx=(0, 20))

        self.lbl_stepdv2 = ctk.CTkLabel(self.frame_dv2, text="Step:", font=fonte_check)
        self.lbl_stepdv2.grid(row=0, column=4, padx=(0, 5))
        self.entry_stepdv2 = ctk.CTkEntry(
            self.frame_dv2,
            textvariable=self.app_state.stepdv2,
            font=fonte_var,
            width=60,
        )
        self.entry_stepdv2.grid(row=0, column=5, padx=(0, 0))

        self.lbl_contagem_dv2 = ctk.CTkLabel(
            self.frame_dv2,
            text="Estimated runs: 0",
            font=("Roboto", 11, "normal"),
            text_color="#5c6269",
        )
        self.lbl_contagem_dv2.grid(
            row=1, column=0, columnspan=6, pady=(8, 0), sticky="e"
        )

        self.app_state.ldv2.trace_add("write", self._atualizar_contagem_dv2)
        self.app_state.hdv2.trace_add("write", self._atualizar_contagem_dv2)
        self.app_state.stepdv2.trace_add("write", self._atualizar_contagem_dv2)

        aba.grid_rowconfigure(4, weight=1)
        self._alternar_parametros_dv2()

    # * ============================================
    # * Lógica Dinâmica da Interface
    # * ============================================
    def _alternar_parametros_dv2(self):
        estado_ativo = self.app_state.searchdv2.get()
        if estado_ativo:
            self.app_state.multicurve.set(False)

        cor_texto = "#8b949e" if estado_ativo else "#5c6269"
        estado_widget = "normal" if estado_ativo else "disabled"

        self.lbl_ldv2.configure(text_color=cor_texto)
        self.lbl_hdv2.configure(text_color=cor_texto)
        self.lbl_stepdv2.configure(text_color=cor_texto)

        self.entry_ldv2.configure(state=estado_widget)
        self.entry_hdv2.configure(state=estado_widget)
        self.entry_stepdv2.configure(state=estado_widget)

        if estado_ativo:
            self.lbl_contagem_dv2.grid()
            self._atualizar_contagem_dv2()
        else:
            self.lbl_contagem_dv2.grid_remove()

    def _on_multicurve_toggle(self):
        if self.app_state.multicurve.get():
            self.app_state.searchdv2.set(False)
            self._alternar_parametros_dv2()

    def _atualizar_contagem_dv2(self, *args):
        try:
            min_val = float(self.app_state.ldv2.get())
            max_val = float(self.app_state.hdv2.get())
            step_val = float(self.app_state.stepdv2.get())

            if step_val > 0 and max_val > min_val:
                runs = int(round((max_val - min_val) / step_val, 5))
                self.lbl_contagem_dv2.configure(text=f"Estimated runs: {runs}")
            else:
                self.lbl_contagem_dv2.configure(text="Estimated runs: 0")

        except ValueError:
            self.lbl_contagem_dv2.configure(text="Estimated runs: --")

    # * ============================================
    # * Ações de Controle
    # * ============================================
    def iniciar_processo(self):
        self.btn_run.configure(state="disabled", text="Calculating...")
        self.on_run_click()

    def iniciar_replot(self):
        self.btn_update_plot.configure(state="disabled", text="Plotting...")
        self.on_update_click()

    def abortar_processo(self):
        self.btn_abort.configure(state="disabled", text="Aborting...")
        self.on_abort_click()
