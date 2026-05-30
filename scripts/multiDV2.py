import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from astraeos_core.main import main
from astraeos_core.lib import *
from astraeos_core.parameters import *

delta = 0.001
search = [0.15005, 0.2]
dv2 = search[0]
dados = [[], []]
while dv2 < search[1]:
    try:
        infos = main(
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
            deltav0=dv2,
            S_divergencia=S_divergencia,
            recuo_pulo=recuo_pulo,
            tamanho_pulo=tamanho_pulo,
            cte=False,
            L0=L0,
        )
        dados[0].append(infos[2])
        dados[1].append(infos[1])
    except:
        sy.ok("Falha na tentativa!", False)
    dv2 += delta
gp.plot(
    x_data=[dados[0]],
    y_data=[dados[1]],
    x_label=r"$<dv^2> (v_{e0}^2)$",
    y_label=r"$v_{\infty}$ (km/s)",
    show_plot=True,
    linestyle=[""],
    marker="o",
    linewidth=1,
    axis_fontsize=20,
    show_grid=True,
    grid_linewidth=1,
    grid_color="gray",
    grid_alpha=0.7,
    grid_linestyle="-",
)
