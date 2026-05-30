#
# * ============================================
# * Importações
# * ============================================
try:
    from .lib import *
    from .parameters import *
    from .utils import *
    from .core import *
except:
    from lib import *
    from parameters import *
    from utils import *
    from core import *


# * ============================================
# * Início
# * ============================================
def main(
    nome,
    Mstar,
    Rstar,
    Teff,
    T,
    mu,
    rho0,
    B0,
    phi0,
    u0_step,
    u0_ini,
    h_rk,
    deltav0,
    S_divergencia,
    recuo_pulo,
    tamanho_pulo,
    cte,
    L0,
    x_sim,
):
    sy.header("JPOStellarWind", Estrela=nome)

    # ? --- Apresentação dos Parâmetros ---
    sy.status("Apresentando parâmetros de entrada...")
    ve0, cs, vA0, vT, x_t = calc_param(deltav0, S_divergencia)
    sy.param(
        ("Nome", nome, ""),
        ("Massa", Mstar, "Msun"),
        ("Raio", Rstar, "Rsun"),
        ("Teff", Teff, "K"),
        ("ve0", ve0 / 1e5, "km/s"),
        ("vA0", vA0, "ve0"),
        ("vA0", vA0 * ve0 / 1e5, "km/s"),
        ("vT", vT, "ve0"),
        ("deltav0", deltav0, "ve0²"),
        ("B0", B0, "G"),
        ("rho0", rho0, "g/cm³"),
        ("S", S_divergencia, ""),
        ("phi0", phi0, "erg/cm²/s"),
        ("T", T, "K"),
        ("L0", L0, "r0"),
        ("x_t", x_t, "r0"),
        ("cs", cs, "cm/s"),
    )

    # ? --- Busca por Velocidade Inicial ---
    sy.status("Iniciando busca pela velocidade inicial...")
    u0, x_crit, y_crit, r_crit, x_append, y_append, vetor = jl.busca_u0(
        vT,
        [B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S_divergencia, 0.0, phi0],
        u0_step,
        u0_ini,
        cte,
    )
    sy.param(
        ("Velocidade Inicial", u0 * ve0 / 1e5, "km/s"),
        ("Velocidade Inicial Adimensional", u0, "ve0"),
        ("Distância do Ponto Crítico", x_crit, "r0"),
        ("Velocidade no Ponto Crítico", y_crit, "ve0"),
        ("Valor da Função no Ponto Crítico", r_crit, "adm"),
    )

    # ? --- Integração de Curva ---
    sy.status("Iniciando integração do perfil de velocidade...")

    x0n, y0, x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list = (
        jl.integra_perfil(
            u0,
            x_crit,
            y_crit,
            vetor,
            x_append,
            y_append,
            x_t,
            recuo_pulo,
            tamanho_pulo,
            h_rk,
            cte,
            x_sim,
        )
    )

    x_tot, y_tot, num_alpha_array, den_alpha_array, idx_crit_num, idx_crit_den = (
        zerosND(x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list)
    )

    sy.param(
        ("Velocidade Terminal", y_tot[-1] * ve0 / 1e5, "km/s"),
        ("Velocidade Terminal", y_tot[-1], "ve0"),
        ("Distância do Ponto de Transição", x_t, "r0"),
    )

    # ? --- Geração de Gráfico Principal ---
    gp.plot(
        x_data=[x_tot],
        y_data=[list(np.array(y_tot) * ve0 / 1e5)],
        show_plot=False,
        x_label=r"$r/r_{0}$",
        y_label=r"$u$ (km/s)",
        x_scale="log",
        y_scale="log",
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
    # ? --- Geração de Gráfico de Análise ---
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
        y_label="Termos da Equação",
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
            "Ponto Sônico (Analítico)",
            f"$X_{{num}}$: {x_tot[idx_crit_num]:.3f}",
            f"$X_{{den}}$: {x_tot[idx_crit_den]:.3f} (Dif: {x_tot[idx_crit_num]-x_tot[idx_crit_den]:.1e})",
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
            r"Denominador ($D$)",
            r"Numerador ($N$)",
            rf"Velocidade ($U$): $\delta v_0^2 = {deltav0:0.4f}$",
            r"Razão ($N/D$)",
        ],
        figure_dpi=600,
        x_lim=[x_crit - 0.1, x_crit + 0.2],
        legend_box=False,
        legend_fontsize=10,
    )
    sy.fim()

    return x_tot, y_tot, x_crit, y_crit, x_t, ve0


if __name__ == "__main__":
    main(
        nome=nome,
        Mstar=Mstar,
        Rstar=Rstar,
        Teff=Teff,
        T=T,
        mu=mu,
        rho0=rho0,
        B0=B0,
        phi0=phi0,
        u0_step=u0_step,
        u0_ini=u0_ini,
        h_rk=h_rk,
        deltav0=deltav0,
        S_divergencia=S_divergencia,
        recuo_pulo=recuo_pulo,
        tamanho_pulo=tamanho_pulo,
        cte=False,
        L0=L0,
        x_sim=x_sim,
    )
