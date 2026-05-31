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


def main_sd(
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
    min_dv2,
    max_dv2,
    step_dv2,
):
    search = [min_dv2, max_dv2]
    idv2 = search[0]
    i=1

    while idv2 < search[1]:
        try:
            x_tot, y_tot, x_crit, y_crit, x_t, ve0, *_ = main(
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
                deltav0=idv2,
                S_divergencia=S_divergencia,
                recuo_pulo=recuo_pulo,
                tamanho_pulo=tamanho_pulo,
                cte=cte,
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
            )
        except:
            sy.ok(f"Falha na tentativa {i}!", False)
        idv2 += step_dv2
        i += 1
    return None


if __name__ == "__main__":
    main_sd(
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
        min_dv2=min_dv2_,
        max_dv2=max_dv2_,
        step_dv2=step_dv2_,
    )
