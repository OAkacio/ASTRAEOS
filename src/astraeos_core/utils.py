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
# * Constantes de Zona Habitável (Interna)
# * ============================================
# ? --- Borda Interna (Recent Venus) --- [empirico/otimista: Fluxo de energia recebida por Vênus no momento que 'morreu']
Seff_sun_int_rv = (
    1.7763  # Fluxo solar efetivo [Lsol/AU²]
)
a_int_rv = 1.4335e-4  # Coeficiente a [adm]
b_int_rv = 3.3954e-9  # Coeficiente b [adm]
c_int_rv = -7.6364e-12  # Coeficiente c [adm]
d_int_rv = -1.1950e-15  # Coeficiente d [adm]

# ? --- Borda Interna (Runaway Greenhouse) --- [teórico: Efeito estufa descontrolado]
Seff_sun_int_rg = (
    1.0385  # Fluxo solar efetivo [Lsol/AU²]
)
a_int_rg = 1.2456e-4  # Coeficiente a [adm]
b_int_rg = 1.4612e-8  # Coeficiente b [adm]
c_int_rg = -7.6345e-12  # Coeficiente c [adm]
d_int_rg = -1.7511e-15  # Coeficiente d [adm]

# ? --- Borda Interna (Moist Greenhouse) --- [teórico/conservador: Atmosfera saturada de vapos d'água]
Seff_sun_int_mg = (
    1.0146  # Fluxo solar efetivo [Lsol/AU²]
)
a_int_mg = 8.1884e-5  # Coeficiente a [adm]
b_int_mg = 1.9394e-9  # Coeficiente b [adm]
c_int_mg = -4.3618e-12  # Coeficiente c [adm]
d_int_mg = -6.8260e-16  # Coeficiente d [adm]

# * ============================================
# * Constantes de Zona Habitável (Externa)
# * ============================================
# ? --- Borda Externa (Maximum Greenhouse) --- [teórico/conservador: saturação atmosférica de CO2 (biológico) para o aquecimento causando intenso efeito Rayleigh e esfriando mais o planeta ao invés de aquecer]
Seff_sun_ext_mg = (
    0.3507  # Fluxo solar efetivo [Lsol/AU²]
)
a_ext_mg = 5.9578e-5  # Coeficiente a [adm]
b_ext_mg = 1.6707e-9  # Coeficiente b [adm]
c_ext_mg = -3.0058e-12  # Coeficiente c [adm]
d_ext_mg = -5.1925e-16  # Coeficiente d [adm]

# ? --- Borda Externa (Early Mars) --- [empirico/otimista: Fluxo de energia recebida por Marte no momento que 'morreu']
Seff_sun_ext_em = (
    0.3207  # Fluxo solar efetivo [Lsol/AU²]
)
a_ext_em = 5.4471e-5  # Coeficiente a [adm]
b_ext_em = 1.5275e-9  # Coeficiente b [adm]
c_ext_em = -2.1709e-12  # Coeficiente c [adm]
d_ext_em = -3.8282e-16  # Coeficiente d [adm]

# ? --- Coeficientes de Zona Habitável Clássica ---
Teq_int = 303  # Temperatura de equilíbrio para a borda interna da zona habitável [K]
Teq_ext = 185  # Temperatura de equilíbrio para a borda externa da zona habitável [K]

# * ============================================
# * Constantes de Blindagem Magnetosférica
# * ============================================
Rseg_terra_at = 10.2  # Raio Padrão de Segurança da Magnetosfera (magnetosfera atual do planeta Terra) [Raios Planetários]
Rseg_terra_min = 5  # Raio Mínimo de Segurança Magnetosfera (magnetosfera paleoarqueana do planeta Terra) [Raios Planetários]
