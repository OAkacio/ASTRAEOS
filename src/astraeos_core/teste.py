import matplotlib.pyplot as plt
import numpy as np

# Configuração do espaço cartesianizado 2D
N = 150
x = np.linspace(-4, 6, N)
y = np.linspace(-5, 5, N)
X, Y = np.meshgrid(x, y)

# Parâmetros físicos simulados
RM = 1.5  # Raio da magnetopausa (distância subsolar)
R_planeta = 0.5  # Tamanho visual do exoplaneta no gráfico

# --- CAMPO VETORIAL DO VENTO ESTELAR (U, V) ---
# Vento vem da esquerda puro (U = 2.0, V = 0.0)
U = np.ones_like(X) * 2.0
V = np.zeros_like(Y)

# Geometria analítica do desvio: Criamos uma repulsão baseada na parábola
# À medida que se aproxima do nariz (-RM, 0), o fluxo ganha velocidade vertical (V)
for i in range(N):
    for j in range(N):
        px, py = X[i, j], Y[i, j]
        # Distância aproximada ao "nariz" ou escudo
        if px < 0:  # Região antes do planeta onde ocorre o choque
            dist_escudo = np.sqrt((px - (-RM))**2 + py**2)
            if dist_escudo < 2.0:
                # Modula a direção do vento baseado no ângulo da posição
                v_defection = py / (dist_escudo + 0.2)
                V[i, j] += v_defection * 1.5
                U[i, j] *= (dist_escudo / 2.0)  # Desacelera ao aproximar

# Força o fluxo interno a ser zero (área protegida dentro da magnetosfera)
# Equação da magnetopausa voltada para o vento (esquerda): x = -RM + (y^2 / 4RM)
dentro_magnetosfera = X > (-RM + (Y**2 / (4 * RM)))
U[dentro_magnetosfera] = 0.1  # Fluxo calmo interno
V[dentro_magnetosfera] = 0.0

# --- DESIGN DO GRÁFICO ---
fig, ax = plt.subplots(figsize=(10, 7), facecolor='#0B0F19')
ax.set_facecolor('#0B0F19')

# 1. Plotando as Linhas de Fluxo com gradiente de velocidade (Streamplot)
velocidade = np.sqrt(U**2 + V**2)
fluxo = ax.streamplot(X, Y, U, V, color=velocidade, cmap='cool', linewidth=1.2, density=1.5, arrowstyle='->', arrowsize=1.0)

# 2. Desenhando a Magnetopausa (Parábola limite)
y_parabola = np.linspace(-5, 5, 200)
x_parabola = -RM + (y_parabola**2 / (4 * RM))
ax.plot(x_parabola, y_parabola, color='#00FFCC', linestyle='--', linewidth=2, 
        label='Magnetopausa (Escudo de Choque)', alpha=0.8)

# Preenchendo a zona segura (Refúgio Seguro)
ax.fill_betweenx(y_parabola, x_parabola, 6, color='#00FFCC', alpha=0.07, label='Zona Protegida')

# 3. O Planeta na origem (0,0)
planeta = plt.Circle((0, 0), R_planeta, edgecolor='black', zorder=5, label='Exoplaneta')
ax.add_patch(planeta)

# Brilho atmosférico simples (Opcional para estética de revista)
atmosfera = plt.Circle((0, 0), R_planeta*1.3, color='#4A90E2', alpha=0.2, zorder=4)
ax.add_patch(atmosfera)

# --- DETALHES E CUSTOMIZAÇÃO ---
ax.set_xlim(-4, 6)
ax.set_ylim(-5, 5)
ax.set_title("Interação Dinâmica: Vento Estelar vs. Magnetosfera", color='white', fontsize=14, pad=15)
ax.set_xlabel("Distância Relativa ($X$)", color='white')
ax.set_ylabel("Distância Relativa ($Y$)", color='white')

# Customização dos eixos para o tema escuro
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('#2C3E50')
ax.spines['left'].set_color('#2C3E50')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(color='#2C3E50', linestyle=':', alpha=0.5)

# Barra de cor para representar a velocidade do vento estelar
cbar = fig.colorbar(fluxo.lines, ax=ax, orientation='horizontal', pad=0.1, shrink=0.7)
cbar.set_label('Velocidade Relativa do Vento Estelar', color='white')
cbar.ax.tick_params(labelsize=9, colors='white')

ax.legend(loc='upper right', facecolor='#111827', edgecolor='#2C3E50', labelcolor='white')
plt.tight_layout()
plt.show()
