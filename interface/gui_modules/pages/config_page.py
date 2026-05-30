"""
Módulo da Página de Configuração (Config Page)
==============================================

Este módulo é responsável por renderizar a interface visual de entrada
de dados (Inputs). Ele atua puramente como a 'Camada de Visão', não
armazenando dados por conta própria.

"""

# * ============================================
# * Importações
# * ============================================
import customtkinter as ctk


# * ============================================
# * Classe da Interface de Entradas
# * ============================================
class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, state, on_run_click):
        super().__init__(master, corner_radius=0)
        
        # ? --- Carrega App State e Inicia Página Principal ---
        self.app_state = state
        self.on_run_click = on_run_click

        # ? --- Configurações de Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=1) 
        self.grid_rowconfigure(3, weight=0) 

        # ? --- Título Principal ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="Simulation Settings", font=("Consolas", 18, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, pady=(10, 2), sticky="w", padx=20)

        # ? --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        aba_astro = self.tabview.add("Star & Corona")
        aba_onda = self.tabview.add("Wind & Wave")
        aba_num = self.tabview.add("Numerical Setup")
        aba_gp = self.tabview.add("Plot Preferences")

        self._construir_aba_astro(aba_astro)
        self._construir_aba_onda(aba_onda)
        self._construir_aba_numerico(aba_num)
        self._construir_aba_gp(aba_gp)

        # ? --- Rodapé e Botão ---
        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.frame_rodape.grid_columnconfigure(0, weight=1)

        self.btn_run = ctk.CTkButton(
            self.frame_rodape,
            text="Run Simulation",
            command=self.iniciar_processo,
            fg_color="#5C7174",
            font=("Consolas", 14, "bold"),
            height=30,
        )
        self.btn_run.grid(row=0, column=0, sticky="ew")

    # * ============================================
    # * Construtores de Abas Internas
    # * ============================================
    # ? --- Parâmetros de Input (Estrela) ---
    def _construir_aba_astro(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        campos = [
            (0, "Star name:", self.app_state.nome),
            (1, "Mass [Msun]:", self.app_state.Mstar),
            (2, "Radius [Rsun]:", self.app_state.Rstar),
            (3, "Effective Temperature (Teff) [K]:", self.app_state.Teff),
            (4, "Coronal Temperature (T) [K]:", self.app_state.T),
            (5, "Coronal Density [g/cm³]:", self.app_state.rho0),
            (6, "Surface magnetic field [G]:", self.app_state.B0),
            (7, "Average molecular weight [dim]:", self.app_state.mu),
        ]
        for linha, texto, var in campos:
            ctk.CTkLabel(aba, text=texto).grid(
                row=linha, column=0, padx=10, pady=5, sticky="e"
            )
            ctk.CTkEntry(aba, textvariable=var).grid(
                row=linha, column=1, padx=10, pady=5, sticky="w"
            )

    # ? --- Parâmetros de Input (Ondas) ---
    def _construir_aba_onda(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        campos = [
            (0, "Expansion Factor [dim]:", self.app_state.S_divergencia),
            (1, "Initial Amplitude [ve0²]:", self.app_state.deltav0),
            (2, "Initial Flux [erg/cm²/s]:", self.app_state.phi0),
            (3, "Damping Length [r0]:", self.app_state.L0),
        ]
        for linha, texto, var in campos:
            ctk.CTkLabel(aba, text=texto).grid(
                row=linha, column=0, padx=10, pady=5, sticky="e"
            )
            ctk.CTkEntry(aba, textvariable=var).grid(
                row=linha, column=1, padx=10, pady=5, sticky="w"
            )

    # ? --- Parâmetros de Input (Numérico) ---
    def _construir_aba_numerico(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        campos = [
            (0, "Simulation Distance [Rstar]:", self.app_state.x_sim),
            (1, "Integration Step [Rstar]:", self.app_state.h_rk),
            (2, "u0 Search - Lower Limit [ve0]:", self.app_state.u0_ini),
            (3, "u0 Search - Step [ve0]:", self.app_state.u0_step),
            (4, "Jump Size [Rstar]:", self.app_state.tamanho_pulo),
            (5, "Backwards Steps [1e-5 Rstar]:", self.app_state.recuo_pulo),
        ]
        for linha, texto, var in campos:
            ctk.CTkLabel(aba, text=texto).grid(
                row=linha, column=0, padx=10, pady=5, sticky="e"
            )
            ctk.CTkEntry(aba, textvariable=var).grid(
                row=linha, column=1, padx=10, pady=5, sticky="w"
            )
        ctk.CTkCheckBox(
            aba, text="Use Constant Damping (Non-Resonant)", variable=self.app_state.cte
        ).grid(row=6, column=0, columnspan=2, pady=15)

    # ? --- Parâmetros de Input (Gráfico) ---
    def _construir_aba_gp(self, aba):
        headers = ["Distance [r0]", "Label", "Color [Hex]", "Line Style"]
        for col, text in enumerate(headers):
            aba.grid_columnconfigure(col, weight=1)
            ctk.CTkLabel(aba, text=text, font=("Consolas", 12, "bold"), text_color="#E5C07B").grid(
                row=0, column=col, pady=(5, 5)
            )
        for i, ref in enumerate(self.app_state.refs):
            row = i + 1
            ctk.CTkEntry(aba, textvariable=ref["x"], width=65, justify="center").grid(row=row, column=0, padx=5, pady=5)
            ctk.CTkEntry(aba, textvariable=ref["nome"], width=65, justify="center").grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkEntry(aba, textvariable=ref["cor"], width=80, justify="center").grid(row=row, column=2, padx=5, pady=5)
            estilos = ["-", "--", "-.", ":"]
            cb = ctk.CTkComboBox(aba, variable=ref["estilo"], values=estilos, width=70, state="readonly")
            cb.grid(row=row, column=3, padx=5, pady=5)
        row_offset = len(self.app_state.refs) + 1
        ctk.CTkLabel(aba, text="Sigma Zone", font=("Consolas", 14, "bold"), text_color="#E5C07B").grid(
            row=row_offset, column=0, columnspan=4, pady=(25, 5)
        )
        frame_sigma = ctk.CTkFrame(aba, fg_color="transparent")
        frame_sigma.grid(row=row_offset+1, column=0, columnspan=4, pady=5)
        
        ctk.CTkLabel(frame_sigma, text="From:").grid(row=0, column=0, padx=5)
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_ini, width=55).grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(frame_sigma, text="To:").grid(row=0, column=2, padx=(15,5))
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_fim, width=55).grid(row=0, column=3, padx=5)
        
        ctk.CTkLabel(frame_sigma, text="Label:").grid(row=0, column=4, padx=(15,5))
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_nome, width=50).grid(row=0, column=5, padx=5)
        
        ctk.CTkLabel(frame_sigma, text="Color:").grid(row=0, column=6, padx=(15,5))
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_cor, width=75).grid(row=0, column=7, padx=5)

    # * ============================================
    # * Ações e Eventos
    # * ============================================
    # ? --- Dispara Thread ---
    def iniciar_processo(self):
        self.btn_run.configure(state="disabled", text="Calculating...")
        self.on_run_click()