# * ============================================
# * Importações e Configuração de Caminhos
# * ============================================
import os
import sys
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from astraeos_core.main import main
from astraeos_core.parameters import *
from astraeos_core.plot_curve import *


# * ============================================
# * Rotina de Análise Comparativa (MultiCurve)
# * ============================================
def main_mc(
    nome,
    Mstar,
    Rstar,
    Teff,
    T,
    mu,
    rho0,
    B0,
    phi0,
    u0_step,
    u0_ini,
    h_rk,
    deltav0,
    S_divergencia,
    recuo_pulo,
    tamanho_pulo,
    cte,
    L0,
    x_sim,
    x_ref,
    linestyle_ref,
    color_ref,
    nome_ref,
    sigmas_ref,
    sigmas_color_ref,
    sigmas_nome_ref,
    x_scale,
    y_scale,
    **kwargs
):
    # ? --- Simulação do Amortecimento Ressonante ---
    print("___PROGRESS___|0.1", flush=True)

    x_totRES, y_totRES, x_critRES, y_critRES, x_t, ve0RES, *_ = main(
        nome=nome,
        Mstar=Mstar,
        Rstar=Rstar,
        Teff=Teff,
        T=T,
        mu=mu,
        rho0=rho0,
        B0=B0,
        phi0=phi0,
        u0_step=u0_step,
        u0_ini=u0_ini,
        h_rk=h_rk,
        deltav0=deltav0,
        S_divergencia=S_divergencia,
        recuo_pulo=recuo_pulo,
        tamanho_pulo=tamanho_pulo,
        cte=False,
        L0=L0,
        x_sim=x_sim,
        x_ref=x_ref,
        linestyle_ref=linestyle_ref,
        color_ref=color_ref,
        nome_ref=nome_ref,
        sigmas_ref=sigmas_ref,
        sigmas_color_ref=sigmas_color_ref,
        sigmas_nome_ref=sigmas_nome_ref,
        x_scale=x_scale,
        y_scale=y_scale,
        show_progress=False,
    )

    # ? --- Simulação do Amortecimento Constante ---
    print("___PROGRESS___|0.5", flush=True)

    x_totCTE, y_totCTE, x_critCTE, y_critCTE, x_t, ve0CTE, *_ = main(
        nome=nome,
        Mstar=Mstar,
        Rstar=Rstar,
        Teff=Teff,
        T=T,
        mu=mu,
        rho0=rho0,
        B0=B0,
        phi0=phi0,
        u0_step=u0_step,
        u0_ini=u0_ini,
        h_rk=h_rk,
        deltav0=deltav0,
        S_divergencia=S_divergencia,
        recuo_pulo=recuo_pulo,
        tamanho_pulo=tamanho_pulo,
        cte=True,
        L0=L0,
        x_sim=x_sim,
        x_ref=x_ref,
        linestyle_ref=linestyle_ref,
        color_ref=color_ref,
        nome_ref=nome_ref,
        sigmas_ref=sigmas_ref,
        sigmas_color_ref=sigmas_color_ref,
        sigmas_nome_ref=sigmas_nome_ref,
        x_scale=x_scale,
        y_scale=y_scale,
        show_progress=False,
    )

    # ? --- Renderização do Gráfico Unificado ---
    print("___PROGRESS___|0.9", flush=True)

    plot_multicurve(
        x_ref,
        linestyle_ref,
        color_ref,
        nome_ref,
        sigmas_ref,
        sigmas_color_ref,
        sigmas_nome_ref,
        x_scale,
        y_scale,
    )

    print("___PROGRESS___|1.0", flush=True)


# * ============================================
# * Execução em Linha de Comando
# * ============================================
if __name__ == "__main__":
    main_mc(
        nome=nome_,
        Mstar=Mstar_,
        Rstar=Rstar_,
        Teff=Teff_,
        T=T_,
        mu=mu_,
        rho0=rho0_,
        B0=B0_,
        phi0=phi0_,
        u0_step=u0_step_,
        u0_ini=u0_ini_,
        h_rk=h_rk_,
        deltav0=deltav0_,
        S_divergencia=S_divergencia_,
        recuo_pulo=recuo_pulo_,
        tamanho_pulo=tamanho_pulo_,
        cte=cte_,
        L0=L0_,
        x_sim=x_sim_,
        x_ref=x_ref_,
        linestyle_ref=linestyle_ref_,
        color_ref=color_ref_,
        nome_ref=nome_ref_,
        sigmas_ref=sigmas_ref_,
        sigmas_color_ref=sigmas_color_ref_,
        sigmas_nome_ref=sigmas_nome_ref_,
        x_scale=x_scale_,
        y_scale=y_scale_,
    )
