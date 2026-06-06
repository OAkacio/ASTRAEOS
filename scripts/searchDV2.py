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
from astraeos_core.lib import *


# * ============================================
# * Rotina de Otimização e Busca de DeltaV0²
# * ============================================
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
    habitabilidade,
    exoplanet_name,
    Lstar,
    e,
    Ab,
    f0,
    Mmag,
    Dorb,
    Rplan,
    parker,
    min_dv2,
    max_dv2,
    step_dv2,
    show_progress=True,
    **kwargs,
):
    # ? --- Inicialização de Varredura ---
    search = [min_dv2, max_dv2]
    idv2 = search[0]
    idv2_salvos = []
    uinf_salvos = []
    i = 1

    if step_dv2 > 0:
        total_runs = int(round((search[1] - search[0]) / step_dv2, 5)) + 1
    else:
        total_runs = 1

    # ? --- Loop de Execução e Integração ---
    while idv2 <= search[1]:
        try:
            progresso_atual = (i - 1) / total_runs
            print(f"___PROGRESS___|{progresso_atual}", flush=True)

            x_tot, y_tot, x_crit, y_crit, x_t, ve0, *_ = main(
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
                deltav0=idv2,
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
                habitabilidade=False,
                exoplanet_name=exoplanet_name_,
                Lstar=Lstar_,
                e=e_,
                Ab=Ab_,
                f0=f0_,
                Mmag=Mmag_,
                Dorb=Dorb_,
                Rplan=Rplan_,
                parker=parker_,
                min_dv2=min_dv2_,
                max_dv2=max_dv2_,
                step_dv2=step_dv2_,
                show_progress=False,
            )

            if y_tot[-1] > 0.2:
                idv2_salvos.append(idv2)
                uinf_salvos.append(y_tot[-1])

            print("___UPDATE_PLOT___", flush=True)

        except Exception as e:
            sy.ok(f"Falha na tentativa {i}! Erro: {e}", False)

        idv2 += step_dv2
        i += 1

    print("___PROGRESS___|1.0", flush=True)

    sy.status("Displaying successfully integrated parameters...", flush=True)
    sy.table(
        ("Initial Amplitude [ ve0 ]", *idv2_salvos),
        ("Terminal Velocity [ ve0 ]", *uinf_salvos),
        mode="column",
        flush=True,
    )
    sy.fim("SEARCH COMPLETED", flush=True)
    return None


# * ============================================
# * Execução em Linha de Comando
# * ============================================
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
        habitabilidade=False,
        exoplanet_name=exoplanet_name_,
        Lstar=Lstar_,
        e=e_,
        Ab=Ab_,
        f0=f0_,
        Mmag=Mmag_,
        Dorb=Dorb_,
        Rplan=Rplan_,
        parker=parker_,
        min_dv2=min_dv2_,
        max_dv2=max_dv2_,
        step_dv2=step_dv2_,
        show_progress=False,
    )
