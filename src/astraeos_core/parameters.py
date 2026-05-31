# * ============================================
# * Parâmetros de Entrada
# * ============================================
nome_ = "TRAPPIST 1a"

Mstar_ = 0.0898
Rstar_ = 0.1192
Teff_ = 2566

T_ = 2.0e6
mu_ = 0.6
rho0_ = 5e-14
B0_ = 600

S_divergencia_ = 2.5
phi0_ = 5e7
L0_ = 1
deltav0_ = 0.12851
cte_ = False

u0_step_ = 5e-4
u0_ini_ = 0.201
x_sim_ = 500

recuo_pulo_ = 484
tamanho_pulo_ = 0.1
h_rk_ = 5e-4

x_scale_ = "log"
y_scale_ = "log"

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

min_dv2_ = 0.001
max_dv2_ = 0.1
step_dv2_ = 0.001
