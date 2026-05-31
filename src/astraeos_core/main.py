# * ============================================
# * Importações
# * ============================================
try:
    from .lib import *
    from .parameters import *
    from .utils import *
    from .core import *
    from .plot_curve import *
except:
    from lib import *
    from parameters import *
    from utils import *
    from core import *
    from plot_curve import *


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
    sy.header("ASTRAEOS", Version="v0.1.0", Author="Victor M. Acacio", flush=True)

    # ? --- Apresentação dos Parâmetros ---
    sy.status("Displaying input parameters...", flush=True)
    ve0, cs, vA0, vT, x_t, r0, M = calc_param(
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
        x_ref,
        linestyle_ref,
        color_ref,
        nome_ref,
        sigmas_ref,
        sigmas_color_ref,
        sigmas_nome_ref,
    )
    sy.param(
        ("Name", nome, ""),
        ("Mass", Mstar, "Msun"),
        ("Radius", Rstar, "Rsun"),
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
        flush=True,
    )

    # ? --- Busca por Velocidade Inicial ---
    sy.status("Initiating search for initial velocity...", flush=True)
    time.sleep(1)
    u0, x_crit, y_crit, r_crit, x_append, y_append, vetor = jl.busca_u0(
        vT,
        [B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S_divergencia, 0.0, phi0],
        u0_step,
        u0_ini,
        cte,
    )
    sy.param(
        ("Initial Velocity", u0 * ve0 / 1e5, "km/s"),
        ("Dimensionless Initial Velocity", u0, "ve0"),
        ("Critical Point Distance", x_crit, "r0"),
        ("Velocity at Critical Point", y_crit, "ve0"),
        ("Function Value at Critical Point", r_crit, "adm"),
        flush=True,
    )

    # ? --- Integração de Curva ---
    sy.status("Initiating velocity profile integration...", flush=True)
    time.sleep(1)
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
    os.makedirs("data", exist_ok=True)
    np.savez(
        "data/curve.npz",
        x_tot=x_tot,
        y_tot=y_tot,
        x_crit=x_crit,
        y_crit=y_crit,
        x_t=x_t,
        ve0=ve0,
        x_sim=x_sim,
        nome=nome,
        num_alpha_array=num_alpha_array,
        den_alpha_array=den_alpha_array,
        idx_crit_num=idx_crit_num,
        idx_crit_den=idx_crit_den,
    )

    sy.param(
        ("Terminal Velocity", y_tot[-1] * ve0 / 1e5, "km/s"),
        ("Terminal Velocity", y_tot[-1], "ve0"),
        ("Transition Point Distance", x_t, "r0"),
        flush=True,
    )

    # ? --- Geração de Gráfico Principal ---
    plot_perfil_main(
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
    )
    # ? --- Geração de Gráfico de Output ---
    plot_perfil_output(
        x_ref,
        linestyle_ref,
        color_ref,
        nome_ref,
        sigmas_ref,
        sigmas_color_ref,
        sigmas_nome_ref,
        x_scale,
        y_scale,
    )
    # ? --- Geração de Gráfico de Análise ---
    plot_curve_analis(
        tamanho_pulo,
        recuo_pulo,
        L0,
        deltav0,
        S_divergencia,
    )

    sy.fim("EXECUTION COMPLETED", flush=True)

    return (
        x_tot,
        y_tot,
        x_crit,
        y_crit,
        x_t,
        ve0,
        x_sim,
        nome,
        num_alpha_array,
        den_alpha_array,
        idx_crit_num,
        idx_crit_den,
    )


if __name__ == "__main__":
    main(
        nome=nome_,
        Mstar=Mstar_,
        Rstar=Rstar_,
        Teff=Teff_,
        T=T_,
        mu=mu_,
        rho0=rho0_,
        B0=B0_,
        phi0=phi0_,
        u0_step=u0_step_,
        u0_ini=u0_ini_,
        h_rk=h_rk_,
        deltav0=deltav0_,
        S_divergencia=S_divergencia_,
        recuo_pulo=recuo_pulo_,
        tamanho_pulo=tamanho_pulo_,
        cte=False,
        L0=L0_,
        x_sim=x_sim_,
        x_ref=x_ref_,
        linestyle_ref=linestyle_ref_,
        color_ref=color_ref_,
        nome_ref=nome_ref_,
        sigmas_ref=sigmas_ref_,
        sigmas_color_ref=sigmas_color_ref_,
        sigmas_nome_ref=sigmas_nome_ref_,
        x_scale=x_scale_,
        y_scale=y_scale_,
    )
