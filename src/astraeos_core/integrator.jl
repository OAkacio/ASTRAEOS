# * ============================================
# * Importação de Pacotes
# * ============================================
using QuadGK

# * ============================================
# * Equações Físicas do Vento Estelar (MHD)
# * ============================================
# ? --- Amortecimento Constante ---
function integral_subsonica(x, vA0, Ma0, y, alpha, S, L0)
    Ma = Ma0 * sqrt(y / alpha) * (x^(S / 2.0))
    vA = vA0 * (x^(-S / 2.0)) * sqrt(y / alpha)
    L = L0 * ((vA / vA0)^2) * (x^(-S / 2.0)) * (1.0 + Ma)
    return 1.0 / L0
end

function integral_supersonica(x, x_t, vA0, Ma0, y, alpha, S, L0)
    Ma = Ma0 * sqrt(y / alpha) * (x_t^(S / 2.0)) * (x / x_t)
    vA = vA0 * (x_t^(-S / 2.0)) * (x_t / x) * sqrt(y / alpha)
    L = L0 * ((vA / vA0)^2) * (x_t^(-S / 2.0)) * (x_t / x) * (1.0 + Ma)
    return 1.0 / L0
end

# ? --- Amortecimento Ressonante ---
function integral_subsonicaRES(x, vA0, Ma0, y, alpha, S, L0)
    Ma = Ma0 * sqrt(y / alpha) * (x^(S / 2.0))
    vA = vA0 * (x^(-S / 2.0)) * sqrt(y / alpha)
    L = L0 * ((vA / vA0)^2) * (x^(-S / 2.0)) * (1.0 + Ma)
    return 1.0 / L
end

function integral_supersonicaRES(x, x_t, vA0, Ma0, y, alpha, S, L0)
    Ma = Ma0 * sqrt(y / alpha) * (x_t^(S / 2.0)) * (x / x_t)
    vA = vA0 * (x_t^(-S / 2.0)) * (x_t / x) * sqrt(y / alpha)
    L = L0 * ((vA / vA0)^2) * (x_t^(-S / 2.0)) * (x_t / x) * (1.0 + Ma)
    return 1.0 / L
end

# * ============================================
# * Equação de Momento e Ponto Crítico
# * ============================================
# ? --- Derivadas da Velocidade do Vento ---
function derivada_velocidade_vento(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0, F = vetor

    # [!] INJEÇÃO DE SEGURANÇA: Usa o fator F passado por argumento
    x_t = (S == 2.0) ? Inf : F^(1.0 / (S - 2.0))

    Ma0 = alpha / vA0

    if x <= x_t
        Z = S
        Ma = Ma0 * sqrt(y / alpha) * (x^(S / 2.0))
        vA = vA0 * (x^(-S / 2.0)) * sqrt(y / alpha)
        L = L0
        res = quadgk(t -> integral_subsonica(t, vA0, Ma0, y, alpha, S, L0), 1.0, x)[1]
        deltav1 = deltav0 * (y / alpha) * (x^S) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    else
        Z = 2.0
        Ma = Ma0 * sqrt(y / alpha) * (x_t^(S / 2.0)) * (x / x_t)
        vA = vA0 * (x_t^(-S / 2.0)) * (x_t / x) * sqrt(y / alpha)
        L = L0
        res_int1 = quadgk(t -> integral_subsonica(t, vA0, Ma0, y, alpha, S, L0), 1.0, x_t)[1]
        res_int2 = quadgk(t -> integral_supersonica(t, x_t, vA0, Ma0, y, alpha, S, L0), x_t, x)[1]
        res = res_int1 + res_int2
        deltav1 = deltav0 * (y / alpha) * (x_t^S) * ((x / x_t)^2) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    end

    razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma)
    numerador = (Z * y / x) * (vT^2 + razao_MA * deltav / 4.0 + (x / (2.0 * Z)) * deltav / L - 1.0 / (2.0 * Z * x))
    denominador = y^2 - vT^2 - (1.0 / 4.0) * razao_MA * deltav

    return numerador / denominador
end

function derivada_velocidade_ventoRES(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0, F = vetor

    # [!] INJEÇÃO DE SEGURANÇA
    x_t = (S == 2.0) ? Inf : F^(1.0 / (S - 2.0))

    Ma0 = alpha / vA0

    if x <= x_t
        Z = S
        Ma = Ma0 * sqrt(y / alpha) * (x^(S / 2.0))
        vA = vA0 * (x^(-S / 2.0)) * sqrt(y / alpha)
        L = L0 * ((vA / vA0)^2) * (x^(-S / 2.0)) * (1.0 + Ma)
        res = quadgk(t -> integral_subsonicaRES(t, vA0, Ma0, y, alpha, S, L0), 1.0, x)[1]
        deltav1 = deltav0 * (y / alpha) * (x^S) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    else
        Z = 2.0
        Ma = Ma0 * sqrt(y / alpha) * (x_t^(S / 2.0)) * (x / x_t)
        vA = vA0 * (x_t^(-S / 2.0)) * (x_t / x) * sqrt(y / alpha)
        L = L0 * ((vA / vA0)^2) * (x_t^(-S / 2.0)) * (x_t / x) * (1.0 + Ma)
        res_int1 = quadgk(t -> integral_subsonicaRES(t, vA0, Ma0, y, alpha, S, L0), 1.0, x_t)[1]
        res_int2 = quadgk(t -> integral_supersonicaRES(t, x_t, vA0, Ma0, y, alpha, S, L0), x_t, x)[1]
        res = res_int1 + res_int2
        deltav1 = deltav0 * (y / alpha) * (x_t^S) * ((x / x_t)^2) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    end

    razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma)
    numerador = (Z * y / x) * (vT^2 + razao_MA * deltav / 4.0 + (x / (2.0 * Z)) * deltav / L - 1.0 / (2.0 * Z * x))
    denominador = y^2 - vT^2 - (1.0 / 4.0) * razao_MA * deltav

    return numerador / denominador
end

# ? --- Topologia do Ponto Crítico ---
function analisa_singularidade_vento(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0, F = vetor

    # [!] INJEÇÃO DE SEGURANÇA
    x_t = (S == 2.0) ? Inf : F^(1.0 / (S - 2.0))

    Ma0 = alpha / vA0

    if x <= x_t
        Z = S
        Ma = Ma0 * sqrt(y / alpha) * (x^(S / 2.0))
        vA = vA0 * (x^(-S / 2.0)) * sqrt(y / alpha)
        L = L0
        res = quadgk(t -> integral_subsonica(t, vA0, Ma0, y, alpha, S, L0), 1.0, x)[1]
        deltav1 = deltav0 * (y / alpha) * (x^S) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    else
        Z = 2.0
        Ma = Ma0 * sqrt(y / alpha) * (x_t^(S / 2.0)) * (x / x_t)
        vA = vA0 * (x_t^(-S / 2.0)) * (x_t / x) * sqrt(y / alpha)
        L = L0
        res_int1 = quadgk(t -> integral_subsonica(t, vA0, Ma0, y, alpha, S, L0), 1.0, x_t)[1]
        res_int2 = quadgk(t -> integral_supersonica(t, x_t, vA0, Ma0, y, alpha, S, L0), x_t, x)[1]
        res = res_int1 + res_int2
        deltav1 = deltav0 * (y / alpha) * (x_t^S) * ((x / x_t)^2) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    end

    razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma)
    numerador = (Z * y / x) * (vT^2 + razao_MA * deltav / 4.0 + (x / (2.0 * Z)) * deltav / L - 1.0 / (2.0 * Z * x))
    denominador = y^2 - vT^2 - (1.0 / 4.0) * razao_MA * deltav

    return (numerador / denominador, numerador, denominador, x, y)
end

function analisa_singularidade_ventoRES(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0, F = vetor

    # [!] INJEÇÃO DE SEGURANÇA
    x_t = (S == 2.0) ? Inf : F^(1.0 / (S - 2.0))

    Ma0 = alpha / vA0

    if x <= x_t
        Z = S
        Ma = Ma0 * sqrt(y / alpha) * (x^(S / 2.0))
        vA = vA0 * (x^(-S / 2.0)) * sqrt(y / alpha)
        L = L0 * ((vA / vA0)^2) * (x^(-S / 2.0)) * (1.0 + Ma)
        res = quadgk(t -> integral_subsonicaRES(t, vA0, Ma0, y, alpha, S, L0), 1.0, x)[1]
        deltav1 = deltav0 * (y / alpha) * (x^S) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    else
        Z = 2.0
        Ma = Ma0 * sqrt(y / alpha) * (x_t^(S / 2.0)) * (x / x_t)
        vA = vA0 * (x_t^(-S / 2.0)) * (x_t / x) * sqrt(y / alpha)
        L = L0 * ((vA / vA0)^2) * (x_t^(-S / 2.0)) * (x_t / x) * (1.0 + Ma)
        res_int1 = quadgk(t -> integral_subsonicaRES(t, vA0, Ma0, y, alpha, S, L0), 1.0, x_t)[1]
        res_int2 = quadgk(t -> integral_supersonicaRES(t, x_t, vA0, Ma0, y, alpha, S, L0), x_t, x)[1]
        res = res_int1 + res_int2
        deltav1 = deltav0 * (y / alpha) * (x_t^S) * ((x / x_t)^2) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        deltav = deltav1 * exp(-res)
    end

    razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma)
    numerador = (Z * y / x) * (vT^2 + razao_MA * deltav / 4.0 + (x / (2.0 * Z)) * deltav / L - 1.0 / (2.0 * Z * x))
    denominador = y^2 - vT^2 - (1.0 / 4.0) * razao_MA * deltav

    return (numerador / denominador, numerador, denominador, x, y)
end

# * ============================================
# * Integração Numérica e Rotinas Principais
# * ============================================
# ? --- RK4 Integrator ---
function runge_kutta_MHD(func, x0_old, x, y0_old, h, vetor)
    x0 = x0_old
    y0 = y0_old
    while (x - x0) > h / 2.0
        k1 = func(x0, y0, vetor)
        k2 = func(x0 + h / 2.0, y0 + (h / 2.0) * k1, vetor)
        k3 = func(x0 + h / 2.0, y0 + (h / 2.0) * k2, vetor)
        k4 = func(x0 + h, y0 + h * k3, vetor)
        y0 = y0 + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        x0 = x0 + h
    end
    return [x0, y0]
end

# ? --- Rotina de Busca da Velocidade Inicial ---
function busca_u0(vT, vetor_base, u0_step, u0_ini, cte, py_cb)
    func_derivada = cte ? derivada_velocidade_vento : derivada_velocidade_ventoRES
    func_analise = cte ? analisa_singularidade_vento : analisa_singularidade_ventoRES

    B0, rho0, _, vA0, L0_input, r0, ve0, deltav0, S, _, phi0, F = vetor_base
    x_vals = 1.0:1e-5:3.9999
    alpha_vals = u0_ini:u0_step:(vT-1e-4)

    d = 1
    x_crit, y_crit, r_crit = 0.0, 0.0, 0.0
    u0_final = 0.0
    x_append_final, y_append_final, vetor_final = Float64[], Float64[], Float64[]

    total_passos = length(alpha_vals)
    contador = 0
    last_pct = -1

    for a in alpha_vals
        if d == 0
            break
        end

        contador += 1
        current_pct = floor(Int, (contador / total_passos) * 100)
        if current_pct > last_pct
            py_cb(current_pct / 100.0)
            last_pct = current_pct
        end

        u0 = a
        u0_aux = u0
        temp_x_append, temp_y_append = Float64[], Float64[]

        vetor = Float64[B0, rho0, vT, vA0, L0_input, r0, ve0, deltav0, S, u0, phi0, F]

        for i in 1:(length(x_vals)-1)
            x0_loop, x_atual = x_vals[i], x_vals[i+1]
            rk = runge_kutta_MHD(func_derivada, x0_loop, x_atual, u0_aux, 1e-5, vetor)
            x_i, y_i = rk[1], rk[2]
            u0_aux = y_i

            r = func_analise(x_i, y_i, vetor)

            if r[2] < 0 && r[3] < 0
                if d == 0 && (r[1] < 1.0 - 1e-2 || r[1] > 1.0 + 1e-2)
                    break
                end

                push!(temp_x_append, x_i)
                push!(temp_y_append, y_i)

                if 1.0 - 1e-2 < r[1] < 1.0 + 1e-2
                    d = 0
                    x_crit, y_crit, r_crit = x_i, y_i, r[1]
                    u0_final = u0
                    x_append_final = copy(temp_x_append)
                    y_append_final = copy(temp_y_append)
                    vetor_final = copy(vetor)
                    break
                end
            else
                if r[1] < 0
                    break
                end
            end
        end
    end
    if u0_final == 0.0
        error("U0_COLLAPSE: The base velocity is exactly 0.0.")
    elseif u0_final == u0_ini
        error("U0_LIMIT: The algorithm hit the lower search limit.")
    end
    py_cb(1.0)
    return u0_final, x_crit, y_crit, r_crit, x_append_final, y_append_final, vetor_final
end

# ? --- Rotina de Integração Espacial ---
function integra_perfil(u0_final, x_crit, y_crit, vetor_final, x_append_final, y_append_final, x_t, passos_recuo, h_step, h_rk, cte, x_sim, py_cb)
    func_derivada = cte ? derivada_velocidade_vento : derivada_velocidade_ventoRES
    func_analise = cte ? analisa_singularidade_vento : analisa_singularidade_ventoRES

    S_interno = vetor_final[9]
    x_t_eff = (S_interno == 2.0) ? Inf : x_t

    x_sub = x_append_final[1:end-passos_recuo]
    y_sub = y_append_final[1:end-passos_recuo]
    x_int = vcat([1.0], x_sub)
    y_int = vcat([u0_final], y_sub)
    x0_old, y0_old = x_sub[end], y_sub[end]

    k1 = func_derivada(x0_old, y0_old, vetor_final)
    k2 = func_derivada(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k1, vetor_final)
    k3 = func_derivada(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k2, vetor_final)
    k4 = func_derivada(x0_old + h_step, y0_old + h_step * k3, vetor_final)

    y0 = y0_old + (h_step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    x0n = x0_old + h_step

    if S_interno == 2.0
        x_e = collect(x0n:h_step:x_sim)
    else
        x_e = vcat(collect(x0n:h_step:(x_t_eff-0.02)), collect((x_t_eff+0.01):0.1:x_sim))
    end

    u0_aux = y0
    x_ext_append, y_ext_append = Float64[], Float64[]

    total_ext = length(x_e) - 1
    contador_ext = 0
    last_pct = -1

    for i in 1:total_ext
        contador_ext += 1
        current_pct = floor(Int, (contador_ext / total_ext) * 100)

        if current_pct > last_pct
            py_cb(current_pct / 100.0)
            last_pct = current_pct
        end

        x_atual, x0_loop = x_e[i+1], x_e[i]
        rk = runge_kutta_MHD(func_derivada, x0_loop, x_atual, u0_aux, h_rk, vetor_final)
        x_i, y_i = rk[1], rk[2]

        push!(x_ext_append, x_i)
        push!(y_ext_append, y_i)
        u0_aux = y_i
    end

    py_cb(1.0)

    x_ext = vcat([x0n], x_ext_append)
    y_ext = vcat([y0], y_ext_append)
    x_total = vcat(x_int, x_ext)
    y_total = vcat(y_int, y_ext)

    # Extração de parâmetros constantes para grandezas do plasma
    rho0 = vetor_final[2]
    vA0 = vetor_final[4]
    L0_input = vetor_final[5]
    ve0 = vetor_final[7]
    deltav0 = vetor_final[8]
    S = vetor_final[9]
    alpha_final = vetor_final[10]
    phi0 = vetor_final[11]

    Ma0 = alpha_final / vA0

    num_alpha_list, den_alpha_list = Vector{Float64}[], Vector{Float64}[]
    vA_total = Float64[]
    rho_total = Float64[]
    phi_total = Float64[]
    deltav2_total = Float64[]
    dmdt_total = Float64[]

    # NOVAS ARRAYS PARA L E P_din
    L_total = Float64[]
    Pdin_total = Float64[]

    # Pós-processamento de toda a física dependente de 'x' e 'y'
    for i in 1:length(x_total)
        x_i = x_total[i]
        y_i = y_total[i]

        # 1. Singularidades
        r = func_analise(x_i, y_i, vetor_final)
        push!(num_alpha_list, [r[2], alpha_final])
        push!(den_alpha_list, [r[3], alpha_final])

        # 2. Grandezas Físicas
        if x_i <= x_t_eff
            vA = vA0 * (x_i^(-S / 2.0)) * sqrt(y_i / alpha_final)
            Ma = Ma0 * sqrt(y_i / alpha_final) * (x_i^(S / 2.0))

            # Cálculo explícito de L para o ponto
            if cte
                L_local = L0_input
                res = quadgk(t -> integral_subsonica(t, vA0, Ma0, y_i, alpha_final, S, L0_input), 1.0, x_i)[1]
            else
                L_local = L0_input * ((vA / vA0)^2) * (x_i^(-S / 2.0)) * (1.0 + Ma)
                res = quadgk(t -> integral_subsonicaRES(t, vA0, Ma0, y_i, alpha_final, S, L0_input), 1.0, x_i)[1]
            end

            rho = rho0 * (alpha_final / y_i) * (x_i^(-S))
            A_r = x_i^S
            deltav1 = deltav0 * (y_i / alpha_final) * (x_i^S) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        else
            vA = vA0 * (x_t_eff^(-S / 2.0)) * (x_t_eff / x_i) * sqrt(y_i / alpha_final)
            Ma = Ma0 * sqrt(y_i / alpha_final) * (x_t_eff^(S / 2.0)) * (x_i / x_t_eff)

            # Cálculo explícito de L para o ponto (supersônico)
            if cte
                L_local = L0_input
                res_int1 = quadgk(t -> integral_subsonica(t, vA0, Ma0, y_i, alpha_final, S, L0_input), 1.0, x_t_eff)[1]
                res_int2 = quadgk(t -> integral_supersonica(t, x_t_eff, vA0, Ma0, y_i, alpha_final, S, L0_input), x_t_eff, x_i)[1]
            else
                L_local = L0_input * ((vA / vA0)^2) * (x_t_eff^(-S / 2.0)) * (x_t_eff / x_i) * (1.0 + Ma)
                res_int1 = quadgk(t -> integral_subsonicaRES(t, vA0, Ma0, y_i, alpha_final, S, L0_input), 1.0, x_t_eff)[1]
                res_int2 = quadgk(t -> integral_supersonicaRES(t, x_t_eff, vA0, Ma0, y_i, alpha_final, S, L0_input), x_t_eff, x_i)[1]
            end
            res = res_int1 + res_int2

            rho = rho0 * (alpha_final / y_i) * (x_t_eff^(-S)) * ((x_t_eff / x_i)^2)
            A_r = (x_t_eff^S) * ((x_i / x_t_eff)^2)
            deltav1 = deltav0 * (y_i / alpha_final) * (x_t_eff^S) * ((x_i / x_t_eff)^2) * (Ma0 / Ma) * ((1.0 + Ma0) / (1.0 + Ma))^2
        end

        deltav2 = deltav1 * exp(-res)

        # dmdt em unidades normalizadas
        dmdt = rho * y_i * A_r

        phi_M = phi0 * ((1.0 + 1.5 * Ma) / (1.0 + 1.5 * Ma0)) * ((1.0 + Ma0) / (1.0 + Ma))^2 * exp(-res)

        # Cálculo da Pressão Dinâmica em CGS (dinas/cm^2). Convertendo y_i (adimensional) para u_cgs.
        u_cgs = y_i * ve0 * 1e5 # ve0 está em km/s, convertemos para cm/s
        pdin = rho * (u_cgs^2)

        push!(vA_total, vA)
        push!(rho_total, rho)
        push!(deltav2_total, deltav2)
        push!(phi_total, phi_M)
        push!(dmdt_total, dmdt)
        push!(L_total, L_local)
        push!(Pdin_total, pdin)
    end

    limiar_brisa = 0.1
    if y_total[end] < limiar_brisa
        error("BREEZE_STATE: The terminal velocity is too low, indicating insufficient u0 precision.")
    end

    return x0n, y0, x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list, vA_total, rho_total, phi_total, deltav2_total, dmdt_total, L_total, Pdin_total
end

function integra_perfil_parker(cs, G, M, ve0, R, rho0, x_sim, h_rk, rsun)
    # Raio crítico em CGS
    rc = (G * M) / (2 * cs^2)

    function parker_root(x, guess)
        v = guess
        for _ in 1:100
            # f(v) = v^2 - log(v^2) - 4*log(x) - 4/x + 3
            f = v^2 - log(v^2) - 4.0 * log(x) - 4.0 / x + 3.0
            # f'(v) = 2v - 2/v
            df = 2.0 * v - 2.0 / v

            v_next = v - f / df

            # Evita que o palpite caia em números negativos (log de negativo)
            if v_next <= 0.0
                v_next = v / 2.0
            end

            if abs(v_next - v) < 1e-8
                return v_next
            end
            v = v_next
        end
        return v
    end

    # Definição do domínio radial 
    r_min = R
    r_max = x_sim * rsun
    pontos = round(Int, x_sim / (100 * h_rk))

    # --- Ramo Subsônico (Cálculos em CGS) ---
    x_int_cgs = collect(range(r_min, stop=rc * 0.999, length=pontos))
    y_int_cgs = zeros(pontos)
    v_guess_int = 0.01

    for i in 1:pontos
        x_norm = x_int_cgs[i] / rc
        v_ans = parker_root(x_norm, v_guess_int)
        y_int_cgs[i] = v_ans * cs
        v_guess_int = v_ans
    end

    # --- Ramo Supersônico (Cálculos em CGS) ---
    x_ext_cgs = collect(range(rc * 1.001, stop=r_max, length=pontos))
    y_ext_cgs = zeros(pontos)
    v_guess_ext = 1.01

    for i in 1:pontos
        x_norm = x_ext_cgs[i] / rc
        v_ans = parker_root(x_norm, v_guess_ext)
        y_ext_cgs[i] = v_ans * cs
        v_guess_ext = v_ans
    end

    # Velocidade na base em CGS
    u0_cgs = y_int_cgs[1]

    # --- Preenchimento de Variáveis Auxiliares (rho, dmdt, L, pdin) ---
    len_total = length(x_int_cgs) + length(x_ext_cgs)

    # Preenchimento com [0.0, 0.0] para evitar o IndexError no Python ([:, 0])
    num_alpha_list = [[0.0, 0.0] for _ in 1:len_total]
    den_alpha_list = [[0.0, 0.0] for _ in 1:len_total]

    vA_total = zeros(len_total)
    phi_total = zeros(len_total)
    deltav2_total = zeros(len_total)

    # Arrays reais para os cálculos de massa e pressão
    rho_total = zeros(len_total)
    dmdt_total = zeros(len_total)
    L_total = zeros(len_total) # Em Parker, o amortecimento mecânico da onda não existe (L=0)
    Pdin_total = zeros(len_total)

    # Concatenação para iterar sobre todo o vento de uma vez
    x_total_cgs = vcat(x_int_cgs, x_ext_cgs)
    y_total_cgs = vcat(y_int_cgs, y_ext_cgs)

    # Constante de perda de massa na base (CGS)
    dmdt0 = rho0 * u0_cgs * R^2

    for i in 1:len_total
        r_cgs = x_total_cgs[i]
        u_cgs = y_total_cgs[i]

        # Física: A conservação estrita impõe que rho = (rho0 * u0 * R^2) / (r^2 * u)
        rho_cgs = (rho0 * u0_cgs * R^2) / (r_cgs^2 * u_cgs)
        dmdt_cgs = rho_cgs * u_cgs * r_cgs^2
        pdin = rho_cgs * (u_cgs^2)

        # Salvando as normalizações (rho/rho0 e dmdt/dmdt0)
        rho_total[i] = rho_cgs / rho0
        dmdt_total[i] = dmdt_cgs / dmdt0
        Pdin_total[i] = pdin
    end

    # --- Normalização Final das Saídas ---
    u0 = u0_cgs / ve0
    x_crit = rc / R
    y_crit = cs / ve0
    x_int = x_int_cgs ./ R
    y_int = y_int_cgs ./ ve0
    x_ext = x_ext_cgs ./ R
    y_ext = y_ext_cgs ./ ve0

    return u0, x_crit, y_crit, x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list, vA_total, rho_total, phi_total, deltav2_total, dmdt_total, L_total, Pdin_total
end