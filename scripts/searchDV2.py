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
    x_un,
    y_un,
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

            # ! CORREÇÃO: Remoção dos "_" variáveis e inserção da varredura "idv2"
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
                deltav0=idv2,  # <--- O SEGREDO ESTÁ AQUI: O deltav0 assume o valor do loop!
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
                habitabilidade=False,  # Otimização: desliga a zona habitável durante as várias passagens para ser mais rápido
                exoplanet_name=exoplanet_name,
                Lstar=Lstar,
                e=e,
                Ab=Ab,
                f0=f0,
                Mmag=Mmag,
                Dorb=Dorb,
                Rplan=Rplan,
                parker=parker,
                x_un=x_un_,
                y_un=y_un_,
                show_progress=False,
            )

            # Só salva se a velocidade terminal for razoável (evita soluções colapsadas na tabela)
            if y_tot[-1] > 0.2:
                idv2_salvos.append(idv2)
                uinf_salvos.append(y_tot[-1])

            # Envia o gatilho assíncrono para a GUI atualizar o gráfico com esta iteração
            print("___UPDATE_PLOT___", flush=True)

        except Exception as err:
            sy.ok(f"Falha na tentativa {i}! Erro: {err}", False)

        idv2 += step_dv2
        i += 1

    print("___PROGRESS___|1.0", flush=True)

    sy.status("Displaying successfully integrated parameters...", flush=True)
    sy.table(
        ("Initial Amplitude [ ve0^2 ]", *idv2_salvos),
        ("Terminal Velocity [ ve0 ]", *uinf_salvos),
        mode="column",
        flush=True,
    )
    sy.fim("SEARCH COMPLETED", flush=True)
    return None
