#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <stddef.h>

// ╭──────────────────────────────────────────╮
// │ Adicione este bloco de código:           │
// ╰──────────────────────────────────────────╯
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* ==================================================================== */
/* 1. ESTRUTURAS DE DADOS E QUADGK (Substituindo os .h)                 */
/* ==================================================================== */

typedef void (*progress_cb_t)(double pct);

typedef struct
{
    double v[2];
} pair2_t;

typedef struct
{
    double razao;
    double numerador;
    double denominador;
    double x;
    double y;
} analise_result_t;

typedef struct
{
    double x0;
    double y0;
} rk_result_t;

typedef struct
{
    double u0_final;
    double x_crit;
    double y_crit;
    double r_crit;
    double *x_append_final;
    double *y_append_final;
    size_t append_len;
    double vetor_final[12];
    int vetor_final_set;
    int has_error;
    char error_msg[256];
} busca_u0_result_t;

typedef struct
{
    double x0n, y0;
    double *x_int;
    size_t x_int_len;
    double *y_int;
    size_t y_int_len;
    double *x_ext;
    size_t x_ext_len;
    double *y_ext;
    size_t y_ext_len;
    pair2_t *num_alpha_list;
    size_t num_alpha_list_len;
    pair2_t *den_alpha_list;
    size_t den_alpha_list_len;
    double *vA_total;
    size_t vA_total_len;
    double *rho_total;
    size_t rho_total_len;
    double *phi_total;
    size_t phi_total_len;
    double *deltav2_total;
    size_t deltav2_total_len;
    double dmdt0;
    double *L_total;
    size_t L_total_len;
    double *Pdin_total;
    size_t Pdin_total_len;
    int has_error;
    char error_msg[256];
} integra_perfil_result_t;

typedef struct
{
    double u0, x_crit, y_crit;
    double *x_int;
    size_t x_int_len;
    double *y_int;
    size_t y_int_len;
    double *x_ext;
    size_t x_ext_len;
    double *y_ext;
    size_t y_ext_len;
    pair2_t *num_alpha_list;
    size_t num_alpha_list_len;
    pair2_t *den_alpha_list;
    size_t den_alpha_list_len;
    double *vA_total;
    size_t vA_total_len;
    double *rho_total;
    size_t rho_total_len;
    double *phi_total;
    size_t phi_total_len;
    double *deltav2_total;
    size_t deltav2_total_len;
    double dmdt0;
    double *L_total;
    size_t L_total_len;
    double *Pdin_total;
    size_t Pdin_total_len;
} integra_perfil_parker_result_t;

typedef double (*deriv_func_t)(double x, double y, const double *vetor);

static const double QGK15_X[15] = {-0.9914553711208126, -0.9491079123427585, -0.8648644233597691, -0.7415311855993944, -0.5860872354676911, -0.4058451513773972, -0.2077849550078985, 0.0000000000000000, 0.2077849550078985, 0.4058451513773972, 0.5860872354676911, 0.7415311855993944, 0.8648644233597691, 0.9491079123427585, 0.9914553711208126};
static const double QGK15_WK[15] = {0.0229353220105292, 0.0630920926299786, 0.1047900103222502, 0.1406532597155259, 0.1690047266392679, 0.1903505780647854, 0.2044329400752989, 0.2094821410847278, 0.2044329400752989, 0.1903505780647854, 0.1690047266392679, 0.1406532597155259, 0.1047900103222502, 0.0630920926299786, 0.0229353220105292};
static const double QGK15_WG[15] = {0.0, 0.1294849661688697, 0.0, 0.2797053914892767, 0.0, 0.3818300505051189, 0.0, 0.4179591836734694, 0.0, 0.3818300505051189, 0.0, 0.2797053914892767, 0.0, 0.1294849661688697, 0.0};

typedef double (*qgk_integrand_t)(double t, void *params);
typedef struct
{
    double a, b, I, err;
} qgk_segment_t;

static inline void qgk_eval_segment(qgk_integrand_t f, void *params, double a, double b, double *I_out, double *err_out)
{
    double center = 0.5 * (a + b), half_length = 0.5 * (b - a), resK = 0.0, resG = 0.0;
    for (int i = 0; i < 15; i++)
    {
        double t = center + half_length * QGK15_X[i];
        double fv = f(t, params);
        resK += QGK15_WK[i] * fv;
        resG += QGK15_WG[i] * fv;
    }
    *I_out = resK * half_length;
    *err_out = fabs(resK - resG) * half_length;
}

static inline double quadgk_eval(qgk_integrand_t f, void *params, double a, double b)
{
    const double rtol = 1.4901161193847656e-08;
    if (a == b)
        return 0.0;
    int reversed = 0;
    if (a > b)
    {
        double tmp = a;
        a = b;
        b = tmp;
        reversed = 1;
    }

    // MUDANÇA AQUI: Usa a memória Stack (ultra-rápida) e remove o malloc/free.
    // 2048 subdivisões são mais do que suficientes para QuadGK.
    qgk_segment_t segs[2048];
    long nseg = 1;

    qgk_eval_segment(f, params, a, b, &segs[0].I, &segs[0].err);
    segs[0].a = a;
    segs[0].b = b;
    double total_I, total_err;

    for (;;)
    {
        total_I = 0.0;
        total_err = 0.0;
        for (long i = 0; i < nseg; i++)
        {
            total_I += segs[i].I;
            total_err += segs[i].err;
        }

        if (total_err <= rtol * fabs(total_I) || nseg >= 2048)
            break;

        long worst = 0;
        for (long i = 1; i < nseg; i++)
            if (segs[i].err > segs[worst].err)
                worst = i;

        double wa = segs[worst].a, wb = segs[worst].b, wm = 0.5 * (wa + wb);
        qgk_segment_t left, right;

        left.a = wa;
        left.b = wm;
        qgk_eval_segment(f, params, left.a, left.b, &left.I, &left.err);

        right.a = wm;
        right.b = wb;
        qgk_eval_segment(f, params, right.a, right.b, &right.I, &right.err);

        segs[worst] = left;
        segs[nseg] = right;
        nseg++;
    }

    return reversed ? -total_I : total_I;
}

/* ==================================================================== */
/* 2. LÓGICA DE FÍSICA E INTEGRAÇÃO (Traduzido do Julia)                */
/* ==================================================================== */

double integral_subsonica(double x, double vA0, double Ma0, double y, double alpha, double S, double L0) { return 1.0 / L0; }
double integral_supersonica(double x, double x_t, double vA0, double Ma0, double y, double alpha, double S, double L0) { return 1.0 / L0; }

double integral_subsonicaRES(double x, double vA0, double Ma0, double y, double alpha, double S, double L0)
{
    double Ma = Ma0 * sqrt(y / alpha) * pow(x, S / 2.0);
    double vA = vA0 * pow(x, -S / 2.0) * sqrt(y / alpha);
    double L = L0 * pow(vA / vA0, 2) * pow(x, -S / 2.0) * (1.0 + Ma);
    return 1.0 / L;
}
double integral_supersonicaRES(double x, double x_t, double vA0, double Ma0, double y, double alpha, double S, double L0)
{
    double Ma = Ma0 * sqrt(y / alpha) * pow(x_t, S / 2.0) * (x / x_t);
    double vA = vA0 * pow(x_t, -S / 2.0) * (x_t / x) * sqrt(y / alpha);
    double L = L0 * pow(vA / vA0, 2) * pow(x_t, -S / 2.0) * (x_t / x) * (1.0 + Ma);
    return 1.0 / L;
}

typedef struct
{
    double vA0, Ma0, y, alpha, S, L0;
} sub_params_t;
typedef struct
{
    double x_t, vA0, Ma0, y, alpha, S, L0;
} super_params_t;

static double qgk_integral_subsonica(double t, void *p)
{
    sub_params_t *sp = (sub_params_t *)p;
    return integral_subsonica(t, sp->vA0, sp->Ma0, sp->y, sp->alpha, sp->S, sp->L0);
}
static double qgk_integral_supersonica(double t, void *p)
{
    super_params_t *sp = (super_params_t *)p;
    return integral_supersonica(t, sp->x_t, sp->vA0, sp->Ma0, sp->y, sp->alpha, sp->S, sp->L0);
}
static double qgk_integral_subsonicaRES(double t, void *p)
{
    sub_params_t *sp = (sub_params_t *)p;
    return integral_subsonicaRES(t, sp->vA0, sp->Ma0, sp->y, sp->alpha, sp->S, sp->L0);
}
static double qgk_integral_supersonicaRES(double t, void *p)
{
    super_params_t *sp = (super_params_t *)p;
    return integral_supersonicaRES(t, sp->x_t, sp->vA0, sp->Ma0, sp->y, sp->alpha, sp->S, sp->L0);
}

double derivada_velocidade_vento(double x, double y, const double *vetor)
{
    double vT = vetor[2], vA0 = vetor[3], L0 = vetor[4], deltav0 = vetor[7], S = vetor[8], alpha = vetor[9], F = vetor[11];
    double x_t = (S == 2.0) ? INFINITY : pow(F, 1.0 / (S - 2.0));
    double Ma0 = alpha / vA0;
    double Z, Ma, L, res, deltav1, deltav;
    if (x <= x_t)
    {
        Z = S;
        Ma = Ma0 * sqrt(y / alpha) * pow(x, S / 2.0);
        L = L0;
        sub_params_t sp = {vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonica, &sp, 1.0, x);
        deltav1 = deltav0 * (y / alpha) * pow(x, S) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    else
    {
        Z = 2.0;
        Ma = Ma0 * sqrt(y / alpha) * pow(x_t, S / 2.0) * (x / x_t);
        L = L0;
        sub_params_t sp1 = {vA0, Ma0, y, alpha, S, L0};
        super_params_t sp2 = {x_t, vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonica, &sp1, 1.0, x_t) + quadgk_eval(qgk_integral_supersonica, &sp2, x_t, x);
        deltav1 = deltav0 * (y / alpha) * pow(x_t, S) * pow(x / x_t, 2) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    deltav = deltav1 * exp(-res);
    double razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma);
    return ((Z * y / x) * (vT * vT + razao_MA * deltav / 4.0 - 1.0 / (2.0 * Z * x)) + y * deltav / (2.0 * L)) / (y * y - vT * vT - (1.0 / 4.0) * razao_MA * deltav);
}

double derivada_velocidade_ventoRES(double x, double y, const double *vetor)
{
    double vT = vetor[2], vA0 = vetor[3], L0 = vetor[4], deltav0 = vetor[7], S = vetor[8], alpha = vetor[9], F = vetor[11];
    double x_t = (S == 2.0) ? INFINITY : pow(F, 1.0 / (S - 2.0));
    double Ma0 = alpha / vA0;
    double Z, Ma, vA, L, res, deltav1, deltav;
    if (x <= x_t)
    {
        Z = S;
        Ma = Ma0 * sqrt(y / alpha) * pow(x, S / 2.0);
        vA = vA0 * pow(x, -S / 2.0) * sqrt(y / alpha);
        L = L0 * pow(vA / vA0, 2) * pow(x, -S / 2.0) * (1.0 + Ma);
        sub_params_t sp = {vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonicaRES, &sp, 1.0, x);
        deltav1 = deltav0 * (y / alpha) * pow(x, S) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    else
    {
        Z = 2.0;
        Ma = Ma0 * sqrt(y / alpha) * pow(x_t, S / 2.0) * (x / x_t);
        vA = vA0 * pow(x_t, -S / 2.0) * (x_t / x) * sqrt(y / alpha);
        L = L0 * pow(vA / vA0, 2) * pow(x_t, -S / 2.0) * (x_t / x) * (1.0 + Ma);
        sub_params_t sp1 = {vA0, Ma0, y, alpha, S, L0};
        super_params_t sp2 = {x_t, vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonicaRES, &sp1, 1.0, x_t) + quadgk_eval(qgk_integral_supersonicaRES, &sp2, x_t, x);
        deltav1 = deltav0 * (y / alpha) * pow(x_t, S) * pow(x / x_t, 2) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    deltav = deltav1 * exp(-res);
    double razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma);
    return ((Z * y / x) * (vT * vT + razao_MA * deltav / 4.0 - 1.0 / (2.0 * Z * x)) + y * deltav / (2.0 * L)) / (y * y - vT * vT - (1.0 / 4.0) * razao_MA * deltav);
}

analise_result_t analisa_singularidade_vento(double x, double y, const double *vetor)
{
    double vT = vetor[2], vA0 = vetor[3], L0 = vetor[4], deltav0 = vetor[7], S = vetor[8], alpha = vetor[9], F = vetor[11];
    double x_t = (S == 2.0) ? INFINITY : pow(F, 1.0 / (S - 2.0));
    double Ma0 = alpha / vA0;
    double Z, Ma, L, res, deltav1, deltav;
    if (x <= x_t)
    {
        Z = S;
        Ma = Ma0 * sqrt(y / alpha) * pow(x, S / 2.0);
        L = L0;
        sub_params_t sp = {vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonica, &sp, 1.0, x);
        deltav1 = deltav0 * (y / alpha) * pow(x, S) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    else
    {
        Z = 2.0;
        Ma = Ma0 * sqrt(y / alpha) * pow(x_t, S / 2.0) * (x / x_t);
        L = L0;
        sub_params_t sp1 = {vA0, Ma0, y, alpha, S, L0};
        super_params_t sp2 = {x_t, vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonica, &sp1, 1.0, x_t) + quadgk_eval(qgk_integral_supersonica, &sp2, x_t, x);
        deltav1 = deltav0 * (y / alpha) * pow(x_t, S) * pow(x / x_t, 2) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    deltav = deltav1 * exp(-res);
    double razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma);
    double num = (Z * y / x) * (vT * vT + razao_MA * deltav / 4.0 - 1.0 / (2.0 * Z * x)) + y * deltav / (2.0 * L);
    double den = y * y - vT * vT - (1.0 / 4.0) * razao_MA * deltav;
    analise_result_t r = {num / den, num, den, x, y};
    return r;
}

analise_result_t analisa_singularidade_ventoRES(double x, double y, const double *vetor)
{
    double vT = vetor[2], vA0 = vetor[3], L0 = vetor[4], deltav0 = vetor[7], S = vetor[8], alpha = vetor[9], F = vetor[11];
    double x_t = (S == 2.0) ? INFINITY : pow(F, 1.0 / (S - 2.0));
    double Ma0 = alpha / vA0;
    double Z, Ma, vA, L, res, deltav1, deltav;
    if (x <= x_t)
    {
        Z = S;
        Ma = Ma0 * sqrt(y / alpha) * pow(x, S / 2.0);
        vA = vA0 * pow(x, -S / 2.0) * sqrt(y / alpha);
        L = L0 * pow(vA / vA0, 2) * pow(x, -S / 2.0) * (1.0 + Ma);
        sub_params_t sp = {vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonicaRES, &sp, 1.0, x);
        deltav1 = deltav0 * (y / alpha) * pow(x, S) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    else
    {
        Z = 2.0;
        Ma = Ma0 * sqrt(y / alpha) * pow(x_t, S / 2.0) * (x / x_t);
        vA = vA0 * pow(x_t, -S / 2.0) * (x_t / x) * sqrt(y / alpha);
        L = L0 * pow(vA / vA0, 2) * pow(x_t, -S / 2.0) * (x_t / x) * (1.0 + Ma);
        sub_params_t sp1 = {vA0, Ma0, y, alpha, S, L0};
        super_params_t sp2 = {x_t, vA0, Ma0, y, alpha, S, L0};
        res = quadgk_eval(qgk_integral_subsonicaRES, &sp1, 1.0, x_t) + quadgk_eval(qgk_integral_supersonicaRES, &sp2, x_t, x);
        deltav1 = deltav0 * (y / alpha) * pow(x_t, S) * pow(x / x_t, 2) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
    }
    deltav = deltav1 * exp(-res);
    double razao_MA = (1.0 + 3.0 * Ma) / (1.0 + Ma);
    double num = (Z * y / x) * (vT * vT + razao_MA * deltav / 4.0 - 1.0 / (2.0 * Z * x)) + y * deltav / (2.0 * L);
    double den = y * y - vT * vT - (1.0 / 4.0) * razao_MA * deltav;
    analise_result_t r = {num / den, num, den, x, y};
    return r;
}

size_t integrator_range_length(double a, double step, double b)
{
    if (step == 0.0)
        return 0;
    long len = (long)floor(((b - a) / step) + 1e-10) + 1;
    return (size_t)(len < 0 ? 0 : len);
}

double integrator_range_value(double a, double step, size_t i) { return a + step * (double)i; }

rk_result_t runge_kutta_MHD(deriv_func_t func, double x0_old, double x, double y0_old, double h, const double *vetor)
{
    double x0 = x0_old, y0 = y0_old;
    while ((x - x0) > h / 2.0)
    {
        double k1 = func(x0, y0, vetor);
        double k2 = func(x0 + h / 2.0, y0 + (h / 2.0) * k1, vetor);
        double k3 = func(x0 + h / 2.0, y0 + (h / 2.0) * k2, vetor);
        double k4 = func(x0 + h, y0 + h * k3, vetor);
        y0 += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4);
        x0 += h;
    }
    rk_result_t r = {x0, y0};
    return r;
}

/* ==================================================================== */
/* 3. FUNÇÕES PRINCIPAIS EXPORTADAS PARA O PYTHON                       */
/* ==================================================================== */

busca_u0_result_t busca_u0(double vT, const double *vetor_base, double u0_step, double u0_ini, int cte, progress_cb_t py_cb)
{
    deriv_func_t func_derivada = cte ? derivada_velocidade_vento : derivada_velocidade_ventoRES;
    analise_result_t (*func_analise)(double, double, const double *) = cte ? analisa_singularidade_vento : analisa_singularidade_ventoRES;

    double B0 = vetor_base[0], rho0 = vetor_base[1], vA0 = vetor_base[3], L0_input = vetor_base[4], r0 = vetor_base[5], ve0 = vetor_base[6], deltav0 = vetor_base[7], S = vetor_base[8], phi0 = vetor_base[10], F = vetor_base[11];

    size_t x_vals_len = integrator_range_length(1.0, 1e-5, 3.9999);
    size_t alpha_vals_len = integrator_range_length(u0_ini, u0_step, vT - 1e-4);

    int d = 1;
    double x_crit = 0.0, y_crit = 0.0, r_crit = 0.0, u0_final = 0.0;
    double *x_append_final = NULL, *y_append_final = NULL;
    size_t append_final_len = 0, temp_cap = (x_vals_len > 0 ? x_vals_len : 1), temp_len = 0;
    double vetor_final[12];
    int vetor_final_set = 0;

    double *temp_x_append = (double *)malloc(sizeof(double) * temp_cap);
    double *temp_y_append = (double *)malloc(sizeof(double) * temp_cap);
    long total_passos = (long)alpha_vals_len, contador = 0, last_pct = -1;

    for (size_t ai = 0; ai < alpha_vals_len; ai++)
    {
        if (d == 0)
            break;
        double a = integrator_range_value(u0_ini, u0_step, ai);
        contador++;
        long current_pct = (long)floor(((double)contador / (double)total_passos) * 100.0);
        if (current_pct > last_pct)
        {
            if (py_cb)
                py_cb(current_pct / 100.0);
            last_pct = current_pct;
        }

        double u0 = a, u0_aux = u0;
        temp_len = 0;
        double vetor[12] = {B0, rho0, vT, vA0, L0_input, r0, ve0, deltav0, S, u0, phi0, F};

        if (x_vals_len >= 1)
        {
            for (size_t i = 0; i + 1 < x_vals_len; i++)
            {
                double x0_loop = integrator_range_value(1.0, 1e-5, i), x_atual = integrator_range_value(1.0, 1e-5, i + 1);
                rk_result_t rk = runge_kutta_MHD(func_derivada, x0_loop, x_atual, u0_aux, 1e-5, vetor);
                u0_aux = rk.y0;
                analise_result_t r = func_analise(rk.x0, rk.y0, vetor);

                if (r.numerador < 0 && r.denominador < 0)
                {
                    if (d == 0 && (r.razao < 0.99 || r.razao > 1.01))
                        break;
                    if (temp_len >= temp_cap)
                    {
                        temp_cap *= 2;
                        temp_x_append = (double *)realloc(temp_x_append, sizeof(double) * temp_cap);
                        temp_y_append = (double *)realloc(temp_y_append, sizeof(double) * temp_cap);
                    }
                    temp_x_append[temp_len] = rk.x0;
                    temp_y_append[temp_len] = rk.y0;
                    temp_len++;

                    if (0.99 < r.razao && r.razao < 1.01)
                    {
                        d = 0;
                        x_crit = rk.x0;
                        y_crit = rk.y0;
                        r_crit = r.razao;
                        u0_final = u0;
                        free(x_append_final);
                        free(y_append_final);
                        x_append_final = (double *)malloc(sizeof(double) * temp_len);
                        y_append_final = (double *)malloc(sizeof(double) * temp_len);
                        memcpy(x_append_final, temp_x_append, sizeof(double) * temp_len);
                        memcpy(y_append_final, temp_y_append, sizeof(double) * temp_len);
                        append_final_len = temp_len;
                        memcpy(vetor_final, vetor, sizeof(double) * 12);
                        vetor_final_set = 1;
                        break;
                    }
                }
                else if (r.razao < 0)
                    break;
            }
        }
    }
    free(temp_x_append);
    free(temp_y_append);

    busca_u0_result_t result;
    memset(&result, 0, sizeof(result));
    result.u0_final = u0_final;
    result.x_crit = x_crit;
    result.y_crit = y_crit;
    result.r_crit = r_crit;
    result.x_append_final = x_append_final;
    result.y_append_final = y_append_final;
    result.append_len = append_final_len;
    if (vetor_final_set)
        memcpy(result.vetor_final, vetor_final, sizeof(double) * 12);
    result.vetor_final_set = vetor_final_set;
    result.has_error = 0;
    result.error_msg[0] = '\0';

    if (u0_final == 0.0)
    {
        result.has_error = 1;
        snprintf(result.error_msg, sizeof(result.error_msg), "U0_COLLAPSE: The base velocity is exactly 0.0.");
        return result;
    }
    if (u0_final == u0_ini)
    {
        result.has_error = 1;
        snprintf(result.error_msg, sizeof(result.error_msg), "U0_LIMIT: The algorithm hit the lower search limit.");
        return result;
    }
    if (py_cb)
        py_cb(1.0);
    return result;
}

/* Utilitários para Arrays Dinâmicos (Substitui o Vector do Julia) */
typedef struct
{
    double *data;
    size_t len;
    size_t cap;
} dvec_t;
static void dvec_init(dvec_t *v, size_t initial_cap)
{
    v->data = (double *)malloc(sizeof(double) * (initial_cap > 0 ? initial_cap : 1));
    v->len = 0;
    v->cap = (initial_cap > 0 ? initial_cap : 1);
}
static void dvec_push(dvec_t *v, double x)
{
    if (v->len >= v->cap)
    {
        v->cap *= 2;
        v->data = (double *)realloc(v->data, sizeof(double) * v->cap);
    }
    v->data[v->len++] = x;
}

integra_perfil_result_t integra_perfil(double u0_final, double x_crit, double y_crit, const double *vetor_final, const double *x_append_final, const double *y_append_final, size_t append_len, double x_t, long passos_recuo, double h_step, double h_rk, int cte, double x_sim, progress_cb_t py_cb)
{
    integra_perfil_result_t out;
    memset(&out, 0, sizeof(out));
    deriv_func_t func_derivada = cte ? derivada_velocidade_vento : derivada_velocidade_ventoRES;
    analise_result_t (*func_analise)(double, double, const double *) = cte ? analisa_singularidade_vento : analisa_singularidade_ventoRES;

    double S_interno = vetor_final[8], x_t_eff = (S_interno == 2.0) ? INFINITY : x_t;
    long x_sub_len_signed = (long)append_len - passos_recuo;
    size_t x_sub_len = (size_t)(x_sub_len_signed < 0 ? 0 : x_sub_len_signed);
    size_t x_int_len = x_sub_len + 1;
    double *x_int = (double *)malloc(sizeof(double) * x_int_len), *y_int = (double *)malloc(sizeof(double) * x_int_len);

    x_int[0] = 1.0;
    y_int[0] = u0_final;
    for (size_t i = 0; i < x_sub_len; i++)
    {
        x_int[i + 1] = x_append_final[i];
        y_int[i + 1] = y_append_final[i];
    }

    double x0_old = x_append_final[x_sub_len - 1], y0_old = y_append_final[x_sub_len - 1];
    double k1 = func_derivada(x0_old, y0_old, vetor_final);
    double k2 = func_derivada(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k1, vetor_final);
    double k3 = func_derivada(x0_old + h_step / 2.0, y0_old + (h_step / 2.0) * k2, vetor_final);
    double k4 = func_derivada(x0_old + h_step, y0_old + h_step * k3, vetor_final);
    double y0 = y0_old + (h_step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4), x0n = x0_old + h_step;

    dvec_t x_e;
    if (S_interno == 2.0)
    {
        size_t n = integrator_range_length(x0n, h_step, x_sim);
        dvec_init(&x_e, n > 0 ? n : 1);
        for (size_t i = 0; i < n; i++)
            dvec_push(&x_e, integrator_range_value(x0n, h_step, i));
    }
    else
    {
        size_t n1 = integrator_range_length(x0n, h_step, x_t_eff - 0.02), n2 = integrator_range_length(x_t_eff + 0.01, 0.1, x_sim);
        dvec_init(&x_e, (n1 + n2) > 0 ? (n1 + n2) : 1);
        for (size_t i = 0; i < n1; i++)
            dvec_push(&x_e, integrator_range_value(x0n, h_step, i));
        for (size_t i = 0; i < n2; i++)
            dvec_push(&x_e, integrator_range_value(x_t_eff + 0.01, 0.1, i));
    }

    double u0_aux = y0;
    dvec_t x_ext_append, y_ext_append;
    dvec_init(&x_ext_append, x_e.len > 1 ? x_e.len - 1 : 1);
    dvec_init(&y_ext_append, x_e.len > 1 ? x_e.len - 1 : 1);
    long total_ext = (long)x_e.len - 1, contador_ext = 0, last_pct = -1;

    for (long i = 0; i < total_ext; i++)
    {
        contador_ext++;
        long current_pct = (long)floor(((double)contador_ext / (double)total_ext) * 100.0);
        if (current_pct > last_pct)
        {
            if (py_cb)
                py_cb(current_pct / 100.0);
            last_pct = current_pct;
        }
        rk_result_t rk = runge_kutta_MHD(func_derivada, x_e.data[i], x_e.data[i + 1], u0_aux, h_rk, vetor_final);
        dvec_push(&x_ext_append, rk.x0);
        dvec_push(&y_ext_append, rk.y0);
        u0_aux = rk.y0;
    }
    if (py_cb)
        py_cb(1.0);

    size_t x_ext_len = x_ext_append.len + 1;
    double *x_ext = (double *)malloc(sizeof(double) * x_ext_len), *y_ext = (double *)malloc(sizeof(double) * x_ext_len);
    x_ext[0] = x0n;
    y_ext[0] = y0;
    for (size_t i = 0; i < x_ext_append.len; i++)
    {
        x_ext[i + 1] = x_ext_append.data[i];
        y_ext[i + 1] = y_ext_append.data[i];
    }
    free(x_ext_append.data);
    free(y_ext_append.data);
    free(x_e.data);

    size_t x_total_len = x_int_len + x_ext_len;
    double *x_total = (double *)malloc(sizeof(double) * x_total_len), *y_total = (double *)malloc(sizeof(double) * x_total_len);
    memcpy(x_total, x_int, sizeof(double) * x_int_len);
    memcpy(x_total + x_int_len, x_ext, sizeof(double) * x_ext_len);
    memcpy(y_total, y_int, sizeof(double) * x_int_len);
    memcpy(y_total + x_int_len, y_ext, sizeof(double) * x_ext_len);

    double rho0 = vetor_final[1], vA0 = vetor_final[3], L0_input = vetor_final[4], ve0 = vetor_final[6], deltav0 = vetor_final[7], S = vetor_final[8], alpha_final = vetor_final[9], phi0 = vetor_final[10], Ma0 = alpha_final / vA0;

    pair2_t *num_alpha_list = (pair2_t *)malloc(sizeof(pair2_t) * x_total_len), *den_alpha_list = (pair2_t *)malloc(sizeof(pair2_t) * x_total_len);
    double *vA_total = (double *)malloc(sizeof(double) * x_total_len), *rho_total = (double *)malloc(sizeof(double) * x_total_len), *phi_total = (double *)malloc(sizeof(double) * x_total_len), *deltav2_total = (double *)malloc(sizeof(double) * x_total_len), *L_total = (double *)malloc(sizeof(double) * x_total_len), *Pdin_total = (double *)malloc(sizeof(double) * x_total_len);

    for (size_t i = 0; i < x_total_len; i++)
    {
        double x_i = x_total[i], y_i = y_total[i];
        analise_result_t r = func_analise(x_i, y_i, vetor_final);
        num_alpha_list[i].v[0] = r.numerador;
        num_alpha_list[i].v[1] = alpha_final;
        den_alpha_list[i].v[0] = r.denominador;
        den_alpha_list[i].v[1] = alpha_final;

        double vA, Ma, L_local, res, rho, deltav1;
        if (x_i <= x_t_eff)
        {
            vA = vA0 * pow(x_i, -S / 2.0) * sqrt(y_i / alpha_final);
            Ma = Ma0 * sqrt(y_i / alpha_final) * pow(x_i, S / 2.0);
            sub_params_t sp = {vA0, Ma0, y_i, alpha_final, S, L0_input};
            if (cte)
            {
                L_local = L0_input;
                res = quadgk_eval(qgk_integral_subsonica, &sp, 1.0, x_i);
            }
            else
            {
                L_local = L0_input * pow(vA / vA0, 2) * pow(x_i, -S / 2.0) * (1.0 + Ma);
                res = quadgk_eval(qgk_integral_subsonicaRES, &sp, 1.0, x_i);
            }
            rho = rho0 * (alpha_final / y_i) * pow(x_i, -S);
            deltav1 = deltav0 * (y_i / alpha_final) * pow(x_i, S) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
        }
        else
        {
            vA = vA0 * pow(x_t_eff, -S / 2.0) * (x_t_eff / x_i) * sqrt(y_i / alpha_final);
            Ma = Ma0 * sqrt(y_i / alpha_final) * pow(x_t_eff, S / 2.0) * (x_i / x_t_eff);
            sub_params_t sp1 = {vA0, Ma0, y_i, alpha_final, S, L0_input};
            super_params_t sp2 = {x_t_eff, vA0, Ma0, y_i, alpha_final, S, L0_input};
            if (cte)
            {
                L_local = L0_input;
                res = quadgk_eval(qgk_integral_subsonica, &sp1, 1.0, x_t_eff) + quadgk_eval(qgk_integral_supersonica, &sp2, x_t_eff, x_i);
            }
            else
            {
                L_local = L0_input * pow(vA / vA0, 2) * pow(x_t_eff, -S / 2.0) * (x_t_eff / x_i) * (1.0 + Ma);
                res = quadgk_eval(qgk_integral_subsonicaRES, &sp1, 1.0, x_t_eff) + quadgk_eval(qgk_integral_supersonicaRES, &sp2, x_t_eff, x_i);
            }
            rho = rho0 * (alpha_final / y_i) * pow(x_t_eff, -S) * pow(x_t_eff / x_i, 2);
            deltav1 = deltav0 * (y_i / alpha_final) * pow(x_t_eff, S) * pow(x_i / x_t_eff, 2) * (Ma0 / Ma) * pow((1.0 + Ma0) / (1.0 + Ma), 2);
        }

        vA_total[i] = vA;
        rho_total[i] = rho;
        deltav2_total[i] = deltav1 * exp(-res);
        phi_total[i] = phi0 * ((1.0 + 1.5 * Ma) / (1.0 + 1.5 * Ma0)) * pow((1.0 + Ma0) / (1.0 + Ma), 2) * exp(-res);
        L_total[i] = L_local;
        Pdin_total[i] = rho * (y_i * ve0 * y_i * ve0);
    }

    out.dmdt0 = (4.0 * M_PI * rho0 * (u0_final * ve0) * (vetor_final[5] * vetor_final[5])) * (3.1536e7 / 1.9884e33);
    out.has_error = 0;
    out.error_msg[0] = '\0';
    if (y_total[x_total_len - 1] < 0.1)
    {
        out.has_error = 1;
        snprintf(out.error_msg, sizeof(out.error_msg), "BREEZE_STATE: The terminal velocity is too low, indicating insufficient u0 precision.");
    }

    out.x0n = x0n;
    out.y0 = y0;
    out.x_int = x_int;
    out.x_int_len = x_int_len;
    out.y_int = y_int;
    out.y_int_len = x_int_len;
    out.x_ext = x_ext;
    out.x_ext_len = x_ext_len;
    out.y_ext = y_ext;
    out.y_ext_len = x_ext_len;
    out.num_alpha_list = num_alpha_list;
    out.num_alpha_list_len = x_total_len;
    out.den_alpha_list = den_alpha_list;
    out.den_alpha_list_len = x_total_len;
    out.vA_total = vA_total;
    out.vA_total_len = x_total_len;
    out.rho_total = rho_total;
    out.rho_total_len = x_total_len;
    out.phi_total = phi_total;
    out.phi_total_len = x_total_len;
    out.deltav2_total = deltav2_total;
    out.deltav2_total_len = x_total_len;
    out.L_total = L_total;
    out.L_total_len = x_total_len;
    out.Pdin_total = Pdin_total;
    out.Pdin_total_len = x_total_len;

    free(x_total);
    free(y_total);
    return out;
}

static double parker_root(double x, double guess)
{
    double v = guess;
    for (int i = 0; i < 100; i++)
    {
        double f = v * v - log(v * v) - 4.0 * log(x) - 4.0 / x + 3.0, df = 2.0 * v - 2.0 / v, v_next = v - f / df;
        if (v_next <= 0.0)
            v_next = v / 2.0;
        if (fabs(v_next - v) < 1e-8)
            return v_next;
        v = v_next;
    }
    return v;
}

static void linspace_inclusive(double start, double stop, long n, double *out)
{
    if (n <= 0)
        return;
    if (n == 1)
    {
        out[0] = start;
        return;
    }
    double step = (stop - start) / (double)(n - 1);
    for (long i = 0; i < n; i++)
        out[i] = start + step * (double)i;
    out[n - 1] = stop;
}

integra_perfil_parker_result_t integra_perfil_parker(double cs, double G, double M, double ve0, double R, double rho0, double x_sim, double h_rk, double rsun)
{
    integra_perfil_parker_result_t out;
    memset(&out, 0, sizeof(out));
    double rc = (G * M) / (2.0 * cs * cs);
    long pontos = (long)rint(x_sim / (100.0 * h_rk));
    double *x_int_cgs = (double *)malloc(sizeof(double) * (size_t)pontos), *y_int_cgs = (double *)calloc((size_t)pontos, sizeof(double));
    linspace_inclusive(R, rc * 0.999, pontos, x_int_cgs);

    double v_guess = 0.01;
    for (long i = 0; i < pontos; i++)
    {
        y_int_cgs[i] = parker_root(x_int_cgs[i] / rc, v_guess) * cs;
        v_guess = y_int_cgs[i] / cs;
    }

    double *x_ext_cgs = (double *)malloc(sizeof(double) * (size_t)pontos), *y_ext_cgs = (double *)calloc((size_t)pontos, sizeof(double));
    linspace_inclusive(rc * 1.001, x_sim * rsun, pontos, x_ext_cgs);

    v_guess = 1.01;
    for (long i = 0; i < pontos; i++)
    {
        y_ext_cgs[i] = parker_root(x_ext_cgs[i] / rc, v_guess) * cs;
        v_guess = y_ext_cgs[i] / cs;
    }

    size_t len_total = (size_t)pontos * 2;
    pair2_t *num_alpha_list = (pair2_t *)calloc(len_total, sizeof(pair2_t)), *den_alpha_list = (pair2_t *)calloc(len_total, sizeof(pair2_t));
    double *vA_total = (double *)calloc(len_total, sizeof(double)), *phi_total = (double *)calloc(len_total, sizeof(double)), *deltav2_total = (double *)calloc(len_total, sizeof(double)), *rho_total = (double *)calloc(len_total, sizeof(double)), *L_total = (double *)calloc(len_total, sizeof(double)), *Pdin_total = (double *)calloc(len_total, sizeof(double));

    out.dmdt0 = (4.0 * M_PI * rho0 * y_int_cgs[0] * (R * R)) * (3.1536e7 / 1.9884e33);
    for (size_t i = 0; i < (size_t)pontos; i++)
    {
        rho_total[i] = (rho0 * y_int_cgs[0] * (R * R)) / ((x_int_cgs[i] * x_int_cgs[i]) * y_int_cgs[i]);
        Pdin_total[i] = rho_total[i] * (y_int_cgs[i] * y_int_cgs[i]);
        rho_total[pontos + i] = (rho0 * y_int_cgs[0] * (R * R)) / ((x_ext_cgs[i] * x_ext_cgs[i]) * y_ext_cgs[i]);
        Pdin_total[pontos + i] = rho_total[pontos + i] * (y_ext_cgs[i] * y_ext_cgs[i]);
    }

    double *x_int = (double *)malloc(sizeof(double) * (size_t)pontos), *y_int = (double *)malloc(sizeof(double) * (size_t)pontos), *x_ext = (double *)malloc(sizeof(double) * (size_t)pontos), *y_ext = (double *)malloc(sizeof(double) * (size_t)pontos);
    for (long i = 0; i < pontos; i++)
    {
        x_int[i] = x_int_cgs[i] / R;
        y_int[i] = y_int_cgs[i] / ve0;
        x_ext[i] = x_ext_cgs[i] / R;
        y_ext[i] = y_ext_cgs[i] / ve0;
    }

    free(x_int_cgs);
    free(y_int_cgs);
    free(x_ext_cgs);
    free(y_ext_cgs);

    out.u0 = y_int_cgs[0] / ve0;
    out.x_crit = rc / R;
    out.y_crit = cs / ve0;
    out.x_int = x_int;
    out.x_int_len = (size_t)pontos;
    out.y_int = y_int;
    out.y_int_len = (size_t)pontos;
    out.x_ext = x_ext;
    out.x_ext_len = (size_t)pontos;
    out.y_ext = y_ext;
    out.y_ext_len = (size_t)pontos;
    out.num_alpha_list = num_alpha_list;
    out.num_alpha_list_len = len_total;
    out.den_alpha_list = den_alpha_list;
    out.den_alpha_list_len = len_total;
    out.vA_total = vA_total;
    out.vA_total_len = len_total;
    out.rho_total = rho_total;
    out.rho_total_len = len_total;
    out.phi_total = phi_total;
    out.phi_total_len = len_total;
    out.deltav2_total = deltav2_total;
    out.deltav2_total_len = len_total;
    out.L_total = L_total;
    out.L_total_len = len_total;
    out.Pdin_total = Pdin_total;
    out.Pdin_total_len = len_total;

    return out;
}

/* ==================================================================== */
/* 4. FUNÇÕES DE LIMPEZA DE MEMÓRIA (Essenciais para o Python)          */
/* ==================================================================== */

void free_busca_u0_result(busca_u0_result_t *res)
{
    if (res->x_append_final)
        free(res->x_append_final);
    if (res->y_append_final)
        free(res->y_append_final);
}

void free_integra_perfil_result(integra_perfil_result_t *res)
{
    if (res->x_int)
        free(res->x_int);
    if (res->y_int)
        free(res->y_int);
    if (res->x_ext)
        free(res->x_ext);
    if (res->y_ext)
        free(res->y_ext);
    if (res->num_alpha_list)
        free(res->num_alpha_list);
    if (res->den_alpha_list)
        free(res->den_alpha_list);
    if (res->vA_total)
        free(res->vA_total);
    if (res->rho_total)
        free(res->rho_total);
    if (res->phi_total)
        free(res->phi_total);
    if (res->deltav2_total)
        free(res->deltav2_total);
    if (res->L_total)
        free(res->L_total);
    if (res->Pdin_total)
        free(res->Pdin_total);
}

void free_integra_perfil_parker_result(integra_perfil_parker_result_t *res)
{
    if (res->x_int)
        free(res->x_int);
    if (res->y_int)
        free(res->y_int);
    if (res->x_ext)
        free(res->x_ext);
    if (res->y_ext)
        free(res->y_ext);
    if (res->num_alpha_list)
        free(res->num_alpha_list);
    if (res->den_alpha_list)
        free(res->den_alpha_list);
    if (res->vA_total)
        free(res->vA_total);
    if (res->rho_total)
        free(res->rho_total);
    if (res->phi_total)
        free(res->phi_total);
    if (res->deltav2_total)
        free(res->deltav2_total);
    if (res->L_total)
        free(res->L_total);
    if (res->Pdin_total)
        free(res->Pdin_total);
}