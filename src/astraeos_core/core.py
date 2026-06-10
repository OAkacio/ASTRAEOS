# * ============================================
# * Importações
# * ============================================
try:
    from .lib import *
    from .utils import *
    from .parameters import *
except ImportError:
    from lib import *
    from utils import *
    from parameters import *


# * ============================================
# * Grandezas Derivadas
# * ============================================
def calc_param(
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
    F,
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
):
    r0 = Rstar * rsun
    M = Mstar * Msun
    ve0 = math.sqrt(2.0 * G * M / r0)
    cs = math.sqrt(kb * T / (mu * mp))
    vA0 = (B0 / math.sqrt(4.0 * math.pi * rho0)) / ve0
    vT = cs / ve0
    x_t = 0 if S_divergencia == 2.0 else F ** (1.0 / (S_divergencia - 2.0))
    return ve0, cs, vA0, vT, x_t, r0, M


# * ============================================
# * Lógica Integrada
# * ============================================
def zerosND(x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list):
    x_tot = np.concatenate([x_int, x_ext])
    y_tot = np.concatenate([y_int, y_ext])

    num_alpha_array = np.array([list(row) for row in num_alpha_list])
    den_alpha_array = np.array([list(row) for row in den_alpha_list])

    valores_num = num_alpha_array[:, 0]
    valores_den = den_alpha_array[:, 0]

    cruza_zero_num = np.where(np.diff(np.sign(valores_num)) != 0)[0]
    cruza_zero_den = np.where(np.diff(np.sign(valores_den)) != 0)[0]

    if len(cruza_zero_num) > 0:
        idx_antes = cruza_zero_num[0]
        idx_depois = idx_antes + 1

        if np.abs(valores_num[idx_antes]) < np.abs(valores_num[idx_depois]):
            idx_crit_num = idx_antes
        else:
            idx_crit_num = idx_depois
    else:
        idx_crit_num = np.argmin(np.abs(valores_num))

    if len(cruza_zero_den) > 0:
        idx_antes = cruza_zero_den[0]
        idx_depois = idx_antes + 1

        if np.abs(valores_den[idx_antes]) < np.abs(valores_den[idx_depois]):
            idx_crit_den = idx_antes
        else:
            idx_crit_den = idx_depois
    else:
        idx_crit_den = np.argmin(np.abs(valores_den))

    return (
        x_tot,
        y_tot,
        num_alpha_array,
        den_alpha_array,
        idx_crit_num,
        idx_crit_den,
    )


def find_i(lista, valor):
    return min(range(len(lista)), key=lambda i: abs(lista[i] - valor))


# * ============================================
# * Zona Habitável
# * ============================================


def Seff_int(Teff, tipo):
    T_dif = Teff - 5780
    if tipo == "rv":
        x = (
            Seff_sun_int_rv
            + a_int_rv * T_dif
            + b_int_rv * T_dif**2
            + c_int_rv * T_dif**3
            + d_int_rv * T_dif**4
        )
    elif tipo == "rg":
        x = (
            Seff_sun_int_rg
            + a_int_rg * T_dif
            + b_int_rg * T_dif**2
            + c_int_rg * T_dif**3
            + d_int_rg * T_dif**4
        )
    elif tipo == "mg":
        x = (
            Seff_sun_int_mg
            + a_int_mg * T_dif
            + b_int_mg * T_dif**2
            + c_int_mg * T_dif**3
            + d_int_mg * T_dif**4
        )
    return x


def Seff_ext(Teff, tipo):
    T_dif = Teff - 5780
    if tipo == "mg":
        x = (
            Seff_sun_ext_mg
            + a_ext_mg * T_dif
            + b_ext_mg * T_dif**2
            + c_ext_mg * T_dif**3
            + d_ext_mg * T_dif**4
        )
    elif tipo == "em":
        x = (
            Seff_sun_ext_em
            + a_ext_em * T_dif
            + b_ext_em * T_dif**2
            + c_ext_em * T_dif**3
            + d_ext_em * T_dif**4
        )
    return x


def distancia_habitavel(Lstar, Teff, e, Rstar_sun):
    fator_ecc = (1 - e**2) ** 0.5
    d_int_au_rv = (Lstar / (Seff_int(Teff, "rv") * fator_ecc)) ** 0.5
    d_int_au_rg = (Lstar / (Seff_int(Teff, "rg") * fator_ecc)) ** 0.5
    d_int_au_mg = (Lstar / (Seff_int(Teff, "mg") * fator_ecc)) ** 0.5
    d_ext_au_mg = (Lstar / (Seff_ext(Teff, "mg") * fator_ecc)) ** 0.5
    d_ext_au_em = (Lstar / (Seff_ext(Teff, "em") * fator_ecc)) ** 0.5
    fator_conversao = au_cgs / (Rstar_sun * rsun)
    d_int_rv = d_int_au_rv * fator_conversao
    d_int_rg = d_int_au_rg * fator_conversao
    d_int_mg = d_int_au_mg * fator_conversao
    d_ext_mg = d_ext_au_mg * fator_conversao
    d_ext_em = d_ext_au_em * fator_conversao
    return d_int_rv, d_int_rg, d_int_mg, d_ext_mg, d_ext_em


def distancia_habitavel_classic(Rstar_sun, Teff, Ab):
    Rstar_au = (Rstar_sun * rsun) / au_cgs
    d_int_au = Rstar_au * 0.5 * (Teff / Teq_int) ** 2 * (1 - Ab) ** 0.5
    d_ext_au = Rstar_au * 0.5 * (Teff / Teq_ext) ** 2 * (1 - Ab) ** 0.5
    fator_conversao = au_cgs / (Rstar_sun * rsun)
    return d_int_au * fator_conversao, d_ext_au * fator_conversao


# * ============================================
# * Blindagem Magnetosférica
# * ============================================


def Pram(rho_cgs, u_ve0, ve0_cgs):
    u_cgs = u_ve0 * ve0_cgs
    conversao_cgs_to_SI = 0.1
    return (rho_cgs * u_cgs**2) * conversao_cgs_to_SI


def raio_magnetosfera(rho_cgs, u_ve0, ve0_cgs, f0, Mmag_AM2):
    N = perm_mag_vac * f0**2 * Mmag_AM2**2
    D = 8 * pi**2 * Pram(rho_cgs, u_ve0, ve0_cgs)
    convcersao_SI_to_RaiosTerrastres = 1 / Rterra
    return ((N / D) ** (1 / 6)) * convcersao_SI_to_RaiosTerrastres


def exo_status(Rmag_RT, Rplan_RT):
    Rmag_RP = Rmag_RT / Rplan_RT
    if Rmag_RP > Rseg_terra_at:
        return "Extended Magnetosphere", "Safe Zone", "lightgreen"
    elif Rseg_terra_min <= Rmag_RP and Rmag_RP <= Rseg_terra_at:
        return "Compressed Magnetosphere", "Marginal Zone", "cyan"
    else:
        return "Sub-critical Shield", "Unsafe Zone", "red"


def Apc(Rmg_terra, Rio_km):
    Rmg, Rio = Rmg_terra * Rterra / 1000, Rio_km
    At=4*pi*Rio**2
    return (100*(2 * pi * Rio ** 3) / (Rmg))/At
