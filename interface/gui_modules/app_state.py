# * ============================================
# * Importações
# * ============================================
import customtkinter as ctk


# * ============================================
# * Gerenciador de Estado (AppState)
# * ============================================
class AppState:
    def __init__(self):
        # ? --- Variáveis Astrofísicas e Numéricas ---
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

        # ? --- Variáveis de Referência e Gráficos ---
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
        self.axis = {
            "X Axis": ctk.StringVar(value="log"),
            "Y Axis": ctk.StringVar(value="log"),
        }

        # ? --- Variáveis de Scripts Avançados ---
        self.multicurve = ctk.BooleanVar(value=False)
        self.searchdv2 = ctk.BooleanVar(value=False)
        self.ldv2 = ctk.StringVar(value="0.001")
        self.hdv2 = ctk.StringVar(value="0.010")
        self.stepdv2 = ctk.StringVar(value="0.001")

    # * ============================================
    # * Exportação de Dados (Cofres)
    # * ============================================
    # ? --- Parâmetros de Entrada ---
    def parameters_input(self):
        """
        Gera o dicionário de parâmetros físicos e numéricos atuais da interface.
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

    # ? --- Parâmetros de Plotagem ---
    def parameters_plot(self):
        """
        Gera o dicionário de configurações de geração de gráfico atuais da interface.
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
            "x_scale": self.axis["X Axis"].get(),
            "y_scale": self.axis["Y Axis"].get(),
        }

    # ? --- Opções Avançadas ---
    def parameters_more_options(self):
        """
        Gera o dicionário de controle dos scripts avançados.
        """
        return {
            "multicurve": self.multicurve.get(),
            "searchdv2": self.searchdv2.get(),
            "ldv2": self.ldv2.get(),
            "hdv2": self.hdv2.get(),
            "stepdv2": self.stepdv2.get(),
        }
