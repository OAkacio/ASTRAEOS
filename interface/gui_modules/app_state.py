"""
Módulo de Gerenciamento de Estado (AppState)
===========================================

Este módulo atua como a Single Source of Truth para a interface gráfica
do ASTRAEOS. Ele isola os dados físicos e numéricos dos widgets, garantindo
segurança e fácil integração com o Core.
"""

# * ============================================
# * Importações
# * ============================================
import customtkinter as ctk


# * ============================================
# * Gerenciador de Estado
# * ============================================
class AppState:
    def __init__(self):
        # ? --- Inicialização de Variáveis ---
        self.nome = ctk.StringVar(value="TRAPPIST 1a")
        self.Mstar = ctk.StringVar(value="0.0898")
        self.Rstar = ctk.StringVar(value="0.1192")
        self.Teff = ctk.StringVar(value="2566.0")
        self.B0 = ctk.StringVar(value="600.0")
        self.rho0 = ctk.StringVar(value="5e-14")
        self.T = ctk.StringVar(value="2.0e6")
        self.mu = ctk.StringVar(value="0.6")
        self.S_divergencia = ctk.StringVar(value="2.5")
        self.deltav0 = ctk.StringVar(value="0.12851")
        self.phi0 = ctk.StringVar(value="5e7")
        self.L0 = ctk.StringVar(value="1.0")
        self.x_sim = ctk.StringVar(value="500.0")
        self.h_rk = ctk.StringVar(value="5e-4")
        self.u0_ini = ctk.StringVar(value="0.201")
        self.u0_step = ctk.StringVar(value="5e-4")
        self.recuo_pulo = ctk.StringVar(value="484")
        self.tamanho_pulo = ctk.StringVar(value="0.1")
        self.cte = ctk.BooleanVar(value=False)

        # ? --- Configurações de Plotagem ---
        self.refs = [
            {
                "x": ctk.StringVar(value="37.0"),
                "nome": ctk.StringVar(value="1d"),
                "cor": ctk.StringVar(value="#922424"),
                "estilo": ctk.StringVar(value=":"),
            },
            {
                "x": ctk.StringVar(value="49.0"),
                "nome": ctk.StringVar(value="1e"),
                "cor": ctk.StringVar(value="#926224"),
                "estilo": ctk.StringVar(value=":"),
            },
            {
                "x": ctk.StringVar(value="63.0"),
                "nome": ctk.StringVar(value="1f"),
                "cor": ctk.StringVar(value="#927824"),
                "estilo": ctk.StringVar(value=":"),
            },
            {
                "x": ctk.StringVar(value="77.0"),
                "nome": ctk.StringVar(value="1g"),
                "cor": ctk.StringVar(value="#439224"),
                "estilo": ctk.StringVar(value=":"),
            },
        ]

        self.sigma_ini = ctk.StringVar(value="39.7")
        self.sigma_fim = ctk.StringVar(value="84.7")
        self.sigma_nome = ctk.StringVar(value="ZH")
        self.sigma_cor = ctk.StringVar(value="#8FFF81")

    # ? --- Exportação de Parâmetros de Entrada ---
    def parameters_input(self):
        """
        Gera o dicionário de parâmetros físicos e numéricos atuais da interface.

        Returns:
            dict: Dicionário contendo os parâmetros estelares (Mstar em M_sun,
                Teff em K...), propriedades do vento (B0, rho0...), controle numérico de
                passagem pelo ponto crítico (recuo_pulo, tamanho_pulo...) e controles
                numéricos do Runge-Kutta (h_rk, x_sim...).
        """
        return {
            "nome": self.nome.get(),
            "Mstar": float(self.Mstar.get()),
            "Rstar": float(self.Rstar.get()),
            "Teff": float(self.Teff.get()),
            "T": float(self.T.get()),
            "mu": float(self.mu.get()),
            "rho0": float(self.rho0.get()),
            "B0": float(self.B0.get()),
            "phi0": float(self.phi0.get()),
            "u0_step": float(self.u0_step.get()),
            "u0_ini": float(self.u0_ini.get()),
            "h_rk": float(self.h_rk.get()),
            "deltav0": float(self.deltav0.get()),
            "S_divergencia": float(self.S_divergencia.get()),
            "recuo_pulo": int(self.recuo_pulo.get()),
            "tamanho_pulo": float(self.tamanho_pulo.get()),
            "cte": self.cte.get(),
            "L0": float(self.L0.get()),
            "x_sim": float(self.x_sim.get()),
        }

    # ? --- Exportação de Configurações de Plot ---
    def parameters_plot(self):
        """
        Gera o dicionário de configurações de geração de gráfico atuais da interface.

        Returns:
            dict: Dicionário contendo as configurações de personalização (nome_ref,
                color_ref...)
        """
        x_ref, nome_ref, color_ref, linestyle_ref = [], [], [], []

        for ref in self.refs:
            val_x = ref["x"].get().strip()
            if val_x:
                x_ref.append(float(val_x))
                nome_bruto = ref["nome"].get()
                nome_ref.append(rf"{nome_bruto} ; ${round(float(val_x), 1)}$ $r_0$")
                color_ref.append(ref["cor"].get())
                linestyle_ref.append(ref["estilo"].get())

        sigmas_ref, sigmas_nome_ref, sigmas_color_ref = [], [], []

        val_ini = self.sigma_ini.get().strip()
        val_fim = self.sigma_fim.get().strip()

        if val_ini and val_fim:
            sigmas_ref.append([float(val_ini), float(val_fim)])
            sigmas_nome_ref.append(self.sigma_nome.get())
            sigmas_color_ref.append(self.sigma_cor.get())

        return {
            "x_ref": tuple(x_ref),
            "linestyle_ref": tuple(linestyle_ref),
            "color_ref": tuple(color_ref),
            "nome_ref": tuple(nome_ref),
            "sigmas_ref": sigmas_ref,
            "sigmas_color_ref": sigmas_color_ref,
            "sigmas_nome_ref": sigmas_nome_ref,
        }
