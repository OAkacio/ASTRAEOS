# * ============================================
# * Importações
# * ============================================
try:
    from .lib import *
except ImportError:
    from lib import *


# * ============================================
# * Geração de Gráficos de Saída e Principais
# * ============================================
def plot_perfil_output(
    x_ref,
    linestyle_ref,
    color_ref,
    nome_ref,
    sigmas_ref,
    sigmas_color_ref,
    sigmas_nome_ref,
    x_scale,
    y_scale,
    cte,
):
    # ? --- Carregamento de Dados ---
    dados = np.load(f"data/curve_{cte}.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_crit = dados["x_crit"].item()
    y_crit = dados["y_crit"].item()
    x_t = dados["x_t"].item()
    ve0 = dados["ve0"].item()
    x_sim = dados["x_sim"].item()
    nome = str(dados["nome"])

    # ? --- Renderização do Gráfico Limpo ---
    fig = gp.plot(
        title=nome,
        x_data=[x_tot],
        y_data=[list(np.array(y_tot) * ve0 / 1e5)],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label=r"$u$ (km/s)",
        x_scale=x_scale,
        y_scale=y_scale,
        linewidth=2.5,
        axis_fontsize=16,
        show_grid=True,
        grid_linewidth=0.4,
        color_style=["#61AFEF"],
        grid_color="#5C6370",
        grid_alpha=0.5,
        grid_linestyle=":",
        save_fig=True,
        file_format="png",
        filename="output",
        vlines=[x_t, *x_ref],
        v_colors=["#C678DD", *color_ref],
        v_linewidth=1.5,
        v_alpha=0.8,
        v_linestyle=["--", *linestyle_ref],
        v_labels=[rf"$r_t$ ; ${x_t}$ $r_0$", *nome_ref],
        curve_names=[
            rf"Velocity Profile ; $u_\infty = {y_tot[-1] * ve0 / 1e5:0.2f}$ km/s"
        ],
        figure_dpi=100,
        fig_width=10.0,
        fig_height=5.0,
        x_lim=[1, x_sim],
        legend_box=False,
        highlight_point=[x_crit, y_crit * ve0 / 1e5],
        highlight_color="#E06C75",
        highlight_size=50,
        highlight_marker="o",
        highlight_label=r"$P_{crit}$",
        legend_fontsize=9,
        y_lim=[None, 1500],
        block_tick=False,
        sigma_intervals=sigmas_ref,
        sigma_linestyle="",
        sigma_labels=sigmas_nome_ref,
        sigma_colors=sigmas_color_ref,
        sigma_alpha=0.15,
        theme="dark",
    )
    return fig


def plot_perfil_main(
    x_ref,
    linestyle_ref,
    color_ref,
    nome_ref,
    sigmas_ref,
    sigmas_color_ref,
    sigmas_nome_ref,
    x_scale,
    y_scale,
    tamanho_pulo,
    recuo_pulo,
    L0,
    deltav0,
    S_divergencia,
    cte,
):
    # ? --- Carregamento de Dados ---
    dados = np.load(f"data/curve_{cte}.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_crit = dados["x_crit"].item()
    y_crit = dados["y_crit"].item()
    x_t = dados["x_t"].item()
    ve0 = dados["ve0"].item()
    x_sim = dados["x_sim"].item()
    nome = str(dados["nome"])

    # ? --- Renderização do Gráfico Principal ---
    fig = gp.plot(
        x_data=[x_tot],
        y_data=[list(np.array(y_tot) * ve0 / 1e5)],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label=r"$u$ (km/s)",
        x_scale=x_scale,
        y_scale=y_scale,
        linewidth=2.5,
        axis_fontsize=20,
        show_grid=True,
        grid_linewidth=0.3,
        color_style=["#0072B2"],
        grid_color="gray",
        grid_alpha=0.3,
        grid_linestyle="-",
        save_fig=True,
        file_format="png",
        filename="clean_output",
        vlines=[x_t, *x_ref],
        v_colors=["#CC79A7", *color_ref],
        v_linewidth=1.5,
        v_alpha=0.6,
        v_linestyle=["--", *linestyle_ref],
        v_labels=[rf"$r_t$ ; ${x_t}$ $r_0$", *nome_ref],
        curve_names=[
            rf"Perfil de Velocidade ; $u_\infty = {y_tot[-1] * ve0 / 1e5:0.2f}$ km/s"
        ],
        figure_dpi=600,
        x_lim=[1, x_sim],
        legend_box=False,
        highlight_point=[x_crit, y_crit * ve0 / 1e5],
        highlight_color="#D55E00",
        highlight_size=40,
        highlight_marker="o",
        highlight_label=r"$P_{crit}$",
        legend_fontsize=12,
        y_lim=[None, 1500],
        block_tick=False,
        sigma_intervals=sigmas_ref,
        sigma_linestyle="",
        sigma_labels=sigmas_nome_ref,
        sigma_colors=sigmas_color_ref,
        sigma_alpha=0.2,
    )
    return fig


# * ============================================
# * Geração de Gráficos de Análise e Comparação
# * ============================================
def plot_curve_analis(tamanho_pulo, recuo_pulo, L0, deltav0, S_divergencia, cte):
    # ? --- Carregamento de Dados ---
    dados = np.load(f"data/curve_{cte}.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_crit = dados["x_crit"].item()
    ve0 = dados["ve0"].item()
    num_alpha_array = dados["num_alpha_array"]
    den_alpha_array = dados["den_alpha_array"]
    idx_crit_num = dados["idx_crit_num"].item()
    idx_crit_den = dados["idx_crit_den"].item()
    nome = str(dados["nome"])

    # ? --- Renderização do Gráfico de Termos da Equação ---
    fig = gp.plot(
        title=f"{nome} - Critical Topology",
        x_data=[x_tot] * 4,
        y_data=[
            den_alpha_array[:, 0],
            num_alpha_array[:, 0],
            y_tot,
            num_alpha_array[:, 0] / den_alpha_array[:, 0],
        ],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label="Equation Terms",
        x_scale="linear",
        y_scale="linear",
        linewidth=[1.5, 1.5, 2.5, 1.5],
        axis_fontsize=16,
        show_grid=True,
        grid_linewidth=0.4,
        grid_color="#5C6370",
        grid_alpha=0.5,
        grid_linestyle=":",
        color_style=["#E06C75", "#61AFEF", "#E5C07B", "#C678DD"],
        linestyle=["-", "-", "--", "-."],
        vlines=[x_crit, x_tot[idx_crit_num], x_tot[idx_crit_den]],
        v_colors=["#98C379", "#E06C75", "#61AFEF"],
        v_linewidth=[1.5, 1.5, 1.5],
        v_linestyle=["-", "--", "--"],
        v_alpha=[0.8, 0.8, 0.8],
        v_labels=[
            "Sonic Point (Analytical)",
            f"$X_{{num}}$: {x_tot[idx_crit_num]:.3f}",
            f"$X_{{den}}$: {x_tot[idx_crit_den]:.3f} (Diff: {x_tot[idx_crit_num]-x_tot[idx_crit_den]:.1e})",
        ],
        hlines=[0.0],
        h_colors=["#ABB2BF"],
        h_linewidth=[1.2],
        h_linestyle=["-"],
        h_alpha=[0.8],
        save_fig=True,
        file_format="png",
        filename="analis_output",
        curve_names=[
            r"Denominator ($D$)",
            r"Numerator ($N$)",
            rf"Velocity ($U$): $\delta v_0^2 = {deltav0:0.4f}$",
            r"Ratio ($N/D$)",
        ],
        figure_dpi=100,
        fig_width=10.0,
        fig_height=5.0,
        x_lim=[x_crit - 0.1, x_crit + 0.2],
        legend_box=False,
        legend_fontsize=10,
        theme="dark",
    )
    return fig


def plot_multicurve(
    x_ref,
    linestyle_ref,
    color_ref,
    nome_ref,
    sigmas_ref,
    sigmas_color_ref,
    sigmas_nome_ref,
    x_scale,
    y_scale,
):
    # ? --- Carregamento de Dados Múltiplos ---
    tdados = np.load("data/curve_True.npz")
    fdados = np.load("data/curve_False.npz")

    tx_tot = tdados["x_tot"]
    ty_tot = tdados["y_tot"]
    tx_crit = tdados["x_crit"].item()
    ty_crit = tdados["y_crit"].item()

    fx_tot = fdados["x_tot"]
    fy_tot = fdados["y_tot"]
    fx_crit = fdados["x_crit"].item()
    fy_crit = fdados["y_crit"].item()

    x_t = tdados["x_t"].item()
    ve0 = tdados["ve0"].item()
    x_sim = tdados["x_sim"].item()
    nome = str(tdados["nome"])

    # ? --- Renderização do Gráfico Comparativo ---
    fig = gp.plot(
        title=nome,
        x_data=[tx_tot, fx_tot],
        y_data=[list(np.array(ty_tot) * ve0 / 1e5), list(np.array(fy_tot) * ve0 / 1e5)],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label=r"$u$ (km/s)",
        x_scale=x_scale,
        y_scale=y_scale,
        linewidth=2.5,
        axis_fontsize=16,
        show_grid=True,
        grid_linewidth=0.4,
        color_style=["#61EF97", "#61AFEF"],
        grid_color="#5C6370",
        grid_alpha=0.5,
        grid_linestyle=":",
        save_fig=True,
        file_format="png",
        filename="output",
        vlines=[x_t, *x_ref],
        v_colors=["#C678DD", *color_ref],
        v_linewidth=1.5,
        v_alpha=0.8,
        v_linestyle=["--", *linestyle_ref],
        v_labels=[rf"$r_t$ ; ${x_t}$ $r_0$", *nome_ref],
        curve_names=[
            rf"Constant Damping ; $u_\infty = {ty_tot[-1] * ve0 / 1e5:0.2f}$ km/s",
            rf"Resonant Damping ; $u_\infty = {fy_tot[-1] * ve0 / 1e5:0.2f}$ km/s",
        ],
        figure_dpi=100,
        fig_width=10.0,
        fig_height=5.0,
        x_lim=[1, x_sim],
        legend_box=False,
        highlight_point=[
            [tx_crit, ty_crit * ve0 / 1e5],
            [fx_crit, fy_crit * ve0 / 1e5],
        ],
        highlight_color=["#E06C75", "#E0A06C"],
        highlight_size=50,
        highlight_marker=["o", "s"],
        highlight_label=[r"$P_{crit}^{cte}$", r"$P_{crit}^{res}$"],
        legend_fontsize=9,
        y_lim=[None, 1500],
        block_tick=False,
        sigma_intervals=sigmas_ref,
        sigma_linestyle="",
        sigma_labels=sigmas_nome_ref,
        sigma_colors=sigmas_color_ref,
        sigma_alpha=0.15,
        theme="dark",
    )
    return fig


def plot_charspeeds(
    x_ref,
    linestyle_ref,
    color_ref,
    nome_ref,
    sigmas_ref,
    sigmas_color_ref,
    sigmas_nome_ref,
    x_scale,
    y_scale,
    cte,
):
    # ? --- Carregamento de Dados ---
    dados = np.load(f"data/curve_{cte}.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_t = dados["x_t"].item()
    ve0 = dados["ve0"].item()
    x_sim = dados["x_sim"].item()
    nome = str(dados["nome"])
    u_km = np.array(y_tot) * ve0 / 1e5
    vA_km = dados["va_total"] * ve0 / 1e5
    cs_km = dados["cs"] * 1e-5
    x_crit = dados["x_crit"].item()
    y_crit = dados["y_crit"].item()

    # ? --- Renderização do Gráfico de Velocidades Características ---
    fig = gp.plot(
        title=f"{nome} - Characteristic Speeds",
        x_data=[x_tot, x_tot],
        y_data=[list(u_km), list(vA_km)],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label=r"Velocity (km/s)",
        x_scale=x_scale,
        y_scale=y_scale,
        linewidth=[2.5, 1.8],
        axis_fontsize=16,
        show_grid=True,
        grid_linewidth=0.4,
        grid_color="#5C6370",
        grid_alpha=0.5,
        grid_linestyle=":",
        save_fig=True,
        file_format="png",
        filename="charspeeds_output",
        color_style=["#0072B2", "#E06C75"],
        linestyle=[":", "-"],
        vlines=[x_t, *x_ref],
        v_colors=["#C678DD", *color_ref],
        v_linewidth=1.5,
        v_alpha=0.8,
        v_linestyle=["--", *linestyle_ref],
        hlines=[cs_km],
        h_colors=["#6C95E0"],
        h_labels=r"Speed of Sound ($c_s$)",
        h_linestyle=["-"],
        curve_names=[
            r"Wind Velocity ($u$)",
            r"Alfvén Speed ($v_A$)",
        ],
        figure_dpi=100,
        fig_width=10.0,
        fig_height=5.0,
        x_lim=[1, x_sim],
        legend_box=False,
        legend_fontsize=10,
        block_tick=False,
        sigma_intervals=sigmas_ref,
        sigma_linestyle="",
        sigma_labels=None,
        sigma_colors=sigmas_color_ref,
        sigma_alpha=0.15,
        theme="dark",
    )
    return fig


def plot_plasmaprop(
    x_ref,
    linestyle_ref,
    color_ref,
    nome_ref,
    sigmas_ref,
    sigmas_color_ref,
    sigmas_nome_ref,
    x_scale,
    y_scale,
    cte,
):
    # ? --- Carregamento de Dados ---
    dados = np.load(f"data/curve_{cte}.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_t = dados["x_t"].item()
    x_sim = dados["x_sim"].item()
    nome = str(dados["nome"])
    x_crit = dados["x_crit"].item()
    y_crit = dados["y_crit"].item()
    ve0 = dados["ve0"].item()

    rho = dados["rho_total"]
    phi = dados["phi_total"]
    deltav2 = dados["deltav2_total"]
    dmdt = dados["dmdt_total"]

    rho_norm = rho / rho[0]
    phi_norm = phi / phi[0]
    deltav2_norm = deltav2 / deltav2[0]
    dmdt_norm = dmdt / dmdt[0]
    u_norm = y_tot / y_tot[0]

    # ? --- Lógica do Limite Inferior Dinâmico ---
    idx_xt = np.argmin(np.abs(x_tot - x_t))
    rho_rt_norm = rho_norm[idx_xt]

    # ? --- Renderização do Gráfico de Propriedades do Plasma ---
    fig = gp.plot(
        title=f"{nome} - Normalized Plasma Properties",
        x_data=[x_tot, x_tot, x_tot, x_tot, x_tot],
        y_data=[
            list(u_norm),
            list(rho_norm),
            list(phi_norm),
            list(deltav2_norm),
            list(dmdt_norm),
        ],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label=r"Normalized Value ($f/f_0$)",
        x_scale=x_scale,
        y_scale=y_scale,
        linewidth=[1.5, 2.0, 2.0, 2.0, 2.0],
        axis_fontsize=16,
        show_grid=True,
        grid_linewidth=0.4,
        grid_color="#5C6370",
        grid_alpha=0.5,
        grid_linestyle=":",
        save_fig=True,
        file_format="png",
        filename="plasmaprop_output",
        color_style=["#0072B2", "#56B6C2", "#E5C07B", "#E06C75", "#98C379"],
        linestyle=[":", "-", "-", "-", "-"],
        vlines=[x_t, *x_ref],
        v_colors=["#C678DD", *color_ref],
        v_linewidth=1.5,
        v_alpha=0.8,
        v_linestyle=["--", *linestyle_ref],
        curve_names=[
            r"Wind Velocity ($u/u_0$)",
            r"Density ($\rho/\rho_0$)",
            r"Alfvén Wave Flux ($\phi_M/\phi_{M0}$)",
            r"Wave Amplitude ($\langle\delta v^2\rangle/\langle\delta v^2\rangle_0$)",
            r"Mass Loss Rate ($\dot{M}/\dot{M}_0$)",
        ],
        figure_dpi=100,
        fig_width=10.0,
        fig_height=5.0,
        x_lim=[1, x_sim],
        y_lim=[rho_rt_norm, max(list(u_norm))],
        legend_box=False,
        legend_fontsize=10,
        block_tick=False,
        sigma_intervals=sigmas_ref,
        sigma_linestyle="",
        sigma_labels=None,
        sigma_colors=sigmas_color_ref,
        sigma_alpha=0.15,
        theme="dark",
    )
    return fig


def plot_habitability_radar(
    cte,
    Dorb,
    e,
    Rstar,
    exoplanet_name,
):
    # * ============================================
    # * Importações
    # * ============================================
    import os
    import numpy as np

    # * ============================================
    # * Carregamento e Preparação de Dados
    # * ============================================
    # ? --- Extração do Arquivo .npz ---
    dados = np.load(f"data/curve_{cte}.npz")
    x_tot = dados["x_tot"]
    rho_total = dados["rho_total"]
    nome = str(dados["nome"])
    x_sim = dados["x_sim"].item()

    d_int = dados["d_int"].item()
    d_ext = dados["d_ext"].item()
    d_int_classic = dados["dc_int"].item()
    d_ext_classic = dados["dc_ext"].item()

    # ? --- Normalização e Otimização Crítica ---
    # Normalização da densidade
    rho_norm = rho_total / rho_total[0]

    # Amostragem da malha para evitar lentidão excessiva no Tkinter
    step = max(1, len(x_tot) // 1000)
    x_mesh = x_tot[::step]
    rho_mesh = rho_norm[::step]

    # ? --- Grade Polar e Matriz Z (Heatmap) ---
    theta_1d = np.linspace(0, 2 * np.pi, 200)
    Theta, R = np.meshgrid(theta_1d, x_mesh)
    Z = rho_mesh[:, np.newaxis] * np.ones((1, len(theta_1d)))

    # * ============================================
    # * Elementos Visuais do Mapa Orbital
    # * ============================================
    # ? --- Zonas Habitáveis ---
    rings_in = []
    rings_out = []
    rings_cols = []
    rings_alps = []
    rings_labs = []

    # Segurança: Adiciona a Zona Clássica se o valor for válido
    if d_int_classic > 0 and d_ext_classic > 0:
        rings_in.append(d_int_classic)
        rings_out.append(d_ext_classic)
        rings_cols.append("#6AFF00")  # Verde
        rings_alps.append(0.3)
        rings_labs.append("Classic Habitable Zone")

    # Segurança: Adiciona a Zona de Kopparapu se o valor for válido
    if d_int > 0 and d_ext > 0:
        rings_in.append(d_int)
        rings_out.append(d_ext)
        rings_cols.append("#00D8FF")  # Ciano
        rings_alps.append(0.3)
        rings_labs.append("Kopparapu Habitable Zone")

    # ? --- Órbita e Posição do Exoplaneta ---
    # Conversão da distância orbital (AU -> r0)
    rsun = 6.957e10
    au_em_cm = 1.495978707e13
    r0 = Rstar * rsun
    Dorb_r0 = Dorb * (au_em_cm / r0)

    # Equação geométrica da órbita elíptica
    theta_orb = np.linspace(0, 2 * np.pi, 150)
    r_orb = Dorb_r0 * (1 - e**2) / (1 + e * np.cos(theta_orb))

    planets_theta = list(theta_orb) + [np.pi / 4]
    planets_r = list(r_orb) + [Dorb_r0 * (1 - e**2) / (1 + e * np.cos(np.pi / 4))]

    # Estilização: Órbita pontilhada (150 pontos) + Planeta central (1 ponto)
    planets_colors = ["#ABB2BF"] * 150 + ["#FF3333"]
    planets_markers = ["."] * 150 + ["o"]
    planets_sizes = [2] * 150 + [60]
    planets_names = [None] * 150 + [exoplanet_name]

    # * ============================================
    # * Renderização e Ajustes Finais
    # * ============================================
    # ? --- Geração do Gráfico Base ---
    fig = gp.radar(
        r_data=R,
        theta_data=Theta,
        z_matrix=Z,
        rings_inner=rings_in,
        rings_outer=rings_out,
        rings_colors=rings_cols,
        rings_alphas=rings_alps,
        rings_labels=rings_labs,
        scatter_r=planets_r,
        scatter_theta=planets_theta,
        scatter_colors=planets_colors,
        scatter_markers=planets_markers,
        scatter_sizes=planets_sizes,
        scatter_labels=planets_names,
        title=None,
        r_scale="log",
        z_scale="log",
        r_lim=[0, x_sim],
        cmap="magma",
        show_grid=True,
        background_color="#1E1E1E",
        grid_color="#5C6370",
        grid_alpha=0.3,
        grid_linestyle=":",
        theme="dark",
        z_label=r"Normalized Plasma Density ($\rho/\rho_0$)",
        fig_width=10.0,
        fig_height=6.0,
        figure_dpi=100,
        save_fig=False,
        show_plot=False,
    )

    # ? --- Intervenções Estéticas Customizadas ---
    ax = fig.axes[0]

    # Remove as marcações de ângulos das bordas (90º, 180º) para um visual limpo
    ax.set_xticks([])

    # Recolhe e reposiciona a legenda à esquerda para evitar sobreposição
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if None in by_label:
        del by_label[None]

    ax.legend(
        by_label.values(),
        by_label.keys(),
        loc="upper left",
        bbox_to_anchor=(-0.25, 1.05),
        frameon=False,
        fontsize=11,
        labelcolor="#ABB2BF",
    )

    # ? --- Salvamento Manual da Figura ---
    filepath = "figures/habitability_radar.png"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, dpi=100, bbox_inches="tight", facecolor="#1E1E1E")

    return fig
