# * ============================================
# * Importações
# * ============================================
try:
    from .lib import *
    from .parameters import *
    from .utils import *
    from .core import *
    from .plot_curve import *
    from .habitability import *
except ImportError:
    from lib import *
    from parameters import *
    from utils import *
    from core import *
    from plot_curve import *
    from habitability import *


# * ============================================
# * Rotina Principal de Simulação
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
    habitabilidade,
    exoplanet_name,
    Lstar,
    e,
    Ab,
    f0,
    Mmag,
    Dorb,
    Rplan,
    show_progress=True,
    **kwargs,
):
    # ? --- Inicialização e Parâmetros ---
    if show_progress:
        print("___PROGRESS___|0.05", flush=True)

    sy.header("ASTRAEOS", Version="v0.1.0", Author="Victor M. Acacio", flush=True)
    sy.status("Loading input parameters...", flush=True)

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
        # --- Stellar & Coronal Properties ---
        ("Target Name", nome, ""),
        ("Stellar Mass", Mstar, "Msun"),
        ("Stellar Radius", Rstar, "Rsun"),
        ("Effective Temperature", Teff, "K"),
        ("Stellar Luminosity", Lstar, "Lsun"),
        ("Coronal Temperature", T, "K"),
        ("Coronal Base Density", rho0, "g/cm³"),
        ("Mean Molecular Weight", mu, "adm"),
        ("Surface Magnetic Field", B0, "G"),
        # --- Wind & Wave Parameters ---
        ("Expansion Factor", S_divergencia, "adm"),
        ("Initial Wave Amplitude", deltav0, "ve0²"),
        ("Initial Alfvén Flux", phi0, "erg/cm²/s"),
        ("Damping Length", L0, "r0"),
        ("Constant Damping Mode", cte, "bool"),
        # --- Calculated Velocities & Scales ---
        ("Escape Velocity (ve0)", ve0 / 1e5, "km/s"),
        ("Normalized Alfvén Velocity", vA0, "ve0"),
        ("Alfvén Velocity (vA0)", vA0 * ve0 / 1e5, "km/s"),
        ("Thermal Velocity (vT)", vT, "ve0"),
        ("Sound Speed (cs)", cs, "cm/s"),
        ("Alfvén Radius (x_t)", x_t, "r0"),
        flush=True,
    )

    if show_progress:
        print("___PROGRESS___|0.2", flush=True)

    # ? --- Callbacks de Progresso ---
    def cb_u0(pct):
        print(f"___U0_PROGRESS___|{pct}", flush=True)

    def cb_int(pct):
        print(f"___INT_PROGRESS___|{pct}", flush=True)

    # ? --- Busca por Velocidade Inicial ---
    sy.status("Searching for base velocity and critical point...", flush=True)
    time.sleep(1)

    u0, x_crit, y_crit, r_crit, x_append, y_append, vetor = jl.busca_u0(
        vT,
        [B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S_divergencia, 0.0, phi0],
        u0_step,
        u0_ini,
        cte,
        cb_u0,
    )

    sy.param(
        ("Base Velocity", u0 * ve0 / 1e5, "km/s"),
        ("Normalized Base Velocity", u0, "ve0"),
        ("Critical Point Distance", x_crit, "r0"),
        ("Critical Velocity", y_crit, "ve0"),
        ("Critical Point Residual", r_crit, "adm"),
        flush=True,
    )

    # ? --- Integração do Perfil de Velocidade ---
    sy.status("Integrating wind velocity profile...", flush=True)
    time.sleep(1)

    (
        x0n,
        y0,
        x_int,
        y_int,
        x_ext,
        y_ext,
        num_alpha_list,
        den_alpha_list,
        vA_total,
        rho_total,
        phi_total,
        deltav2_total,
        dmdt_total,
    ) = jl.integra_perfil(
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
        cb_int,
    )

    x_tot, y_tot, num_alpha_array, den_alpha_array, idx_crit_num, idx_crit_den = (
        zerosND(x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list)
    )

    sy.status("Extracting final results...", flush=True)
    sy.param(
        ("Terminal Velocity", y_tot[-1] * ve0 / 1e5, "km/s"),
        ("Normalized Terminal Velocity", y_tot[-1], "ve0"),
        ("Alfvén Radius", x_t, "r0"),
        flush=True,
    )

    if habitabilidade:
        d_int, d_ext, dc_int, dc_ext, P_din, Rmag = main_hab(
            Lstar,
            Teff,
            e,
            Rstar,
            Ab,
            Dorb,
            Mmag,
            f0,
            x_tot,
            y_tot,
            rho_total,
            ve0,
            Rplan,
            r0,
            cte,
            exoplanet_name,
        )

    # ? --- Processamento e Salvamento de Dados ---
    os.makedirs("data", exist_ok=True)
    np.savez(
        f"data/curve_{cte}.npz",
        # --- Input Parameters ---
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
        cte=cte,
        L0=L0,
        x_sim=x_sim,
        x_ref=x_ref,
        linestyle_ref=linestyle_ref,
        color_ref=color_ref,
        nome_ref=nome_ref,
        sigmas_ref=sigmas_ref,
        sigmas_color_ref=sigmas_color_ref,
        sigmas_nome_ref=sigmas_nome_ref,
        x_scale=x_scale,
        y_scale=y_scale,
        habitabilidade=habitabilidade,
        exoplanet_name=exoplanet_name,
        Lstar=Lstar,
        e=e,
        Ab=Ab,
        f0=f0,
        Mmag=Mmag,
        Dorb=Dorb,
        Rplan=Rplan,
        # --- Output Parameters ---
        x_tot=x_tot,
        y_tot=y_tot,
        x_crit=x_crit,
        y_crit=y_crit,
        x_t=x_t,
        ve0=ve0,
        x_sim=x_sim,
        u0=u0,
        num_alpha_array=num_alpha_array,
        den_alpha_array=den_alpha_array,
        idx_crit_num=idx_crit_num,
        idx_crit_den=idx_crit_den,
        va_total=vA_total,
        cs=cs,
        rho_total=rho_total,
        phi_total=phi_total,
        deltav2_total=deltav2_total,
        dmdt_total=dmdt_total,
        d_int=d_int if habitabilidade else np.nan,
        d_ext=d_ext if habitabilidade else np.nan,
        dc_int=dc_int if habitabilidade else np.nan,
        dc_ext=dc_ext if habitabilidade else np.nan,
        P_din=P_din if habitabilidade else np.nan,
        Rmag=Rmag if habitabilidade else np.nan,
    )

    if show_progress:
        print("___PROGRESS___|0.8", flush=True)

    # ? --- Geração de Gráficos ---
    sy.status("Plotting simulation results...", flush=True)
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
        cte,
    )

    plot_curve_analis(tamanho_pulo, recuo_pulo, L0, deltav0, S_divergencia, cte)

    plot_charspeeds(
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
    )

    plot_plasmaprop(
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
    )

    if habitabilidade:
        plot_habitability_radar(
            cte=cte,
            Dorb=Dorb,
            e=e,
            Rstar=Rstar,
            exoplanet_name=exoplanet_name,
        )
        plot_magnetosphere_shield(
            cte,
            Rplan,
            exoplanet_name,
        )

    if show_progress:
        print("___PROGRESS___|1.0", flush=True)

    sy.fim("SIMULATION COMPLETED", flush=True)

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


# * ============================================
# * Execução em Linha de Comando
# * ============================================
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
        cte=cte_,
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
        habitabilidade=True,
        exoplanet_name=exoplanet_name_,
        Lstar=Lstar_,
        e=e_,
        Ab=Ab_,
        f0=f0_,
        Mmag=Mmag_,
        Dorb=Dorb_,
        Rplan=Rplan_,
        show_progress=False,
    )
