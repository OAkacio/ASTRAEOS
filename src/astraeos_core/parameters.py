#
# * ============================================
# * Parâmetros de Entrada
# * ============================================
# ? --- Identificação ---
nome = "TRAPPIST 1a"

# ? --- Propriedades Estelares ---
Mstar = 0.0898  # Massa da estrela [Massas Solares]
Rstar = 0.1192  # Raio da estrela [Raios Solares].
Teff = 2566  # Temperatura efetiva [K]

# ? --- Parâmetros Físicos da Coroa ---
T = 2.0e6  # Temperatura coronal [K]
mu = 0.6  # Peso molecular médio [adm]
rho0 = 5e-14  # Densidade na base da coroa [g/cm³]
B0 = 600  # Campo magnético inicial [G]

# ? --- Parâmetros de Onda e Geometria ---
S_divergencia = 2.5  # Fator de expansão [adm] #? Livre
phi0 = 5e7  # Fluxo inicial de ondas Alfvén [erg /cm²/s] #? Livre
L0 = 1  # Comprimento de amortecimento [unidades de r0] #? Livre
deltav0 = 0.12851  # Amplitude de onda inicial [ve0²] #? Livre

# ? --- Ajustes de Integração | Alteração pode Ocasionar em Instabilidade ---
u0_step = 5e-4  # Passo de busca pela velocidade inicial [ve0]
u0_ini = 0.201  # limite inferior da busca pela velocidade inicial [ve0]
x_sim = 500  # Distância de simulação [Rstar]

recuo_pulo = 484  # Número de passos recuados para o pulo [1e-5 Rstar]
tamanho_pulo = 0.1  # Tamanho do pulo [Rstar]
h_rk = 5e-4  # Passo de integração [Rstar]

# ? --- Referências e Personalização ---
x_ref = 37.0, 49.0, 63.0, 77.0  # Distância de referência [Rstar]
linestyle_ref = ":", ":", ":", ":"  # Estilo da linha de referência
color_ref = "#922424", "#926224", "#927824", "#439224"  # Cor da linha de referência
nome_ref = (
    rf"1d ; ${round(x_ref[0],1)}$ $r_0$",
    rf"1e ; ${round(x_ref[1],1)}$ $r_0$",
    rf"1f ; ${round(x_ref[2],1)}$ $r_0$",
    rf"1g ; ${round(x_ref[3],1)}$ $r_0$",
)  # Nome do ponto de referência
sigmas_ref = [[39.7, 84.7]]
sigmas_color_ref = ["#8FFF81"]
sigmas_nome_ref = ["ZH"]
