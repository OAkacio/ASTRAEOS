# * ============================================
# * Constantes Físicas
# * ============================================
mp = 1.6726e-24  # Massa do próton [g]
kb = 1.3807e-16  # Constante de Boltzmann [erg/K]
G = 6.6743e-8  # Constante gravitacional [cm³g⁻¹s⁻²]
rsun = 6.96e10  # Raio Solar [cm]
Msun = 1.989e33  # Massa Solar [g]

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
Rsun_to_AU = 0.00465047  # Fator de conversão de raios solares para unidades astronômicas [AU/Rsun]
