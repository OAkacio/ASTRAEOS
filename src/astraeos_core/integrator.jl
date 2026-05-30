# * ============================================
# * Importação de Pacotes
# * ============================================
using QuadGK
using ProgressMeter
using Printf

# * ============================================
# * Definição de Funções
# * ============================================
# ? --- Amoretecimento Constante ---
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
function derivada_velocidade_vento(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0 = vetor
    x_t = 10.0^(1.0 / (S - 2.0))
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
function analisa_singularidade_vento(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0 = vetor
    x_t = 10.0^(1.0 / (S - 2.0))
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
function derivada_velocidade_ventoRES(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0 = vetor
    x_t = 10.0^(1.0 / (S - 2.0))
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
function analisa_singularidade_ventoRES(x, y, vetor)
    B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, alpha, phi0 = vetor
    x_t = 10.0^(1.0 / (S - 2.0))
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

# ? --- Método Numérico ---
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
function busca_u0(vT, vetor_base, u0_step, u0_ini, cte)
    if cte==true
        B0, rho0, _, vA0, L0, r0, ve0, deltav0, S, _, phi0 = vetor_base
        x_vals = 1.0:1e-5:3.9999
        alpha_vals = u0_ini:u0_step:(vT-1e-4)
        d = 1
        x_crit, y_crit, r_crit = 0.0, 0.0, 0.0
        u0_final = 0.0
        x_append_final = Float64[]
        y_append_final = Float64[]
        vetor_final = Float64[]
        pbar_alpha = Progress(length(alpha_vals), dt=0.5, desc="PROGRESSO: ", color=:cyan)
        for a in alpha_vals
            if d == 0
                break
            end
            u0 = a
            u0_aux = u0
            temp_x_append = Float64[]
            temp_y_append = Float64[]
            vetor = Float64[B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, u0, phi0]
            for i in 1:(length(x_vals)-1)
                x0_loop = x_vals[i]
                x_atual = x_vals[i+1]
                rk = runge_kutta_MHD(derivada_velocidade_vento, x0_loop, x_atual, u0_aux, 1e-5, vetor)
                x_i = rk[1]
                y_i = rk[2]
                u0_aux = y_i
                r = analisa_singularidade_vento(x_i, y_i, vetor)
                if r[2] < 0 && r[3] < 0
                    if d == 0 && (r[1] < 1.0 - 1e-2 || r[1] > 1.0 + 1e-2)
                        break
                    end
                    push!(temp_x_append, x_i)
                    push!(temp_y_append, y_i)
                    if 1.0 - 1e-2 < r[1] < 1.0 + 1e-2
                        d = 0
                        x_crit = x_i
                        y_crit = y_i
                        r_crit = r[1]
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
            ProgressMeter.next!(pbar_alpha; showvalues=[("u0 atual", @sprintf("%.5f", u0)), ("vT", @sprintf("%.5f", vT))])
        end
        return u0_final, x_crit, y_crit, r_crit, x_append_final, y_append_final, vetor_final
    else
        B0, rho0, _, vA0, L0, r0, ve0, deltav0, S, _, phi0 = vetor_base
        x_vals = 1.0:1e-5:3.9999
        alpha_vals = u0_ini:u0_step:(vT-1e-4)
        d = 1
        x_crit, y_crit, r_crit = 0.0, 0.0, 0.0
        u0_final = 0.0
        x_append_final = Float64[]
        y_append_final = Float64[]
        vetor_final = Float64[]
        pbar_alpha = Progress(length(alpha_vals), dt=0.5, desc="PROGRESSO: ", color=:cyan)
        for a in alpha_vals
            if d == 0
                break
            end
            u0 = a
            u0_aux = u0
            temp_x_append = Float64[]
            temp_y_append = Float64[]
            vetor = Float64[B0, rho0, vT, vA0, L0, r0, ve0, deltav0, S, u0, phi0]
            for i in 1:(length(x_vals)-1)
                x0_loop = x_vals[i]
                x_atual = x_vals[i+1]
                rk = runge_kutta_MHD(derivada_velocidade_ventoRES, x0_loop, x_atual, u0_aux, 1e-5, vetor)
                x_i = rk[1]
                y_i = rk[2]
                u0_aux = y_i
                r = analisa_singularidade_ventoRES(x_i, y_i, vetor)
                if r[2] < 0 && r[3] < 0
                    if d == 0 && (r[1] < 1.0 - 1e-2 || r[1] > 1.0 + 1e-2)
                        break
                    end
                    push!(temp_x_append, x_i)
                    push!(temp_y_append, y_i)
                    if 1.0 - 1e-2 < r[1] < 1.0 + 1e-2
                        d = 0
                        x_crit = x_i
                        y_crit = y_i
                        r_crit = r[1]
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
            ProgressMeter.next!(pbar_alpha; showvalues=[("u0 atual", @sprintf("%.5f", u0)), ("vT", @sprintf("%.5f", vT))])
        end
        return u0_final, x_crit, y_crit, r_crit, x_append_final, y_append_final, vetor_final
    end
end
function integra_perfil(u0_final, x_crit, y_crit, vetor_final, x_append_final, y_append_final, x_t, passos_recuo, h_step,h_rk,cte, x_sim)
    if cte==true
        x_sub = x_append_final[1:end-passos_recuo]
        y_sub = y_append_final[1:end-passos_recuo]
        x_int = vcat([1.0], x_sub)
        y_int = vcat([u0_final], y_sub)
        x0_old = x_sub[end]
        y0_old = y_sub[end]
        k1 = derivada_velocidade_vento(x0_old, y0_old, vetor_final)
        k2 = derivada_velocidade_vento(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k1, vetor_final)
        k3 = derivada_velocidade_vento(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k2, vetor_final)
        k4 = derivada_velocidade_vento(x0_old + h_step, y0_old + h_step * k3, vetor_final)
        y0 = y0_old + (h_step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        x0n = x0_old + h_step
        x_e_int = x0n:h_step:(x_t-0.02)
        x_e_ext = (x_t+0.01):0.1:x_sim
        x_e = vcat(collect(x_e_int), collect(x_e_ext))
        u0_aux = y0
        x_ext_append = Float64[]
        y_ext_append = Float64[]
        pbar_ext = Progress(length(x_e) - 1, dt=0.5, desc="PROGRESSO: ", color=:yellow)
        for i in 1:(length(x_e)-1)
            x_atual = x_e[i+1]
            x0_loop = x_e[i]
            rk = runge_kutta_MHD(derivada_velocidade_vento, x0_loop, x_atual, u0_aux, h_rk, vetor_final)
            x_i = rk[1]
            y_i = rk[2]
            push!(x_ext_append, x_i)
            push!(y_ext_append, y_i)
            u0_aux = y_i
            ProgressMeter.next!(pbar_ext)
        end
        x_ext = vcat([x0n], x_ext_append)
        y_ext = vcat([y0], y_ext_append)
        x_total = vcat(x_int, x_ext)
        y_total = vcat(y_int, y_ext)
        alpha_final = vetor_final[10]
        num_alpha_list = Vector{Float64}[]
        den_alpha_list = Vector{Float64}[]
        for i in 1:length(x_total)
            resultado_sing = analisa_singularidade_vento(x_total[i], y_total[i], vetor_final)
            num_atual = resultado_sing[2]
            den_atual = resultado_sing[3]

            push!(num_alpha_list, [num_atual, alpha_final])
            push!(den_alpha_list, [den_atual, alpha_final])
        end
        return x0n, y0, x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list
    else
        x_sub = x_append_final[1:end-passos_recuo]
        y_sub = y_append_final[1:end-passos_recuo]
        x_int = vcat([1.0], x_sub)
        y_int = vcat([u0_final], y_sub)
        x0_old = x_sub[end]
        y0_old = y_sub[end]
        k1 = derivada_velocidade_ventoRES(x0_old, y0_old, vetor_final)
        k2 = derivada_velocidade_ventoRES(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k1, vetor_final)
        k3 = derivada_velocidade_ventoRES(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k2, vetor_final)
        k4 = derivada_velocidade_ventoRES(x0_old + h_step, y0_old + h_step * k3, vetor_final)
        y0 = y0_old + (h_step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        x0n = x0_old + h_step
        x_e_int = x0n:h_step:(x_t-0.02)
        x_e_ext = (x_t+0.01):0.1:x_sim
        x_e = vcat(collect(x_e_int), collect(x_e_ext))
        u0_aux = y0
        x_ext_append = Float64[]
        y_ext_append = Float64[]
        pbar_ext = Progress(length(x_e) - 1, dt=0.5, desc="PROGRESSO: ", color=:yellow)
        for i in 1:(length(x_e)-1)
            x_atual = x_e[i+1]
            x0_loop = x_e[i]
            rk = runge_kutta_MHD(derivada_velocidade_ventoRES, x0_loop, x_atual, u0_aux, h_rk, vetor_final)
            x_i = rk[1]
            y_i = rk[2]
            push!(x_ext_append, x_i)
            push!(y_ext_append, y_i)
            u0_aux = y_i
            ProgressMeter.next!(pbar_ext)
        end
        x_ext = vcat([x0n], x_ext_append)
        y_ext = vcat([y0], y_ext_append)
        x_total = vcat(x_int, x_ext)
        y_total = vcat(y_int, y_ext)
        alpha_final = vetor_final[10]
        num_alpha_list = Vector{Float64}[]
        den_alpha_list = Vector{Float64}[]
        for i in 1:length(x_total)
            resultado_sing = analisa_singularidade_ventoRES(x_total[i], y_total[i], vetor_final)
            num_atual = resultado_sing[2]
            den_atual = resultado_sing[3]

            push!(num_alpha_list, [num_atual, alpha_final])
            push!(den_alpha_list, [den_atual, alpha_final])
        end
        return x0n, y0, x_int, y_int, x_ext, y_ext, num_alpha_list, den_alpha_list
    end
end