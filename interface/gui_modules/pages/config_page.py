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
        """
        Inicializa o frame de configurações.

        Args:
            master: O widget pai (geralmente a janela principal).
            state (AppState): A instância do cofre de dados central.
            on_run_click (function): Callback disparado ao clicar em 'Rodar Simulação'.
        """
        super().__init__(master)
        self.app_state = state
        self.on_run_click = on_run_click

        # Configuração de expansão do grid principal
        self.grid_rowconfigure(1, weight=1)  # Faz as abas expandirem
        self.grid_columnconfigure(0, weight=1)

        # --- 1. Título Geral ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="Parâmetros de Simulação JPO", font=("Arial", 22, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, pady=(10, 5), sticky="w", padx=20)

        # --- 2. Sistema de Abas (Tabview) ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Criando as abas
        aba_astro = self.tabview.add("Astro & Coroa")
        aba_onda = self.tabview.add("Vento & Onda")
        aba_num = self.tabview.add("Ajustes Numéricos")

        self._construir_aba_astro(aba_astro)
        self._construir_aba_onda(aba_onda)
        self._construir_aba_numerico(aba_num)

        # --- 3. Rodapé Fixo (Ações e Status) ---
        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.frame_rodape.grid_columnconfigure(0, weight=1)

        self.btn_run = ctk.CTkButton(
            self.frame_rodape,
            text="Rodar Simulação",
            command=self.iniciar_processo,
            fg_color="#D55E00",
            font=("Arial", 14, "bold"),
            height=40,
        )
        self.btn_run.grid(row=0, column=0, pady=(0, 10))

    # * ============================================
    # * Construtores de Abas Internas
    # * ============================================
    def _construir_aba_astro(self, aba):
        """Monta os inputs referentes às propriedades da estrela e coroa."""
        # Configuração de colunas para alinhar Label e Entry
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)

        # Estrutura: Linha, Texto, Variável do AppState
        campos = [
            (0, "Nome da Estrela:", self.app_state.nome),
            (1, "Massa [Msun]:", self.app_state.Mstar),
            (2, "Raio [Rsun]:", self.app_state.Rstar),
            (3, "Temp. Efetiva (Teff) [K]:", self.app_state.Teff),
            (4, "Temp. Coronal (T) [K]:", self.app_state.T),
            (5, "Densidade Base (rho0) [g/cm³]:", self.app_state.rho0),
            (6, "Campo Magnético (B0) [G]:", self.app_state.B0),
            (7, "Peso Molecular (mu):", self.app_state.mu),
        ]

        for linha, texto, var in campos:
            ctk.CTkLabel(aba, text=texto).grid(
                row=linha, column=0, padx=10, pady=5, sticky="e"
            )
            ctk.CTkEntry(aba, textvariable=var).grid(
                row=linha, column=1, padx=10, pady=5, sticky="w"
            )

    def _construir_aba_onda(self, aba):
        """Monta os inputs referentes aos parâmetros da onda Alfvén e geometria."""
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)

        campos = [
            (0, "Fator de Expansão (S):", self.app_state.S_divergencia),
            (1, "Amplitude Inicial (deltav0) [ve0²]:", self.app_state.deltav0),
            (2, "Fluxo Inicial (phi0) [erg/cm²/s]:", self.app_state.phi0),
            (3, "Comp. Amortecimento (L0) [r0]:", self.app_state.L0),
        ]

        for linha, texto, var in campos:
            ctk.CTkLabel(aba, text=texto).grid(
                row=linha, column=0, padx=10, pady=5, sticky="e"
            )
            ctk.CTkEntry(aba, textvariable=var).grid(
                row=linha, column=1, padx=10, pady=5, sticky="w"
            )

    def _construir_aba_numerico(self, aba):
        """Monta os inputs de controle da malha do Runge-Kutta e busca de raízes."""
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)

        campos = [
            (0, "Distância de Simulação (x_sim):", self.app_state.x_sim),
            (1, "Passo de Integração (h_rk):", self.app_state.h_rk),
            (2, "Busca u0 - Limite Inf. (u0_ini):", self.app_state.u0_ini),
            (3, "Busca u0 - Passo (u0_step):", self.app_state.u0_step),
            (4, "Tamanho do Pulo (tamanho_pulo):", self.app_state.tamanho_pulo),
            (5, "Passos Recuados (recuo_pulo):", self.app_state.recuo_pulo),
        ]

        for linha, texto, var in campos:
            ctk.CTkLabel(aba, text=texto).grid(
                row=linha, column=0, padx=10, pady=5, sticky="e"
            )
            ctk.CTkEntry(aba, textvariable=var).grid(
                row=linha, column=1, padx=10, pady=5, sticky="w"
            )

        # Checkbox booleano para amortecimento constante vs ressonante (Linha 6)
        ctk.CTkCheckBox(
            aba, text="Usar Amortecimento Constante (cte)", variable=self.app_state.cte
        ).grid(row=6, column=0, columnspan=2, pady=15)

    # * ============================================
    # * Ações e Eventos
    # * ============================================
    def iniciar_processo(self):
        """Acionado ao clicar no botão de rodar. Trava a interface e delega a ação."""
        # Desabilita o botão para evitar múltiplos cliques acidentais
        self.btn_run.configure(state="disabled", text="Calculando...")

        # Avisa a janela principal (app_window.py) para disparar a thread
        self.on_run_click()
