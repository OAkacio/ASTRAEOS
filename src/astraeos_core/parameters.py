# * ============================================
# * Parâmetros de Entrada | Vento Estelar
# * ============================================
# ? --- Identificação ---


nome_ = "TRAPPIST 1a"


# ? --- Propriedades Estelares ---
Mstar_ = 0.0898  # Massa da estrela [Massas Solares]
Rstar_ = 0.1192  # Raio da estrela [Raios Solares].
Teff_ = 2566  # Temperatura efetiva [K]
Lstar_ = 5.2e-4  # Luminosidade da estrela [Luminosidades Solares]


# ? --- Parâmetros Físicos da Coroa ---
T_ = 2.0e6  # Temperatura coronal [K]
mu_ = 0.6  # Peso molecular médio [adm]
rho0_ = 5e-14  # Densidade na base da coroa [g/cm³]
B0_ = 600  # Campo magnético inicial [G]


# ? --- Parâmetros de Onda e Geometria ---
S_divergencia_ = 2.5  # Fator de expansão [adm] #? Livre
phi0_ = 5e7  # Fluxo inicial de ondas Alfvén [erg /cm²/s] #? Livre
L0_ = 1  # Comprimento de amortecimento [unidades de r0] #? Livre
deltav0_ = 0.12851  # Amplitude de onda inicial [ve0²] #? Livre
cte_ = False  # Usar ou não amortecimento constante


# ? --- Ajustes de Integração | Alteração pode Ocasionar em Instabilidade ---
u0_step_ = 5e-4  # Passo de busca pela velocidade inicial [ve0]
u0_ini_ = 0.201  # limite inferior da busca pela velocidade inicial [ve0]
x_sim_ = 500  # Distância de simulação [Rstar]


recuo_pulo_ = 484  # Número de passos recuados para o pulo [1e-5 Rstar]
tamanho_pulo_ = 0.1  # Tamanho do pulo [Rstar]
h_rk_ = 5e-4  # Passo de integração [Rstar]


# ? --- Referências e Personalização ---
x_scale_ = "log"
y_scale_ = "log"


x_ref_ = 37.0, 49.0, 63.0, 77.0  # Distância de referência [Rstar]
linestyle_ref_ = ":", ":", ":", ":"  # Estilo da linha de referência
color_ref_ = "#922424", "#926224", "#927824", "#439224"  # Cor da linha de referência
nome_ref_ = (
    rf"1d ; ${round(x_ref_[0],1)}$ $r_0$",
    rf"1e ; ${round(x_ref_[1],1)}$ $r_0$",
    rf"1f ; ${round(x_ref_[2],1)}$ $r_0$",
    rf"1g ; ${round(x_ref_[3],1)}$ $r_0$",
)  # Nome do ponto de referência
sigmas_ref_ = [[39.7, 84.7]]
sigmas_color_ref_ = ["#8FFF81"]
sigmas_nome_ref_ = ["ZH"]


# ? --- MultiCurve Script ---
min_dv2_ = 0.001  # Valor mínimo de busca automática de DV2 [ve0]
max_dv2_ = 0.1  # Valor máximo de busca automática de DV2 [ve0]
step_dv2_ = 0.001  # Passo de busca automática de DV2 [ve0]

# * ============================================
# * Parâmetros de Entrada | Zona Habitável
# * ============================================
exoplanet_name_ = "TRAPPIST-1f"  # Nome do exoplaneta para análise de zona habitável
e_ = 0.0056  # Excentricidade da órbita (e = 0 : Órbita circular ; 0 < e < 1 : Órbita elíptica) [adm]
Ab_ = 0.3  # Albedo planetário [adm]

# * ============================================
# * Parâmetros de Entrada | Blindagem Magnetosférica
# * ============================================
Mmag_ = 8e22  # Momento Magnético do Planeta [Am²]
f0_ = 1.16  # Fator de forma da magnetosfera [adm]