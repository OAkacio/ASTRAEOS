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
rsunAU = const.const.R_sun.to(u.au).value  # Raio Solar [AU]
Msun = const.M_sun.cgs.value  # Massa Solar [g]
Lsun = const.L_sun.cgs.value  # Luminosidade Solar [erg/s]
perm_mag_vac = const.mu0.value  # Permeabilidade magnética do vácuo [Tm/A]
Rterra = const.R_earth.value  # Raio da Terra [cm]
pi = np.pi  # Valor da constante matemática PI
au = const.au.cgs.value  # Unidade Astronômica [m]


# * ============================================
# * Constantes de Zona Habitável
# * ============================================
# ? --- Borda Interna (Limite de Estufa Úmida) ---
Seff_sun_int = (
    1.0146  # Fluxo solar efetivo para a borda interna da zona habitável [Lsol/AU²]
)
a_int = 8.1884e-5  # Coeficiente a para a borda interna da zona habitável [adm]
b_int = 1.9394e-9  # Coeficiente b para a borda interna da zona habitável [adm]
c_int = -4.3618e-12  # Coeficiente c para a borda interna da zona habitável [adm]
d_int = -6.8260e-16  # Coeficiente d para a borda interna da zona habitável [adm]

# ? --- Borda Externa (Limite de Estufa Máxima) ---
Seff_sun_ext = (
    0.3507  # Fluxo solar efetivo para a borda externa da zona habitável [Lsol/AU²]
)
a_ext = 5.9578e-5  # Coeficiente a para a borda externa da zona habitável [adm]
b_ext = 1.6707e-9  # Coeficiente b para a borda externa da zona habitável [adm]
c_ext = -3.0058e-12  # Coeficiente c para a borda externa da zona habitável [adm]
d_ext = -5.1925e-16  # Coeficiente d para a borda externa da zona habitável [adm]

# ? --- Coeficientes de Zona Habitável Clássica ---
Teq_int = 303  # Temperatura de equilíbrio para a borda interna da zona habitável [K]
Teq_ext = 185  # Temperatura de equilíbrio para a borda externa da zona habitável [K]

# * ============================================
# * Constantes de Blindagem Magnetosférica
# * ============================================
Rp = 1.045  # Raio do planeta [Raios Terrestres]
Rseg_terra_at = 10.2  # Raio Padrão de Segurança da Magnetosfera (magnetosfera atual do planeta Terra) [Raios Planetários]
Rseg_terra_min = 5  # Raio Mínimo de Segurança Magnetosfera (magnetosfera paleoarqueana do planeta Terra) [Raios Planetários]
