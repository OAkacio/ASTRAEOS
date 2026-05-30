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
        self.nome = ctk.StringVar(value="TRAPPIST 1a")
        self.Mstar = ctk.DoubleVar(value=0.0898)
        self.Rstar = ctk.DoubleVar(value=0.1192)
        self.Teff = ctk.DoubleVar(value=2566.0)
        self.B0 = ctk.DoubleVar(value=600.0)
        self.rho0 = ctk.DoubleVar(value=5e-14)
        self.T = ctk.DoubleVar(value=2.0e6)
        self.mu = ctk.DoubleVar(value=0.6)
        self.S_divergencia = ctk.DoubleVar(value=2.5)
        self.deltav0 = ctk.DoubleVar(value=0.12851)
        self.phi0 = ctk.DoubleVar(value=5e7)
        self.L0 = ctk.DoubleVar(value=1.0)
        self.x_sim = ctk.DoubleVar(value=500.0)
        self.h_rk = ctk.DoubleVar(value=5e-4)
        self.u0_ini = ctk.DoubleVar(value=0.201)
        self.u0_step = ctk.DoubleVar(value=5e-4)
        self.recuo_pulo = ctk.IntVar(value=484)
        self.tamanho_pulo = ctk.DoubleVar(value=0.1)
        self.cte = ctk.BooleanVar(value=False)
        self.x_ref = (37.0, 49.0, 63.0, 77.0)
        self.linestyle_ref = (":", ":", ":", ":")
        self.color_ref = ("#922424", "#926224", "#927824", "#439224")
        self.nome_ref = (
            rf"1d ; ${round(self.x_ref[0],1)}$ $r_0$",
            rf"1e ; ${round(self.x_ref[1],1)}$ $r_0$",
            rf"1f ; ${round(self.x_ref[2],1)}$ $r_0$",
            rf"1g ; ${round(self.x_ref[3],1)}$ $r_0$",
        )
        self.sigmas_ref = [[39.7, 84.7]]
        self.sigmas_color_ref = ["#8FFF81"]
        self.sigmas_nome_ref = ["ZH"]

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
            "Mstar": self.Mstar.get(),
            "Rstar": self.Rstar.get(),
            "Teff": self.Teff.get(),
            "T": self.T.get(),
            "mu": self.mu.get(),
            "rho0": self.rho0.get(),
            "B0": self.B0.get(),
            "phi0": self.phi0.get(),
            "u0_step": self.u0_step.get(),
            "u0_ini": self.u0_ini.get(),
            "h_rk": self.h_rk.get(),
            "deltav0": self.deltav0.get(),
            "S_divergencia": self.S_divergencia.get(),
            "recuo_pulo": self.recuo_pulo.get(),
            "tamanho_pulo": self.tamanho_pulo.get(),
            "cte": self.cte.get(),
            "L0": self.L0.get(),
            "x_sim": self.x_sim.get(),
        }
    
    def plot_settings(self):
        """
        Gera o dicionário de configurações de geração de gráfico atuais da interface.
        
        Returns:
            dict: Dicionário contendo as configurações de personalização (nome_ref, 
                color_ref...)
        """
        return {
            "x_ref": self.x_ref,
            "linestyle_ref": self.linestyle_ref,
            "color_ref": self.color_ref,
            "nome_ref": self.nome_ref,
            "sigmas_ref": self.sigmas_ref,
            "sigmas_color_ref": self.sigmas_color_ref,
            "sigmas_nome_ref": self.sigmas_nome_ref,
        }
