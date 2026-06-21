#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Importações                                                              │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import *
import time
from astropy import constants as const
from astropy import units as u

try:
    from .pytools import system as sy
    from .pytools import graphs as gp
    from .pytools import saveload as sl
except ImportError:
    import pytools.system as sy
    import pytools.graphs as gp
    import pytools.saveload as sl
import ctypes

#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Localiza, Carrega e Define Lib de C                                      │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_lib = os.path.join(diretorio_atual, "integrator.dll")
c_lib = ctypes.CDLL(caminho_lib)


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Mapeamento das Estruturas (Structs) do C para Python                     │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
class Pair2(ctypes.Structure):
    _fields_ = [("v", ctypes.c_double * 2)]


class BuscaU0Result(ctypes.Structure):
    _fields_ = [
        ("u0_final", ctypes.c_double),
        ("x_crit", ctypes.c_double),
        ("y_crit", ctypes.c_double),
        ("r_crit", ctypes.c_double),
        ("x_append_final", ctypes.POINTER(ctypes.c_double)),
        ("y_append_final", ctypes.POINTER(ctypes.c_double)),
        ("append_len", ctypes.c_size_t),
        ("vetor_final", ctypes.c_double * 12),
        ("vetor_final_set", ctypes.c_int),
        ("has_error", ctypes.c_int),
        ("error_msg", ctypes.c_char * 256),
    ]


class IntegraPerfilResult(ctypes.Structure):
    _fields_ = [
        ("x0n", ctypes.c_double),
        ("y0", ctypes.c_double),
        ("x_int", ctypes.POINTER(ctypes.c_double)),
        ("x_int_len", ctypes.c_size_t),
        ("y_int", ctypes.POINTER(ctypes.c_double)),
        ("y_int_len", ctypes.c_size_t),
        ("x_ext", ctypes.POINTER(ctypes.c_double)),
        ("x_ext_len", ctypes.c_size_t),
        ("y_ext", ctypes.POINTER(ctypes.c_double)),
        ("y_ext_len", ctypes.c_size_t),
        ("num_alpha_list", ctypes.POINTER(Pair2)),
        ("num_alpha_list_len", ctypes.c_size_t),
        ("den_alpha_list", ctypes.POINTER(Pair2)),
        ("den_alpha_list_len", ctypes.c_size_t),
        ("vA_total", ctypes.POINTER(ctypes.c_double)),
        ("vA_total_len", ctypes.c_size_t),
        ("rho_total", ctypes.POINTER(ctypes.c_double)),
        ("rho_total_len", ctypes.c_size_t),
        ("phi_total", ctypes.POINTER(ctypes.c_double)),
        ("phi_total_len", ctypes.c_size_t),
        ("deltav2_total", ctypes.POINTER(ctypes.c_double)),
        ("deltav2_total_len", ctypes.c_size_t),
        ("dmdt0", ctypes.c_double),
        ("L_total", ctypes.POINTER(ctypes.c_double)),
        ("L_total_len", ctypes.c_size_t),
        ("Pdin_total", ctypes.POINTER(ctypes.c_double)),
        ("Pdin_total_len", ctypes.c_size_t),
        ("has_error", ctypes.c_int),
        ("error_msg", ctypes.c_char * 256),
    ]


class IntegraPerfilParkerResult(ctypes.Structure):
    _fields_ = [
        ("u0", ctypes.c_double),
        ("x_crit", ctypes.c_double),
        ("y_crit", ctypes.c_double),
        ("x_int", ctypes.POINTER(ctypes.c_double)),
        ("x_int_len", ctypes.c_size_t),
        ("y_int", ctypes.POINTER(ctypes.c_double)),
        ("y_int_len", ctypes.c_size_t),
        ("x_ext", ctypes.POINTER(ctypes.c_double)),
        ("x_ext_len", ctypes.c_size_t),
        ("y_ext", ctypes.POINTER(ctypes.c_double)),
        ("y_ext_len", ctypes.c_size_t),
        ("num_alpha_list", ctypes.POINTER(Pair2)),
        ("num_alpha_list_len", ctypes.c_size_t),
        ("den_alpha_list", ctypes.POINTER(Pair2)),
        ("den_alpha_list_len", ctypes.c_size_t),
        ("vA_total", ctypes.POINTER(ctypes.c_double)),
        ("vA_total_len", ctypes.c_size_t),
        ("rho_total", ctypes.POINTER(ctypes.c_double)),
        ("rho_total_len", ctypes.c_size_t),
        ("phi_total", ctypes.POINTER(ctypes.c_double)),
        ("phi_total_len", ctypes.c_size_t),
        ("deltav2_total", ctypes.POINTER(ctypes.c_double)),
        ("deltav2_total_len", ctypes.c_size_t),
        ("dmdt0", ctypes.c_double),
        ("L_total", ctypes.POINTER(ctypes.c_double)),
        ("L_total_len", ctypes.c_size_t),
        ("Pdin_total", ctypes.POINTER(ctypes.c_double)),
        ("Pdin_total_len", ctypes.c_size_t),
    ]


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Assinaturas das Funções C                                                │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
ProgressCallback = ctypes.CFUNCTYPE(None, ctypes.c_double)
c_lib.busca_u0.argtypes = [
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int,
    ProgressCallback,
]
c_lib.busca_u0.restype = BuscaU0Result
c_lib.free_busca_u0_result.argtypes = [ctypes.POINTER(BuscaU0Result)]
c_lib.integra_perfil.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.c_long,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int,
    ctypes.c_double,
    ProgressCallback,
]
c_lib.integra_perfil.restype = IntegraPerfilResult
c_lib.free_integra_perfil_result.argtypes = [ctypes.POINTER(IntegraPerfilResult)]
c_lib.integra_perfil_parker.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]
c_lib.integra_perfil_parker.restype = IntegraPerfilParkerResult
c_lib.free_integra_perfil_parker_result.argtypes = [
    ctypes.POINTER(IntegraPerfilParkerResult)
]


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Funções Pythonizadas (Wrappers Transparentes)                            │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
def busca_u0(vT, vetor_base, u0_step, u0_ini, cte, py_cb):
    c_vetor = (ctypes.c_double * 12)(*vetor_base)
    c_cb = ProgressCallback(py_cb) if py_cb else ctypes.cast(None, ProgressCallback)
    res = c_lib.busca_u0(vT, c_vetor, u0_step, u0_ini, int(cte), c_cb)
    if res.has_error:
        err = res.error_msg.decode("utf-8")
        c_lib.free_busca_u0_result(ctypes.byref(res))
        raise RuntimeError(err)
    length = res.append_len
    x_app = (
        np.ctypeslib.as_array(res.x_append_final, shape=(length,)).copy()
        if length > 0
        else np.array([])
    )
    y_app = (
        np.ctypeslib.as_array(res.y_append_final, shape=(length,)).copy()
        if length > 0
        else np.array([])
    )
    v_fin = np.array(res.vetor_final) if res.vetor_final_set else np.array([])
    u0_f, xc, yc, rc = res.u0_final, res.x_crit, res.y_crit, res.r_crit
    c_lib.free_busca_u0_result(ctypes.byref(res))
    return u0_f, xc, yc, rc, x_app, y_app, v_fin


def integra_perfil(
    u0_final,
    x_crit,
    y_crit,
    vetor_final,
    x_append_final,
    y_append_final,
    x_t,
    passos_recuo,
    h_step,
    h_rk,
    cte,
    x_sim,
    py_cb,
):
    c_vetor = (ctypes.c_double * 12)(*vetor_final)
    x_append_list = (
        x_append_final.tolist()
        if isinstance(x_append_final, np.ndarray)
        else x_append_final
    )
    y_append_list = (
        y_append_final.tolist()
        if isinstance(y_append_final, np.ndarray)
        else y_append_final
    )
    l_app = len(x_append_list)
    c_x_app = (ctypes.c_double * l_app)(*x_append_list)
    c_y_app = (ctypes.c_double * l_app)(*y_append_list)
    c_cb = ProgressCallback(py_cb) if py_cb else ctypes.cast(None, ProgressCallback)
    res = c_lib.integra_perfil(
        u0_final,
        x_crit,
        y_crit,
        c_vetor,
        c_x_app,
        c_y_app,
        l_app,
        x_t,
        int(passos_recuo),
        h_step,
        h_rk,
        int(cte),
        x_sim,
        c_cb,
    )
    if res.has_error:
        err = res.error_msg.decode("utf-8")
        c_lib.free_integra_perfil_result(ctypes.byref(res))
        raise RuntimeError(err)
    x0n, y0, dmdt0 = res.x0n, res.y0, res.dmdt0
    x_int = np.ctypeslib.as_array(res.x_int, shape=(res.x_int_len,)).copy()
    y_int = np.ctypeslib.as_array(res.y_int, shape=(res.y_int_len,)).copy()
    x_ext = np.ctypeslib.as_array(res.x_ext, shape=(res.x_ext_len,)).copy()
    y_ext = np.ctypeslib.as_array(res.y_ext, shape=(res.y_ext_len,)).copy()
    num_alpha = [
        [res.num_alpha_list[i].v[0], res.num_alpha_list[i].v[1]]
        for i in range(res.num_alpha_list_len)
    ]
    den_alpha = [
        [res.den_alpha_list[i].v[0], res.den_alpha_list[i].v[1]]
        for i in range(res.den_alpha_list_len)
    ]
    vA_tot = np.ctypeslib.as_array(res.vA_total, shape=(res.vA_total_len,)).copy()
    rho_tot = np.ctypeslib.as_array(res.rho_total, shape=(res.rho_total_len,)).copy()
    phi_tot = np.ctypeslib.as_array(res.phi_total, shape=(res.phi_total_len,)).copy()
    deltav2_tot = np.ctypeslib.as_array(
        res.deltav2_total, shape=(res.deltav2_total_len,)
    ).copy()
    L_tot = np.ctypeslib.as_array(res.L_total, shape=(res.L_total_len,)).copy()
    Pdin_tot = np.ctypeslib.as_array(res.Pdin_total, shape=(res.Pdin_total_len,)).copy()
    c_lib.free_integra_perfil_result(ctypes.byref(res))
    return (
        x0n,
        y0,
        x_int,
        y_int,
        x_ext,
        y_ext,
        num_alpha,
        den_alpha,
        vA_tot,
        rho_tot,
        phi_tot,
        deltav2_tot,
        dmdt0,
        L_tot,
        Pdin_tot,
    )


def integra_perfil_parker(cs, G, M, ve0, r0, rho0, x_sim, h_rk, rsun):
    res = c_lib.integra_perfil_parker(cs, G, M, ve0, r0, rho0, x_sim, h_rk, rsun)
    u0, x_crit, y_crit, dmdt0 = res.u0, res.x_crit, res.y_crit, res.dmdt0
    x_int = np.ctypeslib.as_array(res.x_int, shape=(res.x_int_len,)).copy()
    y_int = np.ctypeslib.as_array(res.y_int, shape=(res.y_int_len,)).copy()
    x_ext = np.ctypeslib.as_array(res.x_ext, shape=(res.x_ext_len,)).copy()
    y_ext = np.ctypeslib.as_array(res.y_ext, shape=(res.y_ext_len,)).copy()
    num_alpha = [
        [res.num_alpha_list[i].v[0], res.num_alpha_list[i].v[1]]
        for i in range(res.num_alpha_list_len)
    ]
    den_alpha = [
        [res.den_alpha_list[i].v[0], res.den_alpha_list[i].v[1]]
        for i in range(res.den_alpha_list_len)
    ]
    vA_tot = np.ctypeslib.as_array(res.vA_total, shape=(res.vA_total_len,)).copy()
    rho_tot = np.ctypeslib.as_array(res.rho_total, shape=(res.rho_total_len,)).copy()
    phi_tot = np.ctypeslib.as_array(res.phi_total, shape=(res.phi_total_len,)).copy()
    deltav2_tot = np.ctypeslib.as_array(
        res.deltav2_total, shape=(res.deltav2_total_len,)
    ).copy()
    L_tot = np.ctypeslib.as_array(res.L_total, shape=(res.L_total_len,)).copy()
    Pdin_tot = np.ctypeslib.as_array(res.Pdin_total, shape=(res.Pdin_total_len,)).copy()
    c_lib.free_integra_perfil_parker_result(ctypes.byref(res))
    return (
        u0,
        x_crit,
        y_crit,
        x_int,
        y_int,
        x_ext,
        y_ext,
        num_alpha,
        den_alpha,
        vA_tot,
        rho_tot,
        phi_tot,
        deltav2_tot,
        dmdt0,
        L_tot,
        Pdin_tot,
    )
