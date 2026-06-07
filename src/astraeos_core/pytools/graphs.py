#
# * =============================================================================
# * GRAPHS
# * =============================================================================

# ? --- Bibiliotecas do Projeto ---
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (
    AutoMinorLocator,
    LogFormatterMathtext,
    LogLocator,
    MaxNLocator,
    NullFormatter,
)
from matplotlib.colors import LogNorm


def basic(
    x_data,
    y_data,
    title="",
    x_label="EIXO X",
    show_grid=False,
    y_label="EIXO Y",
    show_box=True,
    color="black",
    linewidth=2.5,
    title_fontsize=16,
    axis_fontsize=12,
    linestyle="-",
    alpha=0.8,
    grid_color="#E6E6E6",
    fig_width=7,
    fig_height=6,
    remove_borders=False,
    marker=None,
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="basicgraph",
    show_plot=True,
):
    """
    Gera um gráfico 2D simples de uma única curva com pré-definições de estilo focadas na formalidade científica. A função permite a personalização completa.

    Args:
        x_data (array-like): Dados do eixo X.
        y_data (array-like): Dados do eixo Y.
        title (str, optional): Título principal do gráfico. Default é "".
        x_label (str, optional): Rótulo do eixo X. Default é "EIXO X".
        y_label (str, optional): Rótulo do eixo Y. Default é "EIXO Y".
        show_grid (bool, optional): Ativa a grade no fundo do gráfico. Default é False.
        show_box (bool, optional): Mantém a caixa ao redor do gráfico. Default é True.
        color (str, optional): Cor da linha. Default é "black".
        linewidth (float, optional): Espessura da linha. Default é 2.5.
        title_fontsize (int, optional): Tamanho da fonte do título. Default é 16.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos. Default é 12.
        linestyle (str, optional): Estilo da linha (ex: '-', '--', ':'). Default é "-".
        alpha (float, optional): Opacidade da linha (0.0 a 1.0). Default é 0.8.
        grid_color (str, optional): Cor da grade. Default é "#E6E6E6".
        fig_width (float, optional): Largura da figura em polegadas. Default é 7.
        fig_height (float, optional): Altura da figura em polegadas. Default é 6.
        remove_borders (bool, optional): Remove as bordas superior e direita se show_box=True. Default é False.
        marker (str, optional): Marcador dos pontos (ex: 'o', '*', 's'). Default é None.
        save_fig (bool, optional): Se True, salva a figura no diretório 'figures/'. Default é False.
        dpi (int, optional): Resolução da imagem salva. Default é 600.
        file_format (str, optional): Formato do arquivo salvo ('pdf', 'png', 'svg'). Default é "pdf".
        filename (str, optional): Nome do arquivo a ser salvo. Default é "basicgraph".
        show_plot (bool, optional): Exibe o gráfico na tela. Default é True.

    Returns:
        None

    Example:
        >>> import numpy as np
        >>> x = np.linspace(0, 10, 100)
        >>> y = np.sin(x)
        >>> gp.basic(x, y, title="Função Seno", x_label="Tempo (s)", y_label="Amplitude")
    """
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
            "legend.frameon": False,
        }
    )
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
    ax.plot(
        x_data,
        y_data,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        marker=marker,
        label=title if title else None,
    )
    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=15, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which="major", length=8, width=1.2)
    ax.tick_params(which="minor", length=3, width=1.0)
    if show_grid:
        ax.grid(True, linestyle="--", linewidth=0.5, color=grid_color, alpha=0.7)
        ax.set_axisbelow(True)
    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("black")
    plt.tight_layout()
    if save_fig:
        if not os.path.exists("figures"):
            os.makedirs("figures")
        filepath = f"figures/{filename}.{file_format}"
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    return None


def basicerror(
    x_data,
    y_data,
    x_err=None,
    y_err=None,
    title="",
    x_label="EIXO X",
    show_grid=False,
    y_label="EIXO Y",
    show_box=True,
    color="black",
    linewidth=2.5,
    title_fontsize=16,
    axis_fontsize=12,
    linestyle="-",
    alpha=0.8,
    grid_color="#E6E6E6",
    fig_width=7,
    fig_height=6,
    remove_borders=False,
    marker=None,
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="basicerrorgraph",
    show_plot=True,
    ecolor=None,
    elinewidth=1.5,
    capsize=3.0,
    capthick=1.5,
):
    """
    Gera um gráfico 2D simples de uma única curva com barras de erro, com pré-definições de estilo focadas na formalidade científica. A função permite a personalização completa.

    Args:
        x_data (array-like): Dados do eixo X.
        y_data (array-like): Dados do eixo Y.
        x_err (array-like, optional): Valores de erro para o eixo X. Pode ser um valor escalar ou uma lista/array com o mesmo tamanho de x_data. Default é None.
        y_err (array-like, optional): Valores de erro para o eixo Y. Pode ser um valor escalar ou uma lista/array com o mesmo tamanho de y_data. Default é None.
        title (str, optional): Título principal do gráfico. Default é "".
        x_label (str, optional): Rótulo do eixo X. Default é "EIXO X".
        y_label (str, optional): Rótulo do eixo Y. Default é "EIXO Y".
        show_grid (bool, optional): Ativa a grade no fundo do gráfico. Default é False.
        show_box (bool, optional): Mantém a caixa ao redor do gráfico. Default é True.
        color (str, optional): Cor da linha e dos marcadores. Default é "black".
        linewidth (float, optional): Espessura da linha. Default é 2.5.
        title_fontsize (int, optional): Tamanho da fonte do título. Default é 16.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos. Default é 12.
        linestyle (str, optional): Estilo da linha (ex: '-', '--', ':'). Default é "-".
        alpha (float, optional): Opacidade da linha e dos erros (0.0 a 1.0). Default é 0.8.
        grid_color (str, optional): Cor da grade. Default é "#E6E6E6".
        fig_width (float, optional): Largura da figura em polegadas. Default é 7.
        fig_height (float, optional): Altura da figura em polegadas. Default é 6.
        remove_borders (bool, optional): Remove as bordas superior e direita se show_box=True. Default é False.
        marker (str, optional): Marcador dos pontos (ex: 'o', '*', 's'). Default é None.
        save_fig (bool, optional): Se True, salva a figura no diretório 'figures/'. Default é False.
        dpi (int, optional): Resolução da imagem salva. Default é 600.
        file_format (str, optional): Formato do arquivo salvo ('pdf', 'png', 'svg'). Default é "pdf".
        filename (str, optional): Nome do arquivo a ser salvo. Default é "basicerrorgraph".
        show_plot (bool, optional): Exibe o gráfico na tela. Default é True.
        ecolor (str, optional): Cor das barras de erro. Se None, utiliza a mesma cor da linha (parâmetro color). Default é None.
        elinewidth (float, optional): Espessura das barras de erro. Default é 1.5.
        capsize (float, optional): Tamanho dos traços perpendiculares (caps) nas extremidades das barras de erro. Default é 3.0.
        capthick (float, optional): Espessura dos traços perpendiculares (caps). Default é 1.5.

    Returns:
        None

    Example:
        >>> import numpy as np
        >>> x = np.linspace(0.1, 10, 15)
        >>> y = np.log(x)
        >>> x_errors = np.random.uniform(0.1, 0.3, size=len(x))
        >>> y_errors = np.random.uniform(0.2, 0.5, size=len(y))
        >>> basicerror(x, y, x_err=x_errors, y_err=y_errors, title="Logaritmo com Erros", marker="o", linestyle="--")
    """
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
            "legend.frameon": False,
        }
    )

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)

    ax.errorbar(
        x_data,
        y_data,
        xerr=x_err,
        yerr=y_err,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        marker=marker,
        zorder=3,
        label=title if title else None,
        ecolor=ecolor if ecolor else color,
        elinewidth=elinewidth,
        capsize=capsize,
        capthick=capthick,
    )

    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=15, fontweight="bold")

    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which="major", length=8, width=1.2)
    ax.tick_params(which="minor", length=3, width=1.0)

    if show_grid:
        ax.grid(True, linestyle="--", linewidth=0.5, color=grid_color, alpha=0.7)
        ax.set_axisbelow(True)

    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("black")

    plt.tight_layout()

    if save_fig:
        if not os.path.exists("figures"):
            os.makedirs("figures")
        filepath = f"figures/{filename}.{file_format}"
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")

    if show_plot:
        plt.show()
    else:
        plt.close(fig)

    return None


def multi(
    x_list,
    y_list,
    curve_names=None,
    title="",
    x_label="EIXO X",
    y_label="EIXO Y",
    show_grid=False,
    show_box=True,
    color_style="random",
    linewidth=2,
    title_fontsize=14,
    axis_fontsize=12,
    linestyle="cycle",
    alpha=1.0,
    grid_color="#E6E6E6",
    fig_width=7,
    fig_height=6,
    remove_borders=False,
    marker=None,
    show_legend=True,
    legend_title=None,
    legend_box=False,
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="multigraph",
    show_plot=True,
    x_lim=None,
    y_lim=None,
):
    """
    Gera um gráfico 2D com "N" curvas sobrepostas com pré-definições de estilo focadas na formalidade científica. A função permite a personalização completa.

    Args:
        x_list (list de arrays): Lista contendo os arrays do eixo X para cada curva.
        y_list (list de arrays): Lista contendo os arrays do eixo Y para cada curva.
        curve_names (list de str, optional): Nomes de cada curva para a legenda. Default é None.
        title (str, optional): Título principal do gráfico. Default é "".
        x_label (str, optional): Rótulo do eixo X. Default é "EIXO X".
        y_label (str, optional): Rótulo do eixo Y. Default é "EIXO Y".
        show_grid (bool, optional): Ativa a grade no fundo. Default é False.
        show_box (bool, optional): Mantém a caixa ao redor do gráfico. Default é True.
        color_style (str ou list, optional): 'random', 'preto', ou lista de cores customizada. Default é "random".
        linewidth (float, optional): Espessura das linhas. Default é 2.
        title_fontsize (int, optional): Tamanho da fonte do título. Default é 14.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos. Default é 12.
        linestyle (str ou list, optional): 'cycle' para alternar automaticamente, ou lista customizada. Default é "cycle".
        alpha (float, optional): Opacidade das linhas. Default é 1.0.
        grid_color (str, optional): Cor da grade. Default é "#E6E6E6".
        fig_width (float, optional): Largura da figura em polegadas. Default é 7.
        fig_height (float, optional): Altura da figura em polegadas. Default é 6.
        remove_borders (bool, optional): Remove as bordas superior e direita. Default é False.
        marker (str, optional): Marcador dos pontos. Default é None.
        show_legend (bool, optional): Exibe a legenda. Default é True.
        legend_title (str, optional): Título da caixa de legenda. Default é None.
        legend_box (bool, optional): Adiciona moldura ao redor da legenda. Default é False.
        save_fig (bool, optional): Salva a figura no disco. Default é False.
        dpi (int, optional): Resolução de salvamento. Default é 600.
        file_format (str, optional): Formato do arquivo. Default é "pdf".
        filename (str, optional): Nome do arquivo. Default é "multigraph".
        show_plot (bool, optional): Exibe o gráfico na tela. Default é True.
        x_lim (tuple, optional): Limites do eixo X no formato (min, max). Default é None.
        y_lim (tuple, optional): Limites do eixo Y no formato (min, max). Default é None.

    Returns:
        None

    Example:
        >>> import numpy as np
        >>> x1, y1 = np.linspace(0, 5, 50), np.linspace(0, 5, 50)**2
        >>> x2, y2 = np.linspace(0, 5, 50), np.linspace(0, 5, 50)**3
        >>> gp.multi([x1, x2], [y1, y2], curve_names=["Quadrática", "Cúbica"], x_label="x", y_label="f(x)")
    """
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
        }
    )
    if len(x_list) != len(y_list):
        raise ValueError(
            "O número de listas em X deve ser igual ao número de listas em Y."
        )
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
    num_curves = len(x_list)
    if color_style == "preto":
        colors = ["black"] * num_curves
    elif color_style == "random":
        cmap = plt.get_cmap("tab10")
        colors = [cmap(i % 10) for i in range(num_curves)]
    elif isinstance(color_style, list):
        colors = color_style
    else:
        colors = [color_style] * num_curves
    if linestyle == "cycle":
        styles_list = ["-", ":", "--", "-."]
    elif isinstance(linestyle, list):
        styles_list = linestyle
    else:
        styles_list = [linestyle]
    for i in range(num_curves):
        curve_label = curve_names[i] if curve_names else f"Curva {i+1}"
        ax.plot(
            x_list[i],
            y_list[i],
            color=colors[i % len(colors)],
            linewidth=linewidth,
            linestyle=styles_list[i % len(styles_list)],
            alpha=alpha,
            marker=marker,
            label=curve_label,
        )
    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=15, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_xscale("linear")
    ax.set_yscale("linear")

    if x_lim is not None:
        ax.set_xlim(x_lim)
    if y_lim is not None:
        ax.set_ylim(y_lim)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which="major", length=8, width=1.2)
    ax.tick_params(which="minor", length=3, width=1.0)
    if show_legend:
        ax.legend(
            title=legend_title,
            frameon=legend_box,
            fontsize=axis_fontsize * 0.9,
            title_fontsize=axis_fontsize,
            loc="best",
            edgecolor="black" if legend_box else None,
        )
    if show_grid:
        ax.grid(True, linestyle="--", linewidth=0.5, color=grid_color, alpha=0.7)
        ax.set_axisbelow(True)
    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("black")
    plt.tight_layout()
    if save_fig:
        if not os.path.exists("figures"):
            os.makedirs("figures")
        filepath = f"figures/{filename}.{file_format}"
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    return None


def multierror(
    x_list,
    y_list,
    x_err_list=None,
    y_err_list=None,
    curve_names=None,
    title="",
    x_label="EIXO X",
    y_label="EIXO Y",
    show_grid=False,
    show_box=True,
    color_style="random",
    linewidth=2.0,
    title_fontsize=14,
    axis_fontsize=12,
    linestyle="cycle",
    alpha=0.8,
    grid_color="#E6E6E6",
    fig_width=7,
    fig_height=6,
    remove_borders=False,
    marker=None,
    show_legend=True,
    legend_title=None,
    legend_box=False,
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="multierrorgraph",
    show_plot=True,
    ecolor=None,
    elinewidth=1.5,
    capsize=3.0,
    capthick=1.5,
):
    """
    Gera um gráfico 2D com "N" curvas sobrepostas e suas respectivas barras de erro, com pré-definições de estilo focadas na formalidade científica. A função permite a personalização completa.

    Args:
        x_list (list de arrays): Lista contendo os arrays do eixo X para cada curva.
        y_list (list de arrays): Lista contendo os arrays do eixo Y para cada curva.
        x_err_list (list de arrays, optional): Lista contendo os arrays de erro do eixo X para cada curva. Default é None.
        y_err_list (list de arrays, optional): Lista contendo os arrays de erro do eixo Y para cada curva. Default é None.
        curve_names (list de str, optional): Nomes de cada curva para a legenda. Default é None.
        title (str, optional): Título principal do gráfico. Default é "".
        x_label (str, optional): Rótulo do eixo X. Default é "EIXO X".
        y_label (str, optional): Rótulo do eixo Y. Default é "EIXO Y".
        show_grid (bool, optional): Ativa a grade no fundo. Default é False.
        show_box (bool, optional): Mantém a caixa ao redor do gráfico. Default é True.
        color_style (str ou list, optional): 'random', 'preto', ou lista de cores customizada. Default é "random".
        linewidth (float, optional): Espessura das linhas. Default é 2.0.
        title_fontsize (int, optional): Tamanho da fonte do título. Default é 14.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos. Default é 12.
        linestyle (str ou list, optional): 'cycle' para alternar automaticamente, ou lista customizada. Default é "cycle".
        alpha (float, optional): Opacidade das linhas e dos erros (0.0 a 1.0). Default é 0.8.
        grid_color (str, optional): Cor da grade. Default é "#E6E6E6".
        fig_width (float, optional): Largura da figura em polegadas. Default é 7.
        fig_height (float, optional): Altura da figura em polegadas. Default é 6.
        remove_borders (bool, optional): Remove as bordas superior e direita. Default é False.
        marker (str, optional): Marcador dos pontos. Default é None.
        show_legend (bool, optional): Exibe a legenda. Default é True.
        legend_title (str, optional): Título da caixa de legenda. Default é None.
        legend_box (bool, optional): Adiciona moldura ao redor da legenda. Default é False.
        save_fig (bool, optional): Salva a figura no disco. Default é False.
        dpi (int, optional): Resolução de salvamento. Default é 600.
        file_format (str, optional): Formato do arquivo. Default é "pdf".
        filename (str, optional): Nome do arquivo. Default é "multierrorgraph".
        show_plot (bool, optional): Exibe o gráfico na tela. Default é True.
        ecolor (str ou list, optional): Cor das barras de erro. Se None, utiliza a mesma cor da respectiva linha. Default é None.
        elinewidth (float, optional): Espessura das barras de erro. Default é 1.5.
        capsize (float, optional): Tamanho dos traços perpendiculares (caps). Default é 3.0.
        capthick (float, optional): Espessura dos traços perpendiculares (caps). Default é 1.5.

    Returns:
        None

    Example:
        >>> import numpy as np
        >>> x1, y1 = np.linspace(0.1, 5, 10), np.log(np.linspace(0.1, 5, 10))
        >>> x2, y2 = np.linspace(0.1, 5, 10), np.sqrt(np.linspace(0.1, 5, 10))
        >>> err_y1 = np.random.uniform(0.1, 0.3, size=len(y1))
        >>> err_y2 = np.random.uniform(0.1, 0.2, size=len(y2))
        >>> multierror([x1, x2], [y1, y2], y_err_list=[err_y1, err_y2], curve_names=["Log", "Raiz"])
    """
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
            "legend.frameon": False,
        }
    )

    if len(x_list) != len(y_list):
        raise ValueError(
            "O número de listas em X deve ser igual ao número de listas em Y."
        )

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
    num_curves = len(x_list)

    # Definição de Cores
    if color_style == "preto":
        colors = ["black"] * num_curves
    elif color_style == "random":
        cmap = plt.get_cmap("tab10")
        colors = [cmap(i % 10) for i in range(num_curves)]
    elif isinstance(color_style, list):
        colors = color_style
    else:
        colors = [color_style] * num_curves

    # Definição de Linestyles
    if linestyle == "cycle":
        styles_list = ["-", ":", "--", "-."]
    elif isinstance(linestyle, list):
        styles_list = linestyle
    else:
        styles_list = [linestyle]

    # Plotagem de cada curva com erro
    for i in range(num_curves):
        curve_label = curve_names[i] if curve_names else f"Curva {i+1}"

        # Tratamento seguro para os erros (podem ser None)
        curr_x_err = x_err_list[i] if x_err_list and i < len(x_err_list) else None
        curr_y_err = y_err_list[i] if y_err_list and i < len(y_err_list) else None

        # Cor da linha e do erro
        curr_color = colors[i % len(colors)]

        if isinstance(ecolor, list):
            curr_ecolor = ecolor[i % len(ecolor)]
        else:
            curr_ecolor = ecolor if ecolor else curr_color

        ax.errorbar(
            x_list[i],
            y_list[i],
            xerr=curr_x_err,
            yerr=curr_y_err,
            color=curr_color,
            linewidth=linewidth,
            linestyle=styles_list[i % len(styles_list)],
            alpha=alpha,
            marker=marker,
            zorder=3,
            label=curve_label,
            ecolor=curr_ecolor,
            elinewidth=elinewidth,
            capsize=capsize,
            capthick=capthick,
        )

    # Estilização
    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=15, fontweight="bold")

    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_xscale("linear")
    ax.set_yscale("linear")

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which="major", length=8, width=1.2)
    ax.tick_params(which="minor", length=3, width=1.0)

    if show_legend:
        ax.legend(
            title=legend_title,
            frameon=legend_box,
            fontsize=axis_fontsize * 0.9,
            title_fontsize=axis_fontsize,
            loc="best",
            edgecolor="black" if legend_box else None,
        )

    if show_grid:
        ax.grid(True, linestyle="--", linewidth=0.5, color=grid_color, alpha=0.7)
        ax.set_axisbelow(True)

    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("black")

    plt.tight_layout()

    # Salvamento e Exibição
    if save_fig:
        if not os.path.exists("figures"):
            os.makedirs("figures")
        filepath = f"figures/{filename}.{file_format}"
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")

    if show_plot:
        plt.show()
    else:
        plt.close(fig)

    return None


def basicstyle(
    x_data,
    y_data,
    highlight_point=None,
    sigma_intervals=None,
    sigma_colors=("#ccebc5", "#fff2ae", "#fbb4ae"),
    sigma_line_colors=("forestgreen", "orange", "lightcoral"),
    sigma_labels=("1σ (68.3%)", "2σ (95.4%)", "3σ (99.7%)"),
    show_sigma_lines=True,
    sigma_alpha=0.6,
    show_legend_frame=True,
    title="",
    x_label="EIXO X",
    y_label="EIXO Y",
    show_grid=False,
    show_box=True,
    color="black",
    linewidth=2.0,
    title_fontsize=16,
    axis_fontsize=12,
    linestyle="-",
    alpha=0.7,
    grid_color="#E6E6E6",
    fig_width=7,
    fig_height=6,
    remove_borders=False,
    marker=None,
    highlight_color="red",
    curve_label="Dados",
    highlight_marker="o",
    highlight_size=150,
    highlight_label="Destaque",
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="basicdot_graph",
    show_plot=True,
):
    """
    Gera um gráfico 2D focado em exibir uma curva em conjunto com a evidenciação de um ponto específico
    e intervalos de confiança (sigmas). Possui pré-definições de estilo focadas na formalidade científica. A função permite a personalização completa.

    Args:
        x_data (array-like): Dados do eixo X.
        y_data (array-like): Dados do eixo Y.
        highlight_point (tuple, optional): Coordenadas (x, y) do ponto que receberá destaque. Default é None.
        sigma_intervals (list of tuples, optional): Lista com limites (x_min, x_max) para os intervalos de erro. Default é None.
        sigma_colors (tuple, optional): Cores de preenchimento para as regiões sigma.
        sigma_line_colors (tuple, optional): Cores das linhas tracejadas das regiões sigma.
        sigma_labels (tuple, optional): Rótulos das regiões sigma para a legenda.
        show_sigma_lines (bool, optional): Exibe linhas tracejadas delimitando as regiões sigma. Default é True.
        sigma_alpha (float, optional): Opacidade do preenchimento das regiões sigma. Default é 0.6.
        show_legend_frame (bool, optional): Exibe a caixa ao redor da legenda. Default é True.
        title (str, optional): Título do gráfico. Default é "".
        x_label (str, optional): Rótulo do eixo X. Default é "EIXO X".
        y_label (str, optional): Rótulo do eixo Y. Default é "EIXO Y".
        show_grid (bool, optional): Ativa a grade do gráfico. Default é False.
        show_box (bool, optional): Mantém a caixa ao redor do gráfico. Default é True.
        color (str, optional): Cor da curva de dados. Default é "black".
        linewidth (float, optional): Espessura da curva. Default é 2.0.
        title_fontsize (int, optional): Tamanho da fonte do título. Default é 16.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos. Default é 12.
        linestyle (str, optional): Estilo da linha. Default é "-".
        alpha (float, optional): Opacidade da linha. Default é 0.7.
        grid_color (str, optional): Cor da grade. Default é "#E6E6E6".
        fig_width (float, optional): Largura da figura. Default é 7.
        fig_height (float, optional): Altura da figura. Default é 6.
        remove_borders (bool, optional): Remove bordas superior e direita. Default é False.
        marker (str, optional): Marcador de pontos na curva regular. Default é None.
        highlight_color (str, optional): Cor do marcador de destaque. Default é "red".
        curve_label (str, optional): Nome da curva na legenda. Default é "Dados".
        highlight_marker (str, optional): Símbolo do marcador de destaque. Default é "o".
        highlight_size (int, optional): Tamanho do marcador de destaque. Default é 150.
        highlight_label (str, optional): Nome do marcador de destaque na legenda. Default é "Destaque".
        save_fig (bool, optional): Salva a figura em arquivo. Default é False.
        dpi (int, optional): Resolução de salvamento. Default é 600.
        file_format (str, optional): Formato do arquivo gerado. Default é "pdf".
        filename (str, optional): Nome do arquivo. Default é "basicdot_graph".
        show_plot (bool, optional): Exibe o gráfico em tela. Default é True.

    Example:
        >>> import numpy as np
        >>> x = np.linspace(0, 1, 100)
        >>> y = (x - 0.73)**2 * 1000 + 550
        >>> intervals = [(0.70, 0.76), (0.68, 0.78), (0.66, 0.80)]
        >>> basicstyle(x, y, highlight_point=(0.73, 550), sigma_intervals=intervals)
    """
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
        }
    )
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
    ax.plot(
        x_data,
        y_data,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        alpha=alpha,
        marker=marker,
        label=curve_label if curve_label else "Dados",
        zorder=3,
    )
    if sigma_intervals is not None:
        for i in range(len(sigma_intervals) - 1, -1, -1):
            x_min, x_max = sigma_intervals[i]
            s_color = sigma_colors[i] if i < len(sigma_colors) else "gray"
            l_color = sigma_line_colors[i] if i < len(sigma_line_colors) else s_color
            s_label = sigma_labels[i] if i < len(sigma_labels) else f"Região {i+1}"
            ax.axvspan(
                x_min, x_max, color=s_color, alpha=sigma_alpha, label=s_label, zorder=1
            )
            if show_sigma_lines:
                ax.axvline(
                    x_min, color=l_color, linestyle="--", linewidth=1.5, zorder=2
                )
                ax.axvline(
                    x_max, color=l_color, linestyle="--", linewidth=1.5, zorder=2
                )
    if highlight_point is not None:
        ax.scatter(
            highlight_point[0],
            highlight_point[1],
            color=highlight_color,
            marker=highlight_marker,
            s=highlight_size,
            label=highlight_label,
            zorder=5,
        )
    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=15, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_xscale("linear")
    ax.set_yscale("linear")
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which="major", length=8, width=1.2)
    ax.tick_params(which="minor", length=3, width=1.0)
    if title or highlight_point or sigma_intervals is not None:
        ax.legend(frameon=show_legend_frame, fontsize=axis_fontsize * 0.9)
    if show_grid:
        ax.grid(True, linestyle="--", linewidth=0.5, color=grid_color, alpha=0.7)
        ax.set_axisbelow(True)
    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("black")
    plt.tight_layout()
    if save_fig:
        if not os.path.exists("figures"):
            os.makedirs("figures")
        filepath = f"figures/{filename}.{file_format}"
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    return None


def basicstylemulti_log(
    x_data,
    y_data,
    highlight_point=None,
    sigma_intervals=None,
    sigma_colors=("#ccebc5", "#fff2ae", "#fbb4ae"),
    sigma_line_colors=("forestgreen", "orange", "lightcoral"),
    sigma_labels=("1σ (68.3%)", "2σ (95.4%)", "3σ (99.7%)"),
    show_sigma_lines=True,
    sigma_alpha=0.6,
    show_legend_frame=True,
    title="",
    x_label="EIXO X",
    y_label="EIXO Y",
    show_grid=False,
    show_box=True,
    color="black",
    linewidth=2.0,
    title_fontsize=16,
    axis_fontsize=12,
    linestyle="-",
    alpha=0.7,
    grid_color="#E6E6E6",
    fig_width=7,
    fig_height=6,
    remove_borders=False,
    marker=None,
    highlight_color="red",
    curve_label="Dados",
    highlight_marker="o",
    highlight_size=150,
    highlight_label="Destaque",
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="basicmulti_log_graph",
    show_plot=True,
):
    """
    Gera um gráfico 2D em escala logarítmica focado em exibir múltiplas curvas em conjunto,
    com a evidenciação de um ponto específico e intervalos de confiança (sigmas). Possui pré definições de estilo para a formalidade científica.

    Args:
        x_data (array-like ou list de array-like): Dados do eixo X. Pode ser uma lista única ou lista de listas para N curvas.
        y_data (array-like ou list de array-like): Dados do eixo Y. Pode ser uma lista única ou lista de listas para N curvas.
        highlight_point (tuple, optional): Coordenadas (x, y) do ponto que receberá destaque. Default é None.
        sigma_intervals (list of tuples, optional): Lista com limites (x_min, x_max) para os intervalos de erro. Default é None.
        sigma_colors (tuple, optional): Cores de preenchimento para as regiões sigma.
        sigma_line_colors (tuple, optional): Cores das linhas tracejadas das regiões sigma.
        sigma_labels (tuple, optional): Rótulos das regiões sigma para a legenda.
        show_sigma_lines (bool, optional): Exibe linhas tracejadas delimitando as regiões sigma. Default é True.
        sigma_alpha (float, optional): Opacidade do preenchimento das regiões sigma. Default é 0.6.
        show_legend_frame (bool, optional): Exibe a caixa ao redor da legenda. Default é True.
        title (str, optional): Título do gráfico. Default é "".
        x_label (str, optional): Rótulo do eixo X. Default é "EIXO X".
        y_label (str, optional): Rótulo do eixo Y. Default é "EIXO Y".
        show_grid (bool, optional): Ativa a grade do gráfico. Default é False.
        show_box (bool, optional): Mantém a caixa ao redor do gráfico. Default é True.
        color (str ou list, optional): Cor das curvas de dados. Aceita lista de cores para N curvas. Default é "black".
        linewidth (float ou list, optional): Espessura das curvas. Default é 2.0.
        title_fontsize (int, optional): Tamanho da fonte do título. Default é 16.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos. Default é 12.
        linestyle (str ou list, optional): Estilo das linhas. Default é "-".
        alpha (float ou list, optional): Opacidade das linhas. Default é 0.7.
        grid_color (str, optional): Cor da grade. Default é "#E6E6E6".
        fig_width (float, optional): Largura da figura. Default é 7.
        fig_height (float, optional): Altura da figura. Default é 6.
        remove_borders (bool, optional): Remove bordas superior e direita. Default é False.
        marker (str ou list, optional): Marcador de pontos nas curvas regulares. Default é None.
        highlight_color (str, optional): Cor do marcador de destaque. Default é "red".
        curve_label (str ou list, optional): Nome das curvas na legenda. Default é "Dados".
        highlight_marker (str, optional): Símbolo do marcador de destaque. Default é "o".
        highlight_size (int, optional): Tamanho do marcador de destaque. Default é 150.
        highlight_label (str, optional): Nome do marcador de destaque na legenda. Default é "Destaque".
        save_fig (bool, optional): Salva a figura em arquivo. Default é False.
        dpi (int, optional): Resolução de salvamento. Default é 600.
        file_format (str, optional): Formato do arquivo gerado. Default é "pdf".
        filename (str, optional): Nome do arquivo. Default é "basicmulti_log_graph".
        show_plot (bool, optional): Exibe o gráfico em tela. Default é True.

    Example:
        >>> import numpy as np
        >>> x = np.linspace(1, 10, 100)
        >>> y1 = x**2
        >>> y2 = x**3
        >>> intervals = [(2, 3), (4, 5)]
        >>> basicstylemulti_log(
        ...     x_data=[x, x],
        ...     y_data=[y1, y2],
        ...     curve_label=["Quadrática", "Cúbica"],
        ...     color=["blue", "green"],
        ...     highlight_point=(5, 125),
        ...     sigma_intervals=intervals
        ... )
    """
    if isinstance(y_data, np.ndarray) and y_data.ndim == 1:
        y_data_list = [y_data]
        x_data_list = [x_data]
    elif isinstance(y_data, list) and not isinstance(
        y_data[0], (list, tuple, np.ndarray)
    ):
        y_data_list = [y_data]
        x_data_list = [x_data]
    else:
        y_data_list = y_data
        if isinstance(x_data, np.ndarray) and x_data.ndim == 1:
            x_data_list = [x_data] * len(y_data_list)
        elif isinstance(x_data, list) and not isinstance(
            x_data[0], (list, tuple, np.ndarray)
        ):
            x_data_list = [x_data] * len(y_data_list)
        else:
            x_data_list = x_data
    n_curves = len(y_data_list)

    def process_param(param, n):
        if isinstance(param, (list, tuple)) and not isinstance(param, str):
            return list(param) + [param[-1]] * max(0, n - len(param))
        return [param] * n

    colors = process_param(color, n_curves)
    linewidths = process_param(linewidth, n_curves)
    linestyles = process_param(linestyle, n_curves)
    alphas = process_param(alpha, n_curves)
    markers = process_param(marker, n_curves)
    if not isinstance(curve_label, (list, tuple)) and n_curves > 1:
        curve_labels = [f"{curve_label} {i+1}" for i in range(n_curves)]
    else:
        curve_labels = process_param(curve_label, n_curves)
    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
        }
    )
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
    for i in range(n_curves):
        ax.plot(
            x_data_list[i],
            y_data_list[i],
            color=colors[i],
            linewidth=linewidths[i],
            linestyle=linestyles[i],
            alpha=alphas[i],
            marker=markers[i],
            label=curve_labels[i],
            zorder=3,
        )
    if sigma_intervals is not None:
        for i in range(len(sigma_intervals) - 1, -1, -1):
            x_min, x_max = sigma_intervals[i]
            s_color = sigma_colors[i] if i < len(sigma_colors) else "gray"
            l_color = sigma_line_colors[i] if i < len(sigma_line_colors) else s_color
            s_label = sigma_labels[i] if i < len(sigma_labels) else f"Região {i+1}"
            ax.axvspan(
                x_min, x_max, color=s_color, alpha=sigma_alpha, label=s_label, zorder=1
            )
            if show_sigma_lines:
                ax.axvline(
                    x_min, color=l_color, linestyle="--", linewidth=1.5, zorder=2
                )
                ax.axvline(
                    x_max, color=l_color, linestyle="--", linewidth=1.5, zorder=2
                )
    if highlight_point is not None:
        ax.scatter(
            highlight_point[0],
            highlight_point[1],
            color=highlight_color,
            marker=highlight_marker,
            s=highlight_size,
            label=highlight_label,
            zorder=5,
        )
    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=15, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_minor_locator(
        LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10)
    )
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_locator(
        LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10)
    )
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(which="major", length=8, width=1.2)
    ax.tick_params(which="minor", length=3, width=1.0)
    if title or highlight_point or sigma_intervals is not None or n_curves > 1:
        ax.legend(frameon=show_legend_frame, fontsize=axis_fontsize * 0.9)
    if show_grid:
        ax.grid(
            True,
            which="major",
            linestyle="--",
            linewidth=0.6,
            color=grid_color,
            alpha=0.9,
        )
        ax.grid(
            True,
            which="minor",
            linestyle=":",
            linewidth=0.4,
            color=grid_color,
            alpha=0.5,
        )
        ax.set_axisbelow(True)
    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("black")
    plt.tight_layout()
    if save_fig:
        if not os.path.exists("figures"):
            os.makedirs("figures")
        filepath = f"figures/{filename}.{file_format}"
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor="white")
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    return None


def plot(
    x_data,
    y_data,
    x_err=None,
    y_err=None,
    curve_names=None,
    title="",
    x_label="EIXO X",
    y_label="EIXO Y",
    x_scale="linear",
    y_scale="linear",
    x_lim=None,
    y_lim=None,
    show_grid=False,
    show_box=True,
    remove_borders=False,
    background_color="white",
    color_style="random",
    linewidth=2.0,
    linestyle="cycle",
    alpha=0.8,
    marker=None,
    markersize=6.0,
    ecolor=None,
    elinewidth=1.5,
    capsize=3.0,
    capthick=1.5,
    highlight_point=None,
    highlight_color="red",
    highlight_marker="o",
    highlight_size=150,
    highlight_label="Destaque",
    sigma_intervals=None,
    sigma_colors=("#ccebc5", "#fff2ae", "#fbb4ae"),
    sigma_line_colors=("forestgreen", "orange", "lightcoral"),
    sigma_labels=("1σ", "2σ", "3σ"),
    show_sigma_lines=True,
    sigma_alpha=0.6,
    sigma_linewidth=1.5,
    sigma_linestyle="--",
    vlines=None,
    v_colors="black",
    v_linewidth=1.5,
    v_linestyle="--",
    v_alpha=0.8,
    v_labels=None,
    hlines=None,
    h_colors="black",
    h_linewidth=1.5,
    h_linestyle="--",
    h_alpha=0.8,
    h_labels=None,
    show_legend=True,
    legend_title=None,
    legend_box=False,
    legend_fontsize=None,
    legend_loc="best",
    title_fontsize=16,
    axis_fontsize=12,
    title_pad=15,
    label_pad=8,
    fig_width=7,
    fig_height=6,
    figure_dpi=100,
    grid_color="#E6E6E6",
    grid_alpha=0.7,
    grid_linewidth=0.5,
    grid_linestyle="--",
    major_tick_length=8.0,
    major_tick_width=1.2,
    minor_tick_length=3.0,
    minor_tick_width=1.0,
    top_right_ticks=True,
    tick_direction="out",
    block_tick=False,
    show_residuals=False,
    res_x_data=None,
    res_y_data=None,
    res_x_err=None,
    res_y_err=None,
    res_y_label="Resíduos",
    res_y_lim=None,
    res_y_scale="linear",
    res_color_style="black",
    res_linewidth=1.5,
    res_linestyle="",
    res_alpha=0.8,
    res_marker="o",
    res_markersize=6.0,
    res_ecolor=None,
    res_elinewidth=1.5,
    res_capsize=3.0,
    res_capthick=1.5,
    res_hline_y=0.0,
    res_hline_color="black",
    res_hline_style="--",
    res_hline_width=1.0,
    gridspec_height_ratios=[3, 1],
    hspace=0.05,
    save_fig=False,
    dpi=100,
    file_format="png",
    filename="plot_graph",
    show_plot=True,
    theme=None,
):
    """
    Gera um gráfico 2D unificado com personalização completa, incluindo a opção de adicionar
    um painel inferior para exibir N resíduos atrelados ao eixo X principal e adicionar
    linhas de referência horizontais e verticais.

    Args:
        x_data (array-like/list): Dados do eixo X principal.
        y_data (array-like/list): Dados do eixo Y principal.
        x_err (array-like/list, optional): Erros do eixo X principal.
        y_err (array-like/list, optional): Erros do eixo Y principal.
        curve_names (str/list, optional): Rótulos das curvas.
        title (str, optional): Título principal.
        x_label (str, optional): Rótulo do eixo X.
        y_label (str, optional): Rótulo do eixo Y.
        x_scale (str, optional): Escala do eixo X ('linear', 'log').
        y_scale (str, optional): Escala do eixo Y principal ('linear', 'log').
        x_lim (tuple, optional): Limites do eixo X.
        y_lim (tuple, optional): Limites do eixo Y principal.
        show_grid (bool, optional): Ativa grade para os painéis.
        show_box (bool, optional): Mantém caixa dos gráficos.
        remove_borders (bool, optional): Remove bordas superior e direita.
        background_color (str, optional): Cor de fundo da figura e dos eixos.
        color_style (str/list, optional): Estilos de cor das curvas principais.
        linewidth (float/list, optional): Espessura(s) das linhas principais.
        linestyle (str/list, optional): Estilo(s) das linhas principais.
        alpha (float/list, optional): Opacidade(s) das curvas principais.
        marker (str/list, optional): Marcador(es) das curvas principais.
        markersize (float/list, optional): Tamanho(s) dos marcadores principais.
        ecolor (str/list, optional): Cor das barras de erro principais.
        elinewidth (float, optional): Espessura da barra de erro principal.
        capsize (float, optional): Tamanho dos traços do erro principal.
        capthick (float, optional): Espessura dos traços do erro principal.
        highlight_point (tuple/list, optional): Coordenadas de um ponto de destaque ou lista de pontos.
        highlight_color (str/list, optional): Cor(es) do(s) destaque(s).
        highlight_marker (str/list, optional): Marcador(es) do(s) destaque(s).
        highlight_size (int/list, optional): Tamanho(s) do(s) destaque(s).
        highlight_label (str/list, optional): Rótulo(s) do(s) destaque(s).
        sigma_intervals (list, optional): Intervalos de regiões de confiança.
        sigma_colors (tuple/list, optional): Cores de preenchimento dos sigmas.
        sigma_line_colors (tuple/list, optional): Cores das linhas dos sigmas.
        sigma_labels (tuple/str/list, optional): Rótulos das regiões sigma.
        show_sigma_lines (bool, optional): Exibe linhas delimitadoras dos sigmas.
        sigma_alpha (float, optional): Opacidade dos sigmas.
        sigma_linewidth (float, optional): Espessura da linha dos sigmas.
        sigma_linestyle (str, optional): Estilo da linha dos sigmas.
        vlines (list, optional): Lista de coordenadas X para retas verticais.
        v_colors (str/list, optional): Cor(es) das retas verticais.
        v_linewidth (float/list, optional): Espessura(s) das retas verticais.
        v_linestyle (str/list, optional): Estilo(s) das retas verticais.
        v_alpha (float/list, optional): Opacidade(s) das retas verticais.
        v_labels (str/list, optional): Rótulo(s) das retas verticais.
        hlines (list, optional): Lista de coordenadas Y para retas horizontais.
        h_colors (str/list, optional): Cor(es) das retas horizontais.
        h_linewidth (float/list, optional): Espessura(s) das retas horizontais.
        h_linestyle (str/list, optional): Estilo(s) das retas horizontais.
        h_alpha (float/list, optional): Opacidade(s) das retas horizontais.
        h_labels (str/list, optional): Rótulo(s) das retas horizontais.
        show_legend (bool, optional): Ativa a legenda do gráfico principal.
        legend_title (str, optional): Título da legenda principal.
        legend_box (bool, optional): Borda da legenda principal.
        legend_fontsize (float, optional): Tamanho da fonte da legenda principal.
        legend_loc (str, optional): Posição da legenda ('best', 'upper right', etc).
        title_fontsize (int, optional): Tamanho do título.
        axis_fontsize (int, optional): Tamanho dos eixos.
        title_pad (float, optional): Espaçamento do título.
        label_pad (float, optional): Espaçamento dos rótulos.
        fig_width (float, optional): Largura da figura.
        fig_height (float, optional): Altura da figura.
        figure_dpi (int, optional): Resolução de exibição da figura.
        grid_color (str, optional): Cor da grade.
        grid_alpha (float, optional): Opacidade da grade.
        grid_linewidth (float, optional): Espessura da grade.
        grid_linestyle (str, optional): Estilo de linha da grade.
        major_tick_length (float, optional): Comprimento das marcações principais.
        major_tick_width (float, optional): Espessura das marcações principais.
        minor_tick_length (float, optional): Comprimento das marcações menores.
        minor_tick_width (float, optional): Espessura das marcações menores.
        top_right_ticks (bool, optional): Marcações no canto superior e direito. Default é True.
        tick_direction (str, optional): Direção das marcações dos eixos ('in' ou 'out'). Default é 'out'.
        block_tick (bool, optional): Impede a formatação automática dos eixos em escalas como notação científica ou com offset, forçando a exibição padrão dos números. Default é False.
        show_residuals (bool, optional): Ativa o painel de resíduos. Default é False.
        res_x_data (array-like/list, optional): X dos resíduos (se None, usa x_data).
        res_y_data (array-like/list, optional): Y dos resíduos. Requerido se show_residuals for True.
        res_x_err (array-like/list, optional): Erros X dos resíduos.
        res_y_err (array-like/list, optional): Erros Y dos resíduos.
        res_y_label (str, optional): Rótulo do eixo Y dos resíduos.
        res_y_lim (tuple, optional): Limites Y dos resíduos.
        res_y_scale (str, optional): Escala Y dos resíduos.
        res_color_style (str/list, optional): Cor das curvas/pontos de resíduos.
        res_linewidth (float/list, optional): Espessura da linha dos resíduos.
        res_linestyle (str/list, optional): Estilo da linha dos resíduos.
        res_alpha (float/list, optional): Opacidade dos resíduos.
        res_marker (str/list, optional): Marcador dos resíduos.
        res_markersize (float/list, optional): Tamanho dos marcadores dos resíduos.
        res_ecolor (str/list, optional): Cor das barras de erro dos resíduos.
        res_elinewidth (float, optional): Espessura das barras de erro dos resíduos.
        res_capsize (float, optional): Caps das barras de erro dos resíduos.
        res_capthick (float, optional): Espessura dos caps dos resíduos.
        res_hline_y (float, optional): Valor Y da linha base dos resíduos.
        res_hline_color (str, optional): Cor da linha base dos resíduos.
        res_hline_style (str, optional): Estilo da linha base dos resíduos.
        res_hline_width (float, optional): Espessura da linha base dos resíduos.
        gridspec_height_ratios (list, optional): Razão de altura entre painel principal e resíduos.
        hspace (float, optional): Espaçamento vertical entre os painéis.
        save_fig (bool, optional): Salva em disco.
        dpi (int, optional): Resolução do salvamento.
        file_format (str, optional): Formato salvo.
        filename (str, optional): Nome do arquivo com suporte a subdiretórios.
        show_plot (bool, optional): Exibe a interface gráfica.
        theme (str, optional): Tema do gráfico ('dark' ou None).

    Returns:
        None
    """
    if theme == "dark":
        text_color = "#ABB2BF"
        edge_color = "#ABB2BF"
        if background_color == "white":
            background_color = "#242424"
    else:
        text_color = "black"
        edge_color = "black"

    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": tick_direction,
            "ytick.direction": tick_direction,
            "xtick.top": top_right_ticks,
            "ytick.right": top_right_ticks,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
            "legend.frameon": legend_box,
            "text.color": text_color,
            "axes.labelcolor": text_color,
            "xtick.color": text_color,
            "ytick.color": text_color,
        }
    )

    if x_data is None or (hasattr(x_data, "__len__") and len(x_data) == 0):
        return None

    if not (
        isinstance(x_data, list)
        and len(x_data) > 0
        and hasattr(x_data[0], "__iter__")
        and not isinstance(x_data[0], str)
    ):
        x_list = [x_data]
        y_list = [y_data]
        x_err_list = [x_err] if x_err is not None else [None]
        y_err_list = [y_err] if y_err is not None else [None]
    else:
        x_list = x_data
        y_list = y_data
        x_err_list = (
            x_err
            if isinstance(x_err, list)
            and (len(x_err) == 0 or hasattr(x_err[0], "__iter__"))
            else [x_err] * len(x_list)
        )
        y_err_list = (
            y_err
            if isinstance(y_err, list)
            and (len(y_err) == 0 or hasattr(y_err[0], "__iter__"))
            else [y_err] * len(y_list)
        )

    if len(x_list) != len(y_list):
        raise ValueError(
            "O número de arrays em X deve ser igual ao número de arrays em Y."
        )

    if show_residuals:
        if res_y_data is None:
            raise ValueError(
                "res_y_data não pode ser None quando show_residuals for True."
            )

        actual_res_x = res_x_data if res_x_data is not None else x_data

        if not (
            isinstance(actual_res_x, list)
            and len(actual_res_x) > 0
            and hasattr(actual_res_x[0], "__iter__")
            and not isinstance(actual_res_x[0], str)
        ):
            rx_list = [actual_res_x]
            ry_list = [res_y_data]
            rx_err_list = [res_x_err] if res_x_err is not None else [None]
            ry_err_list = [res_y_err] if res_y_err is not None else [None]
        else:
            rx_list = actual_res_x
            ry_list = res_y_data
            rx_err_list = (
                res_x_err
                if isinstance(res_x_err, list)
                and (len(res_x_err) == 0 or hasattr(res_x_err[0], "__iter__"))
                else [res_x_err] * len(rx_list)
            )
            ry_err_list = (
                res_y_err
                if isinstance(res_y_err, list)
                and (len(res_y_err) == 0 or hasattr(res_y_err[0], "__iter__"))
                else [res_y_err] * len(ry_list)
            )

        if len(rx_list) != len(ry_list):
            raise ValueError(
                "O número de arrays em res_x_data deve ser igual ao de res_y_data."
            )

    if show_residuals:
        fig, (ax, ax_res) = plt.subplots(
            2,
            1,
            figsize=(fig_width, fig_height),
            dpi=figure_dpi,
            sharex=True,
            gridspec_kw={"height_ratios": gridspec_height_ratios, "hspace": hspace},
        )
        ax_res.set_facecolor(background_color)
    else:
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=figure_dpi)
        ax_res = None

    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    num_curves = len(x_list)

    colors = (
        color_style
        if isinstance(color_style, list)
        else (
            ["black"] * num_curves
            if color_style == "preto"
            else (
                [plt.get_cmap("tab10")(i % 10) for i in range(num_curves)]
                if color_style == "random"
                else [color_style] * num_curves
            )
        )
    )

    styles_list = (
        linestyle
        if isinstance(linestyle, list)
        else (["-", ":", "--", "-."] if linestyle == "cycle" else [linestyle])
    )

    widths_list = linewidth if isinstance(linewidth, list) else [linewidth]
    alphas_list = alpha if isinstance(alpha, list) else [alpha]
    markers_list = marker if isinstance(marker, list) else [marker]
    ms_list = markersize if isinstance(markersize, list) else [markersize]
    ecolors_list = ecolor if isinstance(ecolor, list) else [ecolor]
    c_names = [curve_names] if isinstance(curve_names, str) else curve_names

    if sigma_intervals is not None:
        s_labels_list = (
            [sigma_labels] if isinstance(sigma_labels, str) else sigma_labels
        )
        s_colors_list = (
            [sigma_colors] if isinstance(sigma_colors, str) else sigma_colors
        )
        s_line_colors_list = (
            [sigma_line_colors]
            if isinstance(sigma_line_colors, str)
            else sigma_line_colors
        )

        for i in range(len(sigma_intervals) - 1, -1, -1):
            x_min, x_max = sigma_intervals[i]
            s_color = s_colors_list[i % len(s_colors_list)] if s_colors_list else "gray"
            l_color = (
                s_line_colors_list[i % len(s_line_colors_list)]
                if s_line_colors_list
                else s_color
            )
            s_label = (
                s_labels_list[i]
                if s_labels_list and i < len(s_labels_list) and s_labels_list[i]
                else None
            )

            ax.axvspan(
                x_min, x_max, color=s_color, alpha=sigma_alpha, label=s_label, zorder=1
            )
            if show_sigma_lines:
                ax.axvline(
                    x_min,
                    color=l_color,
                    linestyle=sigma_linestyle,
                    linewidth=sigma_linewidth,
                    zorder=2,
                )
                ax.axvline(
                    x_max,
                    color=l_color,
                    linestyle=sigma_linestyle,
                    linewidth=sigma_linewidth,
                    zorder=2,
                )

    for i in range(num_curves):
        c_label = c_names[i] if c_names and i < len(c_names) and c_names[i] else None
        curr_x_err = x_err_list[i] if i < len(x_err_list) else None
        curr_y_err = y_err_list[i] if i < len(y_err_list) else None

        curr_color = colors[i % len(colors)]
        curr_style = styles_list[i % len(styles_list)]
        curr_width = widths_list[i % len(widths_list)]
        curr_alpha = alphas_list[i % len(alphas_list)]
        curr_marker = markers_list[i % len(markers_list)]
        curr_ms = ms_list[i % len(ms_list)]

        curr_ecolor = ecolors_list[i % len(ecolors_list)]
        if curr_ecolor is None:
            curr_ecolor = curr_color

        if curr_x_err is not None or curr_y_err is not None:
            ax.errorbar(
                x_list[i],
                y_list[i],
                xerr=curr_x_err,
                yerr=curr_y_err,
                color=curr_color,
                linewidth=curr_width,
                linestyle=curr_style,
                alpha=curr_alpha,
                marker=curr_marker,
                markersize=curr_ms,
                zorder=3,
                label=c_label,
                ecolor=curr_ecolor,
                elinewidth=elinewidth,
                capsize=capsize,
                capthick=capthick,
            )
        else:
            ax.plot(
                x_list[i],
                y_list[i],
                color=curr_color,
                linewidth=curr_width,
                linestyle=curr_style,
                alpha=curr_alpha,
                marker=curr_marker,
                markersize=curr_ms,
                zorder=3,
                label=c_label,
            )

    if highlight_point is not None:
        if (
            (isinstance(highlight_point, tuple) or isinstance(highlight_point, list))
            and len(highlight_point) == 2
            and not isinstance(highlight_point[0], (list, tuple))
        ):
            h_pts = [highlight_point]
        else:
            h_pts = highlight_point

        h_cols = (
            highlight_color if isinstance(highlight_color, list) else [highlight_color]
        )
        h_mrks = (
            highlight_marker
            if isinstance(highlight_marker, list)
            else [highlight_marker]
        )
        h_szs = highlight_size if isinstance(highlight_size, list) else [highlight_size]
        h_labs = (
            highlight_label
            if isinstance(highlight_label, list)
            else [highlight_label] if highlight_label else []
        )

        for idx, pt in enumerate(h_pts):
            c_lab = h_labs[idx % len(h_labs)] if h_labs else None
            ax.scatter(
                pt[0],
                pt[1],
                color=h_cols[idx % len(h_cols)],
                marker=h_mrks[idx % len(h_mrks)],
                s=h_szs[idx % len(h_szs)],
                label=c_lab,
                zorder=5,
            )

    if show_residuals:
        res_num_curves = len(rx_list)
        res_colors = (
            res_color_style
            if isinstance(res_color_style, list)
            else (
                ["black"] * res_num_curves
                if res_color_style == "preto"
                else (
                    [plt.get_cmap("tab10")(i % 10) for i in range(res_num_curves)]
                    if res_color_style == "random"
                    else [res_color_style] * res_num_curves
                )
            )
        )
        res_styles_list = (
            res_linestyle
            if isinstance(res_linestyle, list)
            else (
                ["-", ":", "--", "-."] if res_linestyle == "cycle" else [res_linestyle]
            )
        )
        res_widths_list = (
            res_linewidth if isinstance(res_linewidth, list) else [res_linewidth]
        )
        res_alphas_list = res_alpha if isinstance(res_alpha, list) else [res_alpha]
        res_markers_list = res_marker if isinstance(res_marker, list) else [res_marker]
        res_ms_list = (
            res_markersize if isinstance(res_markersize, list) else [res_markersize]
        )
        res_ecolors_list = res_ecolor if isinstance(res_ecolor, list) else [res_ecolor]

        if res_hline_y is not None:
            ax_res.axhline(
                res_hline_y,
                color=res_hline_color,
                linestyle=res_hline_style,
                linewidth=res_hline_width,
                zorder=2,
            )

        for i in range(res_num_curves):
            curr_rx_err = rx_err_list[i] if i < len(rx_err_list) else None
            curr_ry_err = ry_err_list[i] if i < len(ry_err_list) else None

            curr_rcolor = res_colors[i % len(res_colors)]
            curr_recolor = res_ecolors_list[i % len(res_ecolors_list)]
            if curr_recolor is None:
                curr_recolor = curr_rcolor

            if curr_rx_err is not None or curr_ry_err is not None:
                ax_res.errorbar(
                    rx_list[i],
                    ry_list[i],
                    xerr=curr_rx_err,
                    yerr=curr_ry_err,
                    color=curr_rcolor,
                    linewidth=res_widths_list[i % len(res_widths_list)],
                    linestyle=res_styles_list[i % len(res_styles_list)],
                    alpha=res_alphas_list[i % len(res_alphas_list)],
                    marker=res_markers_list[i % len(res_markers_list)],
                    markersize=res_ms_list[i % len(res_ms_list)],
                    zorder=3,
                    ecolor=curr_recolor,
                    elinewidth=res_elinewidth,
                    capsize=res_capsize,
                    capthick=res_capthick,
                )
            else:
                ax_res.plot(
                    rx_list[i],
                    ry_list[i],
                    color=curr_rcolor,
                    linewidth=res_widths_list[i % len(res_widths_list)],
                    linestyle=res_styles_list[i % len(res_styles_list)],
                    alpha=res_alphas_list[i % len(res_alphas_list)],
                    marker=res_markers_list[i % len(res_markers_list)],
                    markersize=res_ms_list[i % len(res_ms_list)],
                    zorder=3,
                )

    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=title_pad, fontweight="bold")

    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=label_pad)
    if show_residuals:
        ax_res.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=label_pad)
        ax_res.set_ylabel(res_y_label, fontsize=axis_fontsize, labelpad=label_pad)
        ax.tick_params(labelbottom=False)
    else:
        ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=label_pad)

    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale)
    if show_residuals:
        ax_res.set_yscale(res_y_scale)

    if x_lim is not None:
        ax.set_xlim(x_lim)
    if y_lim is not None:
        ax.set_ylim(y_lim)
    if show_residuals and res_y_lim is not None:
        ax_res.set_ylim(res_y_lim)

    axes_list = [ax, ax_res] if show_residuals else [ax]

    if x_scale == "linear":
        for a in axes_list:
            a.xaxis.set_minor_locator(AutoMinorLocator())
    if y_scale == "linear":
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    if show_residuals and res_y_scale == "linear":
        ax_res.yaxis.set_minor_locator(AutoMinorLocator())

    for a in axes_list:
        if block_tick:
            from matplotlib.ticker import ScalarFormatter

            formatter_x = ScalarFormatter()
            formatter_x.set_scientific(False)
            formatter_x.set_useOffset(False)
            a.xaxis.set_major_formatter(formatter_x)

            formatter_y = ScalarFormatter()
            formatter_y.set_scientific(False)
            formatter_y.set_useOffset(False)
            a.yaxis.set_major_formatter(formatter_y)

        a.tick_params(which="major", length=major_tick_length, width=major_tick_width)
        a.tick_params(which="minor", length=minor_tick_length, width=minor_tick_width)

        if show_grid:
            a.grid(
                True,
                linestyle=grid_linestyle,
                linewidth=grid_linewidth,
                color=grid_color,
                alpha=grid_alpha,
            )
            a.set_axisbelow(True)

        if not show_box:
            a.set_frame_on(False)
        elif remove_borders:
            a.spines["top"].set_visible(False)
            a.spines["right"].set_visible(False)
            a.spines["bottom"].set_visible(True)
            a.spines["left"].set_visible(True)
            a.spines["bottom"].set_color(edge_color)
            a.spines["left"].set_color(edge_color)
        else:
            for spine in a.spines.values():
                spine.set_visible(True)
                spine.set_color(edge_color)

    if vlines is not None:
        v_locs = vlines if isinstance(vlines, list) else [vlines]
        v_cols = v_colors if isinstance(v_colors, list) else [v_colors]
        v_lws = v_linewidth if isinstance(v_linewidth, list) else [v_linewidth]
        v_lss = v_linestyle if isinstance(v_linestyle, list) else [v_linestyle]
        v_alps = v_alpha if isinstance(v_alpha, list) else [v_alpha]
        v_labs = (
            v_labels if isinstance(v_labels, list) else [v_labels] if v_labels else []
        )

        for idx, vx in enumerate(v_locs):
            for a in axes_list:
                c_lab = v_labs[idx % len(v_labs)] if v_labs and a == ax else None
                a.axvline(
                    x=vx,
                    color=v_cols[idx % len(v_cols)],
                    linewidth=v_lws[idx % len(v_lws)],
                    linestyle=v_lss[idx % len(v_lss)],
                    alpha=v_alps[idx % len(v_alps)],
                    label=c_lab,
                    zorder=2,
                )

    if hlines is not None:
        h_locs = hlines if isinstance(hlines, list) else [hlines]
        h_cols = h_colors if isinstance(h_colors, list) else [h_colors]
        h_lws = h_linewidth if isinstance(h_linewidth, list) else [h_linewidth]
        h_lss = h_linestyle if isinstance(h_linestyle, list) else [h_linestyle]
        h_alps = h_alpha if isinstance(h_alpha, list) else [h_alpha]
        h_labs = (
            h_labels if isinstance(h_labels, list) else [h_labels] if h_labels else []
        )

        for idx, hy in enumerate(h_locs):
            c_lab = h_labs[idx % len(h_labs)] if h_labs else None
            ax.axhline(
                y=hy,
                color=h_cols[idx % len(h_cols)],
                linewidth=h_lws[idx % len(h_lws)],
                linestyle=h_lss[idx % len(h_lss)],
                alpha=h_alps[idx % len(h_alps)],
                label=c_lab,
                zorder=2,
            )

    if show_legend:
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            final_legend_fontsize = (
                legend_fontsize if legend_fontsize else axis_fontsize * 0.9
            )
            ax.legend(
                title=legend_title,
                frameon=legend_box,
                fontsize=final_legend_fontsize,
                title_fontsize=axis_fontsize,
                loc=legend_loc,
                edgecolor=edge_color if legend_box else None,
            )

    plt.tight_layout()

    if save_fig:
        filepath = f"figures/{filename}.{file_format}"
        import os

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor=background_color)

    if show_plot:
        plt.show()

    return fig


def elipse(
    x_data,
    y_data,
    z_data,
    extra_line_x=None,
    extra_line_y=None,
    extra_line_label="Linha extra",
    extra_line_width=1.0,
    extra_line_style=":",
    extra_line_color="black",
    highlight_point=None,
    ellipse_levels=None,
    sigma_names=None,
    show_sigma=True,
    title=None,
    x_label="EIXO X",
    y_label="EIXO Y",
    x_scale="linear",
    y_scale="linear",
    z_scale="linear",
    show_grid=True,
    show_box=True,
    remove_borders=False,
    legend_frame=True,
    legend_alpha=0.5,
    legend_fontsize=11,
    legend_facecolor="white",
    legend_edgecolor="#333333",
    colorbar_format="neither",
    colorbar_ticks=None,
    cmap="viridis_r",
    title_fontsize=16,
    axis_fontsize=14,
    highlight_label="Destaque",
    highlight_color="red",
    highlight_marker="*",
    highlight_size=150,
    ellipse_styles=["-", ":", ":"],
    ellipse_colors=["red", "green", "blue"],
    ellipse_linewidths=1.8,
    sigma_fontsize=None,
    sigma_fontweight="bold",
    fig_width=8,
    fig_height=6,
    figure_dpi=100,
    show_colorbar=True,
    colorbar_label=rf"$\chi^2$",
    colorbar_pad=0.02,
    colorbar_tick_labelsize=None,
    colorbar_outline_width=1.2,
    heatmap_levels=200,
    cf_antialiased=True,
    z_min_default=1e-10,
    log_locator_base=10.0,
    log_locator_subs=None,
    title_pad=15,
    label_pad=10,
    font_serif=["Computer Modern Roman", "DejaVu Serif"],
    mathtext_fontset="cm",
    axes_linewidth=1.2,
    grid_linestyle=":",
    grid_linewidth=0.5,
    grid_color="black",
    grid_alpha=0.15,
    grid_axisbelow=False,
    save_fig=False,
    dpi=600,
    file_format="pdf",
    filename="ellipse_graph",
    show_plot=True,
):
    """
    Gera um mapa de calor (heat map) frequentemente usado para visualização de chi-quadrado e intervalos de confiança.

    Args:
        x_data (array-like): Matriz de coordenadas X.
        y_data (array-like): Matriz de coordenadas Y.
        z_data (array-like): Matriz de valores Z correspondentes a X e Y.
        extra_line_x (array-like, optional): Coordenadas X para uma linha extra.
        extra_line_y (array-like, optional): Coordenadas Y para uma linha extra.
        extra_line_label (str, optional): Rótulo da linha extra.
        extra_line_width (float, optional): Espessura da linha extra.
        extra_line_style (str, optional): Estilo da linha extra.
        extra_line_color (str, optional): Cor da linha extra.
        highlight_point (tuple, optional): Tupla (x, y) marcando um ponto de destaque.
        ellipse_levels (list, optional): Valores exatos de Z onde os contornos serão desenhados.
        sigma_names (list, optional): Lista de strings nomeando os níveis.
        show_sigma (bool, optional): Escreve o nome do nível sobre a linha da elipse.
        title (str, optional): Título do gráfico.
        x_label (str, optional): Rótulo do eixo X.
        y_label (str, optional): Rótulo do eixo Y.
        x_scale (str, optional): Escala para o eixo X.
        y_scale (str, optional): Escala para o eixo Y.
        z_scale (str, optional): Escala de cor do eixo Z.
        show_grid (bool, optional): Ativa a grade do gráfico.
        show_box (bool, optional): Mantém a moldura do gráfico.
        remove_borders (bool, optional): Remove as bordas direitas e superiores.
        legend_frame (bool, optional): Ativa a caixa ao redor da legenda.
        legend_alpha (float, optional): Transparência do fundo da legenda.
        legend_fontsize (int, optional): Tamanho da fonte da legenda.
        legend_facecolor (str, optional): Cor de fundo da legenda.
        legend_edgecolor (str, optional): Cor da borda da legenda.
        colorbar_format (str, optional): Formato de extensão da colorbar ('max', 'min', 'both', 'neither').
        colorbar_ticks (int, optional): Limite de marcações na barra de cores.
        cmap (str, optional): Colormap para a superfície de preenchimento.
        title_fontsize (int, optional): Tamanho da fonte do título.
        axis_fontsize (int, optional): Tamanho da fonte dos eixos.
        highlight_label (str, optional): Nome para o ponto de destaque na legenda.
        highlight_color (str, optional): Cor do marcador de destaque.
        highlight_marker (str, optional): Símbolo do marcador de destaque.
        highlight_size (int, optional): Tamanho do marcador de destaque.
        ellipse_styles (list, optional): Estilos das elipses traçadas.
        ellipse_colors (list, optional): Cores das elipses traçadas.
        ellipse_linewidths (float, optional): Espessura das linhas das elipses.
        sigma_fontsize (float, optional): Tamanho da fonte dos nomes dos sigmas.
        sigma_fontweight (str, optional): Peso da fonte dos nomes dos sigmas.
        fig_width (float, optional): Largura da figura.
        fig_height (float, optional): Altura da figura.
        figure_dpi (int, optional): Resolução de exibição da figura.
        show_colorbar (bool, optional): Exibe a barra lateral de cores.
        colorbar_label (str, optional): Rótulo da barra de cores.
        colorbar_pad (float, optional): Espaçamento entre o gráfico e a barra de cores.
        colorbar_tick_labelsize (float, optional): Tamanho da fonte dos números na barra de cores.
        colorbar_outline_width (float, optional): Espessura da borda da barra de cores.
        heatmap_levels (int, optional): Níveis gerados no contourf para gradiente suave.
        cf_antialiased (bool, optional): Suavização do mapa de preenchimento.
        z_min_default (float, optional): Mínimo padrão para evitar erros na escala log.
        log_locator_base (float, optional): Base logarítmica da barra de cores.
        log_locator_subs (array-like, optional): Sub-marcações da barra de cores em log.
        title_pad (float, optional): Espaçamento do título.
        label_pad (float, optional): Espaçamento dos rótulos dos eixos.
        font_serif (list, optional): Fontes serifadas utilizadas.
        mathtext_fontset (str, optional): Set de fontes matemáticas.
        axes_linewidth (float, optional): Espessura das bordas dos eixos principais.
        grid_linestyle (str, optional): Estilo da linha da grade.
        grid_linewidth (float, optional): Espessura da linha da grade.
        grid_color (str, optional): Cor da grade.
        grid_alpha (float, optional): Transparência da grade.
        grid_axisbelow (bool, optional): Coloca a grade atrás dos dados.
        save_fig (bool, optional): Salva o gráfico em arquivo.
        dpi (int, optional): Resolução do arquivo salvo.
        file_format (str, optional): Formato do arquivo salvo.
        filename (str, optional): Nome do arquivo a ser salvo (com suporte a subpastas).
        show_plot (bool, optional): Exibe o gráfico na tela.

    Returns:
        tuple: (fig, ax) contendo os objetos de figura e eixo da Matplotlib.
    """
    plt.rcParams.update(
        {
            "text.usetex": False,
            "font.family": "serif",
            "font.serif": font_serif,
            "mathtext.fontset": mathtext_fontset,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "axes.linewidth": axes_linewidth,
        }
    )

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=figure_dpi)

    if z_scale == "log":
        Z_min_positive = (
            np.min(z_data[z_data > 0]) if np.any(z_data > 0) else z_min_default
        )
        norm = LogNorm(vmin=Z_min_positive, vmax=np.max(z_data))
        levels_cf = np.geomspace(Z_min_positive, np.max(z_data), heatmap_levels)
    else:
        norm = None
        levels_cf = heatmap_levels

    cf = ax.contourf(
        x_data,
        y_data,
        z_data,
        levels=levels_cf,
        cmap=cmap,
        norm=norm,
        extend=colorbar_format,
        antialiased=cf_antialiased,
    )

    if ellipse_levels is not None:
        styles_list = (
            [ellipse_styles] if isinstance(ellipse_styles, str) else ellipse_styles
        )
        colors_list = (
            [ellipse_colors] if isinstance(ellipse_colors, str) else ellipse_colors
        )

        if sigma_names is None:
            s_names = [rf"{i+1}$\sigma$" for i in range(len(ellipse_levels))]
        else:
            s_names = [sigma_names] if isinstance(sigma_names, str) else sigma_names

        final_sigma_fontsize = (
            sigma_fontsize if sigma_fontsize is not None else axis_fontsize * 0.9
        )

        for i, level in enumerate(ellipse_levels):
            style = styles_list[i % len(styles_list)]
            color = colors_list[i % len(colors_list)]
            sigma_name = s_names[i % len(s_names)]

            contour = ax.contour(
                x_data,
                y_data,
                z_data,
                levels=[level],
                colors=[color],
                linestyles=style,
                linewidths=ellipse_linewidths,
            )

            if show_sigma:
                fmt = {level: sigma_name}
                labels_text = ax.clabel(
                    contour,
                    inline=True,
                    fontsize=final_sigma_fontsize,
                    fmt=fmt,
                    colors=[color],
                )
                for text in labels_text:
                    text.set_fontweight(sigma_fontweight)

    if extra_line_x is not None and extra_line_y is not None:
        ax.plot(
            extra_line_x,
            extra_line_y,
            color=extra_line_color,
            linestyle=extra_line_style,
            linewidth=extra_line_width,
            label=extra_line_label,
            zorder=4,
        )

    if highlight_point is not None:
        ax.scatter(
            highlight_point[0],
            highlight_point[1],
            color=highlight_color,
            marker=highlight_marker,
            s=highlight_size,
            label=f"{highlight_label}\n({highlight_point[0]:.3f}, {highlight_point[1]:.3f})",
            zorder=5,
        )

    if show_colorbar:
        cbar = fig.colorbar(cf, ax=ax, pad=colorbar_pad)
        cbar.set_label(colorbar_label, fontsize=axis_fontsize)

        final_cbar_labelsize = (
            colorbar_tick_labelsize
            if colorbar_tick_labelsize is not None
            else axis_fontsize * 0.8
        )
        cbar.ax.tick_params(labelsize=final_cbar_labelsize)
        cbar.outline.set_linewidth(colorbar_outline_width)

        if z_scale == "log":
            cbar.ax.yaxis.set_major_formatter(LogFormatterMathtext())
            if colorbar_ticks is not None:
                cbar.ax.yaxis.set_major_locator(
                    LogLocator(base=log_locator_base, numticks=colorbar_ticks)
                )
            else:
                subs_arr = (
                    log_locator_subs
                    if log_locator_subs is not None
                    else np.arange(2, 10) * 0.1
                )
                cbar.ax.yaxis.set_minor_locator(
                    LogLocator(base=log_locator_base, subs=subs_arr)
                )
        else:
            if colorbar_ticks is not None:
                cbar.ax.yaxis.set_major_locator(MaxNLocator(colorbar_ticks))

    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=title_pad)

    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=label_pad)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=label_pad)
    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale)

    ax.minorticks_on()
    ax.tick_params(which="minor", direction="in", top=True, right=True)

    if highlight_point is not None or (
        extra_line_x is not None and extra_line_y is not None
    ):
        ax.legend(
            frameon=legend_frame,
            facecolor=legend_facecolor,
            framealpha=legend_alpha,
            edgecolor=legend_edgecolor,
            fontsize=legend_fontsize,
            loc="best",
        )

    if show_grid:
        ax.grid(
            True,
            linestyle=grid_linestyle,
            linewidth=grid_linewidth,
            color=grid_color,
            alpha=grid_alpha,
        )
        ax.set_axisbelow(grid_axisbelow)

    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)
        ax.spines["bottom"].set_color("black")
        ax.spines["left"].set_color("black")

    ax.set_xlim(np.min(x_data), np.max(x_data))
    ax.set_ylim(np.min(y_data), np.max(y_data))

    plt.tight_layout()

    if save_fig:
        filepath = f"figures/{filename}.{file_format}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight")

    if show_plot:
        plt.show()

    return fig, ax


def radar(
    r_data,
    theta_data,
    z_matrix=None,
    rings_inner=None,
    rings_outer=None,
    rings_colors=None,
    rings_alphas=None,
    rings_labels=None,
    scatter_r=None,
    scatter_theta=None,
    scatter_colors=None,
    scatter_markers=None,
    scatter_sizes=None,
    scatter_labels=None,
    title="",
    r_label="",
    z_label="",
    r_scale="linear",
    z_scale="log",
    r_lim=None,
    z_lim=None,
    cmap="viridis",
    show_grid=True,
    background_color="white",
    grid_color="#E6E6E6",
    grid_alpha=0.7,
    grid_linewidth=0.5,
    grid_linestyle="--",
    show_legend=True,
    legend_title=None,
    legend_box=False,
    legend_fontsize=None,
    legend_loc="upper right",
    title_fontsize=16,
    axis_fontsize=12,
    title_pad=15,
    label_pad=8,
    fig_width=7,
    fig_height=7,
    figure_dpi=100,
    save_fig=False,
    dpi=100,
    file_format="png",
    filename="plot_radar",
    show_plot=True,
    theme=None,
):
    """
    Gera um mapa de radar 2D polar com personalização completa, ideal para visualizar
    a distribuição espacial de grandezas físicas (ex: zonas orbitais, Zonas Habitáveis...).

    Args:
        r_data (array-like): Matriz ou vetor do eixo radial.
        theta_data (array-like): Matriz ou vetor do eixo angular.
        z_matrix (array-like, optional): Matriz 2D representando a grandeza de fundo (heatmap).
        rings_inner (float/list, optional): Raios internos dos anéis (ex: Zona Habitável).
        rings_outer (float/list, optional): Raios externos dos anéis.
        rings_colors (str/list, optional): Cores de preenchimento dos anéis.
        rings_alphas (float/list, optional): Opacidade dos anéis.
        rings_labels (str/list, optional): Rótulos dos anéis.
        scatter_r (array-like/list, optional): Coordenadas radiais para pontos espaciais (ex: planetas).
        scatter_theta (array-like/list, optional): Coordenadas angulares para pontos espaciais.
        scatter_colors (str/list, optional): Cores dos pontos.
        scatter_markers (str/list, optional): Marcadores dos pontos.
        scatter_sizes (float/list, optional): Tamanhos dos pontos.
        scatter_labels (str/list, optional): Rótulos dos pontos.
        title (str, optional): Título principal.
        r_label (str, optional): Rótulo do eixo radial.
        z_label (str, optional): Rótulo da barra de cores (z_matrix).
        r_scale (str, optional): Escala do eixo radial ('linear', 'symlog').
        z_scale (str, optional): Escala de normalização do heatmap ('linear', 'log').
        r_lim (tuple, optional): Limites do eixo radial.
        z_lim (tuple, optional): Limites numéricos para a barra de cores (vmin, vmax).
        cmap (str, optional): Mapa de cores para o z_matrix.
        show_grid (bool, optional): Ativa grade polar.
        background_color (str, optional): Cor de fundo.
        grid_color (str, optional): Cor da grade polar.
        grid_alpha (float, optional): Opacidade da grade.
        grid_linewidth (float, optional): Espessura da grade.
        grid_linestyle (str, optional): Estilo de linha da grade.
        show_legend (bool, optional): Ativa a legenda principal.
        legend_title (str, optional): Título da legenda.
        legend_box (bool, optional): Borda da legenda.
        legend_fontsize (float, optional): Tamanho da fonte da legenda.
        legend_loc (str/tuple, optional): Posição da legenda.
        title_fontsize (int, optional): Tamanho do título.
        axis_fontsize (int, optional): Tamanho da fonte dos rótulos e eixos.
        title_pad (float, optional): Espaçamento do título.
        label_pad (float, optional): Espaçamento do rótulo da barra de cores.
        fig_width (float, optional): Largura da figura.
        fig_height (float, optional): Altura da figura.
        figure_dpi (int, optional): Resolução em tela.
        save_fig (bool, optional): Salva em disco.
        dpi (int, optional): Resolução de exportação.
        file_format (str, optional): Formato do arquivo exportado.
        filename (str, optional): Nome do arquivo.
        show_plot (bool, optional): Exibe a interface gráfica nativa.
        theme (str, optional): Aplica tema de cores ('dark' ou None).

    Returns:
        Figure: Objeto de figura do Matplotlib.
    """
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import numpy as np

    if theme == "dark":
        text_color = "#ABB2BF"
        edge_color = "#ABB2BF"
        if background_color == "white":
            background_color = "#242424"
    else:
        text_color = "black"
        edge_color = "black"

    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "text.color": text_color,
            "axes.labelcolor": text_color,
            "xtick.color": text_color,
            "ytick.color": text_color,
        }
    )

    fig, ax = plt.subplots(
        figsize=(fig_width, fig_height),
        dpi=figure_dpi,
        subplot_kw={"projection": "polar"},
    )
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    if z_matrix is not None:
        vmin = z_lim[0] if z_lim else None
        vmax = z_lim[1] if z_lim else None
        if z_scale == "log":
            norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
        else:
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

        mesh = ax.pcolormesh(
            theta_data, r_data, z_matrix, cmap=cmap, norm=norm, shading="auto"
        )

        if z_label:
            cbar = fig.colorbar(mesh, ax=ax, pad=0.1, fraction=0.046)
            cbar.set_label(z_label, fontsize=axis_fontsize, labelpad=label_pad)
            cbar.ax.yaxis.set_tick_params(color=text_color)
            plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color=text_color)

    if rings_inner is not None and rings_outer is not None:
        r_in_list = rings_inner if isinstance(rings_inner, list) else [rings_inner]
        r_out_list = rings_outer if isinstance(rings_outer, list) else [rings_outer]
        r_col_list = rings_colors if isinstance(rings_colors, list) else [rings_colors]
        r_alp_list = rings_alphas if isinstance(rings_alphas, list) else [rings_alphas]
        r_lab_list = rings_labels if isinstance(rings_labels, list) else [rings_labels]

        theta_fill = np.linspace(0, 2 * np.pi, 200)
        for i in range(len(r_in_list)):
            r_in = r_in_list[i]
            r_out = r_out_list[i]
            c = r_col_list[i % len(r_col_list)]
            a = r_alp_list[i % len(r_alp_list)]
            l = r_lab_list[i % len(r_lab_list)] if r_lab_list else None
            ax.fill_between(
                theta_fill, r_in, r_out, color=c, alpha=a, label=l, zorder=2
            )

    if scatter_r is not None and scatter_theta is not None:
        sr_list = scatter_r if isinstance(scatter_r, list) else [scatter_r]
        st_list = scatter_theta if isinstance(scatter_theta, list) else [scatter_theta]
        sc_list = (
            scatter_colors if isinstance(scatter_colors, list) else [scatter_colors]
        )
        sm_list = (
            scatter_markers if isinstance(scatter_markers, list) else [scatter_markers]
        )
        sz_list = scatter_sizes if isinstance(scatter_sizes, list) else [scatter_sizes]
        sl_list = (
            scatter_labels if isinstance(scatter_labels, list) else [scatter_labels]
        )

        for i in range(len(sr_list)):
            c = sc_list[i % len(sc_list)]
            m = sm_list[i % len(sm_list)]
            s = sz_list[i % len(sz_list)]
            l = sl_list[i % len(sl_list)] if sl_list else None
            ax.scatter(
                st_list[i], sr_list[i], color=c, marker=m, s=s, label=l, zorder=4
            )

    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=title_pad, fontweight="bold")

    ax.set_rlabel_position(45)
    ax.tick_params(axis="y", labelsize=axis_fontsize - 2, colors=text_color)
    ax.tick_params(axis="x", labelsize=axis_fontsize - 2, colors=text_color)

    if r_label:
        ax.set_ylabel(r_label, fontsize=axis_fontsize, color=text_color, labelpad=35)

    if r_scale == "log":
        ax.set_rscale("symlog")

    if r_lim is not None:
        ax.set_ylim(r_lim)

    if show_grid:
        ax.grid(
            True,
            linestyle=grid_linestyle,
            linewidth=grid_linewidth,
            color=grid_color,
            alpha=grid_alpha,
        )
        ax.set_axisbelow(True)

    if show_legend:
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            final_legend_fontsize = (
                legend_fontsize if legend_fontsize else axis_fontsize * 0.9
            )
            ax.legend(
                title=legend_title,
                frameon=legend_box,
                fontsize=final_legend_fontsize,
                title_fontsize=axis_fontsize,
                loc=legend_loc,
                edgecolor=edge_color if legend_box else None,
                bbox_to_anchor=(1.2, 1.1),
            )

    plt.tight_layout()

    if save_fig:
        filepath = f"figures/{filename}.{file_format}"
        import os

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor=background_color)

    if show_plot:
        plt.show()

    return fig


def magnetosphere(
    R_m,
    R_p=1.0,
    cme_factor=100.0,
    show_cme=True,
    x_range=None,
    y_range=None,
    grid_density=200,
    wind_velocity=1.0,
    title="Magnetospheric Standoff & Bow Shock",
    x_label=r"Distance [$R_{planet}$]",
    y_label=r"Distance [$R_{planet}$]",
    background_color="white",
    stream_color="#1f77b4",
    stream_density=1.5,
    stream_linewidth=1.2,
    stream_arrowsize=1.5,
    planet_color="black",
    planet_edgecolor="white",
    planet_linewidth=1.5,
    shield_color="red",
    shield_linestyle="-",
    shield_linewidth=2.0,
    shield_alpha=0.8,
    safe_zone_color="blue",
    safe_zone_alpha=0.1,
    cme_color="#E06C75",
    cme_linestyle=":",
    cme_linewidth=2.0,
    cme_alpha=0.9,
    show_grid=True,
    show_box=True,
    remove_borders=False,
    grid_color="#E6E6E6",
    grid_alpha=0.7,
    grid_linewidth=0.5,
    grid_linestyle="--",
    title_fontsize=16,
    axis_fontsize=12,
    title_pad=15,
    label_pad=8,
    fig_width=8,
    fig_height=6,
    figure_dpi=100,
    top_right_ticks=True,
    tick_direction="out",
    save_fig=False,
    dpi=300,
    file_format="png",
    filename="magnetosphere_graph",
    show_plot=True,
    theme=None,
):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    import matplotlib.colors as mcolors

    if theme == "dark":
        text_color = "#ABB2BF"
        edge_color = "#ABB2BF"
        if background_color == "white":
            background_color = "#242424"
        if stream_color == "#1f77b4":
            stream_color = "#61AFEF"
        if shield_color == "red":
            shield_color = "#00D8FF"
        if safe_zone_color == "blue":
            safe_zone_color = "#00D8FF"
        if planet_color == "black":
            planet_color = "#1E1E1E"
    else:
        text_color = "black"
        edge_color = "black"

    # Aplica transparência elegante diretamente aos vetores de fluxo do vento (30% opacidade)
    stream_rgba = mcolors.to_rgba(stream_color, alpha=0.3)

    plt.rcParams.update(
        {
            "font.family": "serif",
            "mathtext.fontset": "dejavuserif",
            "axes.linewidth": 1.2,
            "xtick.direction": tick_direction,
            "ytick.direction": tick_direction,
            "xtick.top": top_right_ticks,
            "ytick.right": top_right_ticks,
            "xtick.labelsize": axis_fontsize - 2,
            "ytick.labelsize": axis_fontsize - 2,
            "text.color": text_color,
            "axes.labelcolor": text_color,
            "xtick.color": text_color,
            "ytick.color": text_color,
        }
    )

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=figure_dpi)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    x_min = x_range[0] if x_range else -R_m * 2.5
    x_max = x_range[1] if x_range else R_m * 3.5
    y_min = y_range[0] if y_range else -R_m * 3.0
    y_max = y_range[1] if y_range else R_m * 3.0

    # ? --- Malha Espacial e Solução Analítica da Gota ---
    x = np.linspace(x_min, x_max, grid_density)
    y = np.linspace(y_min, y_max, grid_density)
    X, Y = np.meshgrid(x, y)

    Theta_mesh = np.arctan2(np.abs(Y), -X)
    Theta_mesh = np.where(Theta_mesh == 0, 1e-10, Theta_mesh)

    R_boundary = R_m * np.sqrt(Theta_mesh / np.sin(Theta_mesh))
    R_mesh = np.sqrt(X**2 + Y**2)
    inside = R_mesh <= R_boundary

    # ? --- Campo de Escoamento Estelar ---
    r_sq = X**2 + Y**2
    r_sq[r_sq == 0] = 1e-10

    U = wind_velocity * (1 + R_m * X / r_sq)
    V_flow = wind_velocity * (R_m * Y / r_sq)

    U[inside] = np.nan
    V_flow[inside] = np.nan

    ax.streamplot(
        X, Y, U, V_flow,
        color=stream_rgba,
        density=stream_density,
        linewidth=stream_linewidth,
        arrowsize=stream_arrowsize,
    )

    # ? --- Máscaras Ocultas e Traçado Principal ---
    theta_line = np.linspace(1e-4, np.pi - 1e-4, 1000)
    r_line = R_m * np.sqrt(theta_line / np.sin(theta_line))
    x_line_top = -r_line * np.cos(theta_line)
    y_line_top = r_line * np.sin(theta_line)

    # Corta a linha na extremidade da tela para não quebrar a geometria do preenchimento
    valid_top = (x_line_top <= x_max * 1.2)
    x_top_crop = x_line_top[valid_top]
    y_top_crop = y_line_top[valid_top]

    x_poly = np.concatenate([[x_max * 1.2], x_top_crop[::-1], x_top_crop, [x_max * 1.2]])
    y_poly = np.concatenate([[-y_top_crop[-1]], -y_top_crop[::-1], y_top_crop, [y_top_crop[-1]]])

    # O SEGREDO DA CAUDA LÍMPIDA: Preenche o fundo com cor sólida para "apagar" o vento que cruzou as malhas!
    ax.fill(x_poly, y_poly, color=background_color, alpha=1.0, zorder=2)
    
    # Aplica o tom de escudo (azul) por cima
    ax.fill(x_poly, y_poly, color=safe_zone_color, alpha=safe_zone_alpha, zorder=3)

    # Traço da fronteira visível
    x_line = np.concatenate([x_line_top[::-1], x_line_top])
    y_line = np.concatenate([-y_line_top[::-1], y_line_top])
    valid_plot = (x_line >= x_min) & (x_line <= x_max) & (y_line >= y_min) & (y_line <= y_max)

    ax.plot(
        x_line[valid_plot], y_line[valid_plot],
        color=shield_color, linestyle=shield_linestyle,
        linewidth=shield_linewidth, alpha=shield_alpha, zorder=4,
    )

    # ? --- Traçado do Evento de CME ---
    if show_cme:
        R_m_cme = R_m * (cme_factor ** (-1/6))
        r_cme = R_m_cme * np.sqrt(theta_line / np.sin(theta_line))
        x_cme_top = -r_cme * np.cos(theta_line)
        y_cme_top = r_cme * np.sin(theta_line)

        x_cme = np.concatenate([x_cme_top[::-1], x_cme_top])
        y_cme = np.concatenate([-y_cme_top[::-1], y_cme_top])
        valid_cme = (x_cme >= x_min) & (x_cme <= x_max) & (y_cme >= y_min) & (y_cme <= y_max)

        ax.plot(
            x_cme[valid_cme], y_cme[valid_cme],
            color=cme_color, linestyle=cme_linestyle,
            linewidth=cme_linewidth, alpha=cme_alpha, zorder=5,
        )
        
        valid_cme_top = (x_cme_top <= x_max * 1.2)
        x_cme_top_crop = x_cme_top[valid_cme_top]
        y_cme_top_crop = y_cme_top[valid_cme_top]
        
        x_poly_cme = np.concatenate([[x_max * 1.2], x_cme_top_crop[::-1], x_cme_top_crop, [x_max * 1.2]])
        y_poly_cme = np.concatenate([[-y_cme_top_crop[-1]], -y_cme_top_crop[::-1], y_cme_top_crop, [y_cme_top_crop[-1]]])
        ax.fill(x_poly_cme, y_poly_cme, color=cme_color, alpha=0.05, zorder=4)

    # ? --- Planeta Central ---
    planet = Circle((0, 0), R_p, color=planet_color, ec=planet_edgecolor, lw=planet_linewidth, zorder=6)
    ax.add_patch(planet)

    if title:
        ax.set_title(title, fontsize=title_fontsize, pad=title_pad, fontweight="bold")

    ax.set_xlabel(x_label, fontsize=axis_fontsize, labelpad=label_pad)
    ax.set_ylabel(y_label, fontsize=axis_fontsize, labelpad=label_pad)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    if show_grid:
        ax.grid(True, linestyle=grid_linestyle, linewidth=grid_linewidth, color=grid_color, alpha=grid_alpha, zorder=1)
        ax.set_axisbelow(True)

    if not show_box:
        ax.set_frame_on(False)
    elif remove_borders:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)
        ax.spines["bottom"].set_color(edge_color)
        ax.spines["left"].set_color(edge_color)
    else:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(edge_color)

    plt.tight_layout()

    if save_fig:
        import os
        filepath = f"figures/{filename}.{file_format}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight", facecolor=background_color)

    if show_plot:
        plt.show()

    return fig