try:
    from .lib import *
    from .utils import *
    from .parameters import *
    from .core import *
    from .plot_curve import *
except ImportError:
    from lib import *
    from utils import *
    from parameters import *
    from core import *
    from plot_curve import *


def main_hab(
    Lstar,
    Teff,
    e,
    Rstar,
    Ab,
    Dorb,
    Mmag,
    f0,
    x_tot,
    y_tot,
    rho_total,
    ve0,
    Rplan,
    r0,
    cte,
):
    # ? --- Cálculo de ZH ---
    sy.status("Calculating habitable zone distances...", flush=True)
    d_int, d_ext = distancia_habitavel(Lstar=Lstar, Teff=Teff, e=e, Rstar_sun=Rstar)
    dc_int, dc_ext = distancia_habitavel_classic(
        Rstar_sun=Rstar,
        Teff=Teff,
        Ab=Ab,
    )
    sy.param(
        ("Inner Edge Distance", d_int, "r0"),
        ("Outer Edge Distance", d_ext, "r0"),
        ("Classic Inner Edge Distance", dc_int, "r0"),
        ("Classic Outer Edge Distance", dc_ext, "r0"),
        flush=True,
    )
    time.sleep(1)
    # ? --- Raio Magnetosférico ---
    sy.status("Calculating magnetospheric standoff distance...", flush=True)
    i = find_i(x_tot, Dorb * (au_cgs / r0))
    P_din = Pram(rho_cgs=rho_total[i], u_ve0=y_tot[i], ve0_cgs=ve0)
    Rmag = raio_magnetosfera(
        rho_cgs=rho_total[i], u_ve0=y_tot[i], ve0_cgs=ve0, f0=f0, Mmag_AM2=Mmag
    )
    sy.param(
        ("Pressão Dinâmica", P_din, "Pa"),
        ("Raio Magnetosférico", Rmag, "Rearth"),
        ("Raio Magnetosférico", Rmag / Rplan, "Rplan"),
        flush=True,
    )
    time.sleep(1)
    status_mag, label_mag, color_mag = exo_status(Rmag_RT=Rmag, Rplan_RT=Rplan)
    sy.structurelog(
        message=status_mag,
        label=label_mag,
        color=color_mag,
        index="STATUS",
        flush=True,
    )

    # ? --- Salvando Valores ---
    dados = np.load(f"data/curve_{cte}.npz")
    dadosdic = dict(dados)
    dados.close()
    novos_valores = {
        "d_int": d_int,
        "d_ext": d_ext,
        "dc_int": dc_int,
        "dc_ext": dc_ext,
        "P_din": P_din,
        "Rmag": Rmag,
    }
    for chave, novo_valor in novos_valores.items():
        dadosdic[chave] = novo_valor
    dadosdic.update(novos_valores)
    np.savez(f"data/curve_{cte}.npz", **dadosdic)
    time.sleep(1)

    return d_int, d_ext, dc_int, dc_ext, P_din, Rmag
