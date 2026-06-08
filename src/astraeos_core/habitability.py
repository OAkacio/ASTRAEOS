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
    exoplanet_name,
    k_cme,
    hion,
):
    # ? --- Cálculo de ZH ---
    sy.status("Loading input parameters...", flush=True)
    sy.param(
        ("Exoplanet Designation", exoplanet_name, ""),
        ("Orbital Distance ( Dorb )", Dorb, "AU"),
        ("Orbital Eccentricity ( e )", e, "dim"),
        ("Bond Albedo ( Ab )", Ab, "dim"),
        ("Planetary Radius ( Rₚ )", Rplan, "R⊕"),
        ("Magnetic Dipole Moment ( Mmag )", Mmag, "Am²"),
        ("Chapman-Ferraro Factor ( f₀ )", f0, "dim"),
        ("Compression Factor ( k )",k_cme,"dim"),
        ("Ionosphere Height ( hion )",hion,"km"),
        flush=True,
    )
    sy.status("Calculating habitable zone distances...", flush=True)
    d_int_rv, d_int_rg, d_int_mg, d_ext_mg, d_ext_em = distancia_habitavel(Lstar=Lstar, Teff=Teff, e=e, Rstar_sun=Rstar)
    dc_int, dc_ext = distancia_habitavel_classic(
        Rstar_sun=Rstar,
        Teff=Teff,
        Ab=Ab,
    )
    sy.param(
        ("Kopparapu Recent Venus Inner Edge", d_int_rv, "R★"),
        ("Kopparapu Runaway Greenhouse Inner Edge", d_int_rg, "R★"),
        ("Kopparapu Moist Greenhouse Inner Edge", d_int_mg, "R★"),
        ("Kopparapu Maximum Greenhouse Outer Edge", d_ext_mg, "R★"),
        ("Kopparapu Early Mars Outer Edge", d_ext_em, "R★"),
        ("Classic Inner Edge", dc_int, "R★"),
        ("Classic Outer Edge", dc_ext, "R★"),
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
        ("Ram Pressure ( Pdyn )", P_din, "Pa"),
        ("Magnetopause Radius ( Rm )", Rmag, "R⊕"),
        ("Normalized Magnetopause Radius", Rmag / Rplan, "Rₚ"),
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
        "d_int_rv": d_int_rv,
        "d_int_rg": d_int_rg,
        "d_int_mg": d_int_mg,
        "d_ext_mg": d_ext_mg,
        "d_ext_em": d_ext_em,
        "dc_int": dc_int,
        "dc_ext": dc_ext,
        "P_din": P_din,
        "Rmag": Rmag,
        "k_cme":k_cme,
        "Rmag":Rmag,
        "Pdin":P_din,
        "Rplan":Rplan,
        "Dorb":Dorb,
        "Mmag":Mmag,
        "f0":f0,
        "Ab":Ab,
        "e":e,
        "exoplanet_name":exoplanet_name,
        "hion":hion,
    }
    for chave, novo_valor in novos_valores.items():
        dadosdic[chave] = novo_valor
    dadosdic.update(novos_valores)
    np.savez(f"data/curve_{cte}.npz", **dadosdic)
    time.sleep(1)

    return d_int_rv, d_int_rg, d_int_mg, d_ext_mg, d_ext_em, dc_int, dc_ext, P_din, Rmag
