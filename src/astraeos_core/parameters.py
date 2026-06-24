#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Parâmetros de Entrada da Estrela                                         │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Identificação                                    │
# ? ╰────────────────────────────────────────────────────╯
#
nome_ = "TRAPPIST 1a"
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Parâmetros Estelares                             │
# ? ╰────────────────────────────────────────────────────╯
#
Mstar_ = 0.0898  # Massa da estrela [Massas Solares]
Rstar_ = 0.1192  # Raio da estrela [Raios Solares]
Teff_ = 2566  # Temperatura efetiva [K]
Lstar_ = 5.2e-4  # Luminosidade da estrela [Luminosidades Solares]
T_ = 2.0e6  # Temperatura coronal [K]
mu_ = 0.6  # Peso molecular médio [adm]
rho0_ = 5e-14  # Densidade na base da coroa [g/cm³]
B0_ = 600  # Campo magnético inicial [G]
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Parâmetros de Onda                               │
# ? ╰────────────────────────────────────────────────────╯
#
S_divergencia_ = 2.5
F_ = 10
phi0_ = 5e7
L0_ = 1
deltav0_ = 0.12851
cte_ = False
parker_ = False
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Integração Numérica                              │
# ? ╰────────────────────────────────────────────────────╯
#
u0_step_ = 5e-4
u0_ini_ = 0.201
x_sim_ = 500
recuo_pulo_ = 484
tamanho_pulo_ = 0.1
h_rk_ = 5e-4
autotol_ = 1e-6
checkautotol_ = False
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Personalização                                   │
# ? ╰────────────────────────────────────────────────────╯
#
x_scale_ = "log"
y_scale_ = "log"
x_un_ = "r/r0"
y_un_ = "u/ve0"
x_ref_ = 37.0, 49.0, 63.0, 77.0
linestyle_ref_ = ":", ":", ":", ":"
color_ref_ = "#922424", "#926224", "#927824", "#439224"
nome_ref_ = (
    rf"1d ; ${round(x_ref_[0],1)}$ $r_0$",
    rf"1e ; ${round(x_ref_[1],1)}$ $r_0$",
    rf"1f ; ${round(x_ref_[2],1)}$ $r_0$",
    rf"1g ; ${round(x_ref_[3],1)}$ $r_0$",
)
sigmas_ref_ = [[39.7, 84.7]]
sigmas_color_ref_ = ["#8FFF81"]
sigmas_nome_ref_ = ["ZH"]
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Parâmetros de Script                             │
# ? ╰────────────────────────────────────────────────────╯
#
min_dv2_ = 0.001
max_dv2_ = 0.1
step_dv2_ = 0.001
#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Parâmetros de Entrada de Zona Habitável                                  │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Propriedades do Planeta                          │
# ? ╰────────────────────────────────────────────────────╯
#
exoplanet_name_ = "TRAPPIST-1f"
Dorb_ = 0.03849  # Distância orbital do planeta [AU]
e_ = 0.0056  # Excentricidade da órbita [adm]
Ab_ = 0.3  # Albedo planetário [adm]
#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Parâmetros de Entrada de Magnetosfera                                    │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
Rplan_ = 1.045  # Raio do planeta [Raios Terrestres]
Mmag_ = 8e22  # Momento magnético planetário [Am²]
f0_ = 1.16  # Fator de forma da magnetosfera [adm]
k_cme_ = 4.0  # Fator multiplicativo para Ejeção de Massa Coronal [adm]
hion_ = 1000  # Altura máxima da ionosfera [km]
