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
    x_t = 10.0 ** (1.0 / (S_divergencia - 2.0))
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


# * ============================================
# * Zona Habitável
# * ============================================


def Seff_int(Teff):
    T_dif = Teff - 5780
    return (
        Seff_sun_int
        + a_int * T_dif
        + b_int * T_dif**2
        + c_int * T_dif**3
        + d_int * T_dif**4
    )


def Seff_ext(Teff):
    T_dif = Teff - 5780
    return (
        Seff_sun_ext
        + a_ext * T_dif
        + b_ext * T_dif**2
        + c_ext * T_dif**3
        + d_ext * T_dif**4
    )


def distancia_habitavel(Lstar, Teff, e):
    fator_ecc = (1 - e**2) ** 0.5
    d_int = (Lstar / (Seff_int(Teff) * fator_ecc)) ** 0.5
    d_ext = (Lstar / (Seff_ext(Teff) * fator_ecc)) ** 0.5
    return d_int, d_ext


def distancia_habitavel_classic(Rstar_sun, Teff, Ab):
    Rstar_au = Rstar_sun * Rsun_to_AU
    d_int = Rstar_au * 0.5 * (Teff / Teq_int) ** 2 * (1 - Ab) ** 0.5
    d_ext = Rstar_au * 0.5 * (Teff / Teq_ext) ** 2 * (1 - Ab) ** 0.5
    return d_int, d_ext
