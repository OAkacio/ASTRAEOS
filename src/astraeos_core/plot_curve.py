try:
    from .lib import *
except:
    from lib import *


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
):
    # 1. Carrega os dados salvos da última simulação
    dados = np.load("data/curve.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_crit = dados["x_crit"]
    y_crit = dados["y_crit"]
    x_t = dados["x_t"]
    ve0 = dados["ve0"]
    x_sim = dados["x_sim"]
    nome = str(dados["nome"])
    num_alpha_array = dados["num_alpha_array"]
    den_alpha_array = dados["den_alpha_array"]
    idx_crit_num = dados["idx_crit_num"].item()
    idx_crit_den = dados["idx_crit_den"].item()

    # 2. Chama APENAS a geração do gráfico de Output com os novos parâmetros visuais
    gp.plot(
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
        color_style=["#61AFEF"],  # Azul ciano vibrante para a curva principal
        grid_color="#5C6370",  # Cinza sutil para a grade
        grid_alpha=0.5,
        grid_linestyle=":",
        save_fig=True,
        file_format="png",
        filename="output",
        vlines=[x_t, *x_ref],
        v_colors=["#C678DD", *color_ref],  # Magenta para a linha de transição
        v_linewidth=1.5,
        v_alpha=0.8,
        v_linestyle=["--", *linestyle_ref],
        v_labels=[rf"$r_t$ ; ${x_t}$ $r_0$", *nome_ref],
        curve_names=[
            rf"Velocity Profile ; $u_\infty = {y_tot[-1] * ve0 / 1e5:0.2f}$ km/s"
        ],
        figure_dpi=600,  # Desempenho alto para UI em tempo real
        fig_width=10.0,  # Gráfico widescreen (Esticado)
        fig_height=5.0,  # Altura balanceada
        x_lim=[1, x_sim],
        legend_box=False,
        highlight_point=[x_crit, y_crit * ve0 / 1e5],
        highlight_color="#E06C75",  # Ponto crítico em vermelho vibrante
        highlight_size=50,
        highlight_marker="o",
        highlight_label=r"$P_{crit}$",
        legend_fontsize=8,
        y_lim=[None, 1500],
        block_tick=False,
        sigma_intervals=sigmas_ref,
        sigma_linestyle="",
        sigma_labels=sigmas_nome_ref,
        sigma_colors=sigmas_color_ref,
        sigma_alpha=0.15,
        theme="dark",  # Ativa o modo escuro que criamos!
    )


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
    # 1. Carrega os dados salvos da última simulação
    dados = np.load("data/curve.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_crit = dados["x_crit"]
    y_crit = dados["y_crit"]
    x_t = dados["x_t"]
    ve0 = dados["ve0"]
    x_sim = dados["x_sim"]
    nome = str(dados["nome"])
    num_alpha_array = dados["num_alpha_array"]
    den_alpha_array = dados["den_alpha_array"]
    idx_crit_num = dados["idx_crit_num"].item()
    idx_crit_den = dados["idx_crit_den"].item()

    # 2. Chama APENAS a geração do gráfico de Output com os novos parâmetros visuais
    gp.plot(
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
        filename=f"{cte}_perfil_t{round(tamanho_pulo,3)}_rec{round(recuo_pulo,3)}_s{round(S_divergencia)}_L0{round(L0, 3)}_deltav0{round(deltav0,7)}",
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


def plot_curve_analis(tamanho_pulo, recuo_pulo, L0, deltav0, S_divergencia):
    # 1. Carrega os dados salvos da última simulação
    dados = np.load("data/curve.npz")
    x_tot = dados["x_tot"]
    y_tot = dados["y_tot"]
    x_crit = dados["x_crit"]
    y_crit = dados["y_crit"]
    x_t = dados["x_t"]
    ve0 = dados["ve0"]
    x_sim = dados["x_sim"]
    nome = str(dados["nome"])
    num_alpha_array = dados["num_alpha_array"]
    den_alpha_array = dados["den_alpha_array"]
    idx_crit_num = dados["idx_crit_num"].item()
    idx_crit_den = dados["idx_crit_den"].item()

    gp.plot(
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
        linewidth=[1.5, 1.5, 2.0, 1.2],
        axis_fontsize=12,
        show_grid=True,
        grid_linewidth=0.5,
        grid_color="#B0B0B0",
        grid_alpha=0.5,
        grid_linestyle=":",
        color_style=["#E06C75", "#61AFEF", "#282C34", "#ABB2BF"],
        linestyle=["-", "-", "--", "-."],
        vlines=[x_crit, x_tot[idx_crit_num], x_tot[idx_crit_den]],
        v_colors=["#98C379", "#E06C75", "#61AFEF"],
        v_linewidth=[1.5, 1.0, 1.0],
        v_linestyle=["-", "--", "--"],
        v_alpha=[0.8, 0.7, 0.7],
        v_labels=[
            "Sonic Point (Analytical)",
            f"$X_{{num}}$: {x_tot[idx_crit_num]:.3f}",
            f"$X_{{den}}$: {x_tot[idx_crit_den]:.3f} (Diff: {x_tot[idx_crit_num]-x_tot[idx_crit_den]:.1e})",
        ],
        hlines=[0.0],
        h_colors=["black"],
        h_linewidth=[1.2],
        h_linestyle=["-"],
        h_alpha=[0.8],
        save_fig=True,
        file_format="png",
        filename=f"perfil_t{round(tamanho_pulo)}_rec{round(recuo_pulo,3)}_s{round(S_divergencia)}_L0{round(L0)}_deltav0{round(deltav0,6)}_ANALISE",
        curve_names=[
            r"Denominator ($D$)",
            r"Numerator ($N$)",
            rf"Velocity ($U$): $\delta v_0^2 = {deltav0:0.4f}$",
            r"Ratio ($N/D$)",
        ],
        figure_dpi=600,
        x_lim=[x_crit - 0.1, x_crit + 0.2],
        legend_box=False,
        legend_fontsize=10,
    )
