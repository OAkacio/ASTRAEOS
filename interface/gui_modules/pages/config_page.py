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
    def __init__(self, master, state, on_run_click, on_update_click):
        super().__init__(master, corner_radius=0)

        # ? --- Carrega App State e Inicia Página Principal ---
        self.app_state = state
        self.on_run_click = on_run_click
        self.on_update_click = on_update_click

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
        aba_more = self.tabview.add("More Options")

        self._construir_aba_astro(aba_astro)
        self._construir_aba_onda(aba_onda)
        self._construir_aba_numerico(aba_num)
        self._construir_aba_gp(aba_gp)
        self._construir_aba_more(aba_more)

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
        aba.grid_columnconfigure(2, weight=1)
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Star name:", self.app_state.nome, ""),
            (1, "Star Mass ( M ) :", self.app_state.Mstar,"[ Msun ]"),
            (2, "Star Radius ( R ) :", self.app_state.Rstar, "[ Rsun ]"),
            (3, "Effective Temperature ( Teff ) :", self.app_state.Teff, "[ K ]"),
            (4, "Coronal Temperature ( T ) :", self.app_state.T, "[ K ]"),
            (5, "Coronal Density ( rho0 ) :", self.app_state.rho0, "[ g/cm³ ]"),
            (6, "Surface Magnetic Field ( B0 ) :", self.app_state.B0, "[ G ]"),
            (7, "Average Molecular Weight ( mu ) :", self.app_state.mu, "[ dim ]"),
        ]
        for linha, texto, var , uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10,0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0,50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    # ? --- Parâmetros de Input (Ondas) ---
    def _construir_aba_onda(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        campos = [
            (0, "Expansion Factor ( S ) :", self.app_state.S_divergencia,"[ dim ]"),
            (1, "Initial Amplitude ( DeltaV0² ) :", self.app_state.deltav0,"[ ve0² ]"),
            (2, "Initial Flux ( phi0 ) :", self.app_state.phi0, "[ erg/cm²/s ]"),
            (3, "Damping Length ( L0 ) :", self.app_state.L0, "[ r0 ]"),
        ]
        for linha, texto, var , uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10,0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0,50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)
        ctk.CTkCheckBox(
            aba, text="Use Constant Damping (Non-Resonant)", variable=self.app_state.cte
        ).grid(row=6, column=0, columnspan=3, pady=15)

    # ? --- Parâmetros de Input (Numérico) ---
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
        for linha, texto, var , uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10,0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0,50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    # ? --- Parâmetros de Input (Gráfico) ---
    def _construir_aba_gp(self, aba):
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        headers = ["Distance [r0]", "Label", "Color [Hex]", "Line Style"]
        for col, text in enumerate(headers):
            aba.grid_columnconfigure(col, weight=1)
            ctk.CTkLabel(
                aba, text=text, font=fonte, text_color="#E5C07B"
            ).grid(row=0, column=col, pady=(5, 5))
        for i, ref in enumerate(self.app_state.refs):
            row = i + 1
            ctk.CTkEntry(aba, textvariable=ref["x"], font=fonte_var, width=65, justify="center").grid(
                row=row, column=0, padx=5, pady=5
            )
            ctk.CTkEntry(
                aba, textvariable=ref["nome"], font=fonte_var, width=65, justify="center"
            ).grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkEntry(aba, textvariable=ref["cor"], width=80, justify="center").grid(
                row=row, column=2, padx=5, pady=5
            )
            estilos = ["-", "--", "-.", ":"]
            cb = ctk.CTkComboBox(
                aba, variable=ref["estilo"], font=fonte_var, values=estilos, width=70, state="readonly"
            )
            cb.grid(row=row, column=3, padx=5, pady=5)
        row_offset = len(self.app_state.refs) + 1
        ctk.CTkLabel(
            aba, text="Sigma Zone", font=fonte, text_color="#E5C07B"
        ).grid(row=row_offset, column=0, columnspan=4, pady=(25, 5))
        frame_sigma = ctk.CTkFrame(aba, fg_color="transparent")
        frame_sigma.grid(row=row_offset + 1, column=0, columnspan=4, pady=5)

        ctk.CTkLabel(frame_sigma, text="From:").grid(row=0, column=0, padx=5)
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_ini, font=fonte_var, width=55).grid(
            row=0, column=1, padx=5
        )

        ctk.CTkLabel(frame_sigma, text="To:").grid(row=0, column=2, padx=(15, 5))
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_fim, font=fonte_var, width=55).grid(
            row=0, column=3, padx=5
        )

        ctk.CTkLabel(frame_sigma, text="Label:").grid(row=0, column=4, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_nome, font=fonte_var, width=50
        ).grid(row=0, column=5, padx=5)

        ctk.CTkLabel(frame_sigma, text="Color:").grid(row=0, column=6, padx=(15, 5))
        ctk.CTkEntry(frame_sigma, textvariable=self.app_state.sigma_cor, font=fonte_var, width=75).grid(
            row=0, column=7, padx=5
        )

        row_offset += 2  # Pula duas linhas abaixo da Sigma Zone
        ctk.CTkLabel(
            aba, text="Axis Scales", font=fonte, text_color="#E5C07B"
        ).grid(row=row_offset, column=0, columnspan=4, pady=(25, 5))

        # Cria uma caixinha invisível para centralizar os controles
        frame_axis = ctk.CTkFrame(aba, fg_color="transparent")
        frame_axis.grid(row=row_offset + 1, column=0, columnspan=4, pady=5)

        estilos_escala = ["log", "linear"]

        # Controle do Eixo X
        ctk.CTkLabel(frame_axis, text="X Axis Scale:").grid(row=0, column=0, padx=5)
        cb_x = ctk.CTkComboBox(
            frame_axis,
            variable=self.app_state.axis["X Axis"],  # Puxa direto do dicionário!
            font=fonte_var,
            values=estilos_escala,
            width=100,
            state="readonly",  # Impede o usuário de digitar bobagem
        )
        cb_x.grid(row=0, column=1, padx=5)

        # Controle do Eixo Y
        ctk.CTkLabel(frame_axis, text="Y Axis Scale:").grid(
            row=0, column=2, padx=(30, 5)
        )
        cb_y = ctk.CTkComboBox(
            frame_axis,
            variable=self.app_state.axis["Y Axis"],  # Puxa direto do dicionário!
            font=fonte_var,
            values=estilos_escala,
            width=100,
            state="readonly",
        )
        cb_y.grid(row=0, column=3, padx=5)

        row_offset += 2
        self.btn_update_plot = ctk.CTkButton(
            aba,
            text="Update Plot",
            command=self.iniciar_replot,
            fg_color="#5C7174",
            state="disabled",  # Inicia bloqueado até a primeira simulação rodar
        )
        self.btn_update_plot.grid(row=row_offset, column=0, columnspan=4, pady=(20, 10))
    # ? --- Parâmetros de Input (More Options) ---
    def _construir_aba_more(self, aba):
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
        for linha, texto, var , uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10,0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0,50), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    # * ============================================
    # * Ações e Eventos
    # * ============================================
    # ? --- Dispara Thread ---
    def iniciar_processo(self):
        self.btn_run.configure(state="disabled", text="Calculating...")
        self.on_run_click()

    def iniciar_replot(self):
        self.btn_update_plot.configure(state="disabled", text="Plotting...")
        self.on_update_click()
