#
# * ============================================
# * Importações
# * ============================================
from lib import *
from utils import *
from parameters import *

# * ============================================
# * Conversões de Unidades
# * ============================================
r0 = Rstar * rsun  # Raio inicial                                               [cm]
M = Mstar * Msun  # Massa da estrela                                            [g]

# * ============================================
# * Grandezas derivadas
# * ============================================
def calc_param(dv2,S):
    ve0 = math.sqrt(2.0 * G * M / r0)  # Velocidade de escape na Superfície         [cm/s]
    cs = math.sqrt(kb * T / (mu * mp))  # Velocidade do som                         [cm/s]
    vA0 = (B0 / math.sqrt(4.0 * math.pi * rho0)) / ve0  # Velocidade de Alfvén      [ve0]
    vT = cs / ve0  # Velocidade Térmica                                             [ve0]
    x_t = 10.0 ** (1.0 / (S - 2.0))  # Raio de transição                            [r0]
    return ve0, cs, vA0, vT, x_t


# * ============================================
# * Lógica Integrada
# * ============================================
def zerosND(x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list):
    x_tot = np.concatenate([x_int, x_ext])
    y_tot = np.concatenate([y_int, y_ext])

    # Converte para arrays do NumPy
    num_alpha_array = np.array([list(row) for row in num_alpha_list])
    den_alpha_array = np.array([list(row) for row in den_alpha_list])

    # =========================================================
    # LÓGICA PARA ACHAR A PRIMEIRA TRAVESSIA PELO ZERO
    # =========================================================

    # 1. Pega apenas as colunas dos valores (Numerador e Denominador)
    valores_num = num_alpha_array[:, 0]
    valores_den = den_alpha_array[:, 0]

    # 2. Encontra os índices onde ocorre mudança de sinal
    cruza_zero_num = np.where(np.diff(np.sign(valores_num)) != 0)[0]
    cruza_zero_den = np.where(np.diff(np.sign(valores_den)) != 0)[0]

    # 3. Define os índices críticos pegando a PRIMEIRA travessia
    if len(cruza_zero_num) > 0:
        idx_antes = cruza_zero_num[0]
        idx_depois = idx_antes + 1

        if np.abs(valores_num[idx_antes]) < np.abs(valores_num[idx_depois]):
            idx_crit_num = idx_antes
        else:
            idx_crit_num = idx_depois
    else:
        # Fallback: Se não cruzou o zero, usa a lógica original
        idx_crit_num = np.argmin(np.abs(valores_num))

    # Repete a mesma lógica para o denominador
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