try:
    from .lib import *
except ImportError:
    from lib import *

# * ============================================
# * Constantes Físicas
# * ============================================
mp = const.m_p.cgs.value  # Massa do próton [g]
kb = const.k_B.cgs.value  # Constante de Boltzmann [erg/K]
G = const.G.cgs.value  # Constante gravitacional [cm³g⁻¹s⁻²]
rsun = const.R_sun.cgs.value  # Raio Solar [cm]
rsunAU = const.R_sun.to(u.au).value  # Raio Solar [AU]
Msun = const.M_sun.cgs.value  # Massa Solar [g]
Lsun = const.L_sun.cgs.value  # Luminosidade Solar [erg/s]
perm_mag_vac = const.mu0.value  # Permeabilidade magnética do vácuo [N/A²]
Rterra = const.R_earth.value  # Raio da Terra [m]
pi = np.pi  # Valor da constante matemática PI
au_cgs = const.au.cgs.value  # Distância Astronômica em centímetros [cm]


# * ============================================
# * Constantes de Zona Habitável
# * ============================================
# ? --- Borda Interna (Recent Venus) ---
Seff_sun_int = (
    1.7763  # Fluxo solar efetivo [Lsol/AU²]
)
a_int = 1.4335e-4  # Coeficiente a [adm]
b_int = 3.3954e-9  # Coeficiente b [adm]
c_int = -7.6364e-12  # Coeficiente c [adm]
d_int = -1.1950e-15  # Coeficiente d [adm]

# ? --- Borda Interna (Runaway Greenhouse) ---
Seff_sun_int = (
    1.7763  # Fluxo solar efetivo [Lsol/AU²]
)
a_int = 1.2456e-4  # Coeficiente a [adm]
b_int = 1.4612e-8  # Coeficiente b [adm]
c_int = -7.6345e-12  # Coeficiente c [adm]
d_int = -1.7511e-15  # Coeficiente d [adm]

# ? --- Borda Interna (Moist Greenhouse) ---
Seff_sun_int = (
    1.0146  # Fluxo solar efetivo [Lsol/AU²]
)
a_int = 8.1884e-5  # Coeficiente a [adm]
b_int = 1.9394e-9  # Coeficiente b [adm]
c_int = -4.3618e-12  # Coeficiente c [adm]
d_int = -6.8260e-16  # Coeficiente d [adm]

# ? --- Borda Externa (Maximum Greenhouse) ---
Seff_sun_ext = (
    0.3507  # Fluxo solar efetivo [Lsol/AU²]
)
a_ext = 5.9578e-5  # Coeficiente a [adm]
b_ext = 1.6707e-9  # Coeficiente b [adm]
c_ext = -3.0058e-12  # Coeficiente c [adm]
d_ext = -5.1925e-16  # Coeficiente d [adm]

# ? --- Borda Externa (Early Mars) ---
Seff_sun_ext = (
    0.3207  # Fluxo solar efetivo [Lsol/AU²]
)
a_ext = 5.4471e-5  # Coeficiente a [adm]
b_ext = 1.5275e-9  # Coeficiente b [adm]
c_ext = -2.1709e-12  # Coeficiente c [adm]
d_ext = -3.8282e-16  # Coeficiente d [adm]

# ? --- Coeficientes de Zona Habitável Clássica ---
Teq_int = 303  # Temperatura de equilíbrio para a borda interna da zona habitável [K]
Teq_ext = 185  # Temperatura de equilíbrio para a borda externa da zona habitável [K]

# * ============================================
# * Constantes de Blindagem Magnetosférica
# * ============================================
Rseg_terra_at = 10.2  # Raio Padrão de Segurança da Magnetosfera (magnetosfera atual do planeta Terra) [Raios Planetários]
Rseg_terra_min = 5  # Raio Mínimo de Segurança Magnetosfera (magnetosfera paleoarqueana do planeta Terra) [Raios Planetários]
