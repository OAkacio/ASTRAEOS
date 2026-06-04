import os

BLUE = "\033[94m"
CYAN = "\033[96m"
GOLD = "\033[33m"
GRAY = "\033[90m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
LIGHTGREEN = "\033[92m"


def header(title, width=80, flush=False, **kwargs):
    """
    Gera um cabeçalho para início de código apresentando um título principal e um conjunto de "N" informações adicionais no formato de "CHAVE 1: VALOR 1 | CHAVE 2: VALOR 2 | ...".

    Args:
        title (str): O texto principal a ser exibido no centro do cabeçalho.
        width (int, optional): A largura total da moldura. Default é 80.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.
        **kwargs: Informações adicionais exibidas abaixo do título, formatadas como 'CHAVE: VALOR'.

    Returns:
        None

    Exemplo de Aplicação:
        >>> sy.header("Meu Código v2.1.0", width=80, autor="Victor", Prâmetro="25.02")
    """

    TL, TR = "╔", "╗"
    BL, BR = "╚", "╝"
    HL, VL = "═", "║"
    DIV_L, DIV_R = "╠", "╣"
    formatted_title = f" {title.upper()} "
    inner_space = width - 2
    print("\n" * 2, flush=flush)
    print(f"{GRAY}{TL}{HL * inner_space}{TR}{RESET}", flush=flush)
    print(
        f"{GRAY}{VL}{RESET}{BOLD}{GOLD}{formatted_title:^{inner_space}}{RESET}{GRAY}{VL}{RESET}",
        flush=flush
    )
    if kwargs:
        print(f"{GRAY}{DIV_L}{HL * inner_space}{DIV_R}{RESET}", flush=flush)
        info_str = "  |  ".join([f"{k.upper()}: {v}" for k, v in kwargs.items()])
        print(
            f"{GRAY}{VL}{RESET}{CYAN}{info_str:^{inner_space}}{RESET}{GRAY}{VL}{RESET}",
            flush=flush
        )
    print(f"{GRAY}{BL}{HL * inner_space}{BR}{RESET}", flush=flush)
    print("\n", flush=flush)


def status(message, flush=False):
    """
    Exibe uma mensagem de status formatada no terminal.

    Args:
        message (str): O texto descritivo do status ou evento atual a ser exibido.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.status("Calculando distâncias cosmológicas...")
    """

    print(f"\n  {BLUE}{BOLD}»{RESET} {message}", flush=flush)


def param(*items, indent=6, flush=False):
    """
    Exibe múltiplos parâmetros com alinhamento vertical e indicaçãod e "Nome", "Valor", "Unidade".

    Args:
        *items (tuple): Sequências contendo (nome, valor, [unidade]).
        indent (int, optional): O número de espaços iniciais para o recuo no terminal. Default é 6.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.param(("Velocidade Inicial", 300, "km/s"), ("Densidade", 1e5, "cm^-3"), ...)
    """
    if not items:
        return
    processed = []
    for item in items:
        name = str(item[0])
        val = str(item[1])
        unit = str(item[2]) if len(item) > 2 else ""
        processed.append((name, val, unit))
    name_width = max(len(p[0]) for p in processed)
    val_width = max(len(p[1]) for p in processed)
    spacing = " " * indent
    for n, v, u in processed:
        name_fmt = f"{BOLD}{n.ljust(name_width)}{RESET}"
        separator = f"{GRAY}={RESET}"
        val_fmt = f"{CYAN}{v.rjust(val_width)}{RESET}"
        unit_fmt = f" {GRAY}[{u}]{RESET}" if u else ""
        print(f"{spacing}{name_fmt} {separator} {val_fmt}{unit_fmt}", flush=flush)


def space(height=3, flush=False):
    """
    Insere um distanciamento vertical no terminal.

    Args:
        height (int, optional): O número de quebras de linha a serem impressas. Default é 3.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.space(height=2)
    """
    print("\n" * height, flush=flush)


def table(*axes, mode="column", flush=False, **kwargs):
    """
    Formata e exibe dados de forma simplificada tanto para alinhamento de colunas ou linhas em uma estrutura de tabela ASCII.

    Args:
        *axes (tuple): Tuplas contendo os dados.
        mode (str, optional): Define se as tuplas representam 'column' (coluna) ou 'row' (linha). Default é 'column'.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.
        **kwargs: Permite passar os eixos de forma nomeada.

    Returns:
        None

    Exemplo:
        >>> sy.table(("ID", 1, 2), ("NOME", "Estrela A", "Estrela B"), mode="column")
    """
    inputs = list(axes) + list(kwargs.values())
    if not inputs:
        print("A lista está vazia.", flush=flush)
        return
    data = []
    if mode == "column":
        keys = [str(axis[0]) for axis in inputs]
        row_values = zip(*[axis[1:] for axis in inputs])
        for values in row_values:
            data.append(dict(zip(keys, values)))
    elif mode == "row":
        keys = [str(c) for c in inputs[0]]
        row_lines = inputs[1:]
        for values in row_lines:
            data.append(dict(zip(keys, values)))
    else:
        print(f"Tipo '{mode}' inválido. Use mode='column' ou mode='row'.", flush=flush)
        return
    if not data:
        print("A lista está vazia.", flush=flush)
        return
    columns = list(data[0].keys())
    widths = {}
    for col in columns:
        max_val_len = max([len(str(item[col])) for item in data])
        widths[col] = max(max_val_len, len(col))
    horizontal_separator = (
        "+" + "+".join(["-" * (widths[c] + 2) for c in columns]) + "+"
    )
    print(horizontal_separator, flush=flush)
    header_str = "|"
    for c in columns:
        header_str += f" {BOLD}{CYAN}{c.upper().center(widths[c])}{RESET} |"
    print(header_str, flush=flush)
    print(horizontal_separator, flush=flush)
    for item in data:
        line_str = "|"
        for c in columns:
            val = str(item[c])
            if val.replace(".", "", 1).isdigit():
                line_str += f" {val.rjust(widths[c])} |"
            else:
                line_str += f" {val.ljust(widths[c])} |"
        print(line_str, flush=flush)
    print(horizontal_separator, flush=flush)


def cin(message, expected_type="string", flush=False):
    """
    Recebe e valida ("int", "float", "string") a entrada do usuário com um visual amigável no terminal.

    Args:
        message (str): A mensagem ou pergunta a ser exibida para o usuário.
        expected_type (str, optional): Tipo de dado ('int', 'float' ou 'string'). Default é 'string'.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        any: O valor inserido pelo usuário convertido para o tipo especificado.

    Exemplo:
        >>> limite_max = sy.cin("Insira o limite superior da integração", expected_type="float")
    """

    question_mark = f"{GOLD}{BOLD}?{RESET}"
    error_mark = f"{RED}{BOLD}!{RESET}"
    cursor = f"{CYAN}»{RESET}"
    while True:
        prompt = (
            f"\n  {question_mark} {message} {GRAY}[{expected_type}]{RESET} {cursor} "
        )
        user_input = input(prompt)
        try:
            if expected_type.lower() == "int":
                return int(user_input)
            elif expected_type.lower() == "float":
                return float(user_input.replace(",", "."))
            elif expected_type.lower() == "string":
                return str(user_input)
            else:
                print(
                    f"\n  {error_mark} {GRAY}Erro: Formato '{expected_type}' não reconhecido. Use 'int', 'float' ou 'string'.{RESET}",
                    flush=flush
                )
                return None
        except ValueError:
            print(
                f"  {error_mark} {GRAY}Entrada inválida. Insira um valor numérico do tipo '{expected_type}'.{RESET}",
                flush=flush
            )


def ok(messages, is_ok=True, flush=False):
    """
    Exibe uma confirmação visual estilizada de sucesso ou falha no terminal.

    Args:
        messages (str ou list): Mensagem única ou lista de mensagens a serem exibidas.
        is_ok (bool, optional): Se True, exibe a tag [OK] em ciano. Se False, exibe [NOK] em vermelho. Default é True.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.ok("Matriz de densidade carregada")
        >>> sy.ok(["Arquivo corrompido", "Dados em branco"], is_ok=False)
    """

    if is_ok:
        status_tag = f"{LIGHTGREEN}[OK]{RESET}"
    else:
        status_tag = f"{RED}[NOK]{RESET}"

    prefix = f"            {BLUE}{BOLD}»{RESET} {status_tag}  "
    if isinstance(messages, str):
        messages = [messages]
    for item in messages:
        print(f"{prefix} {item}", flush=flush)


def fim(message="EXECUÇÃO FINALIZADA!", flush=False):
    """
    Imprime uma mensagem visual de finalização de script no terminal.

    Args:
        message (str): Mensagem a ser devolvida ao usuário indicando a finalização do script. Default é "EXECUÇÃO FINALIZADA!"
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.fim()
    """
    simb = "=" * 40
    print(f"\n     {BLUE}{simb}{RESET} {message} {BLUE}{simb}{RESET}\n", flush=flush)


def help(filepath, flush=False):
    """
    Lê e exibe um arquivo de texto no terminal utilizando uma paleta de cores minimalista (stealth).

    Args:
        filepath (str): Caminho para o arquivo de texto contendo a tabela ASCII.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.help("data/instrucoes.txt")
    """
    if not os.path.exists(filepath):
        print(
            f"\n  {RED}{BOLD}!{RESET} {GRAY}Arquivo de ajuda '{filepath}' não encontrado.{RESET}",
            flush=flush
        )
        return
    print(flush=flush)
    with open(filepath, "r", encoding="utf-8-sig") as file:
        for line in file:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("+"):
                print(f"  {GRAY}{line}{RESET}", flush=flush)
            elif line.startswith("|"):
                formatted_line = line.replace("|", f"{RESET}{GRAY}|{RESET}{DIM}")
                print(f"  {DIM}{formatted_line}{RESET}", flush=flush)
            else:
                print(f"  {GRAY}{DIM}{line}{RESET}", flush=flush)
    print(flush=flush)


def hidestatus(message, NSpaces=10, flush=False):
    """
    Lê e exibe um arquivo de texto no terminal utilizando uma paleta de cores apagadas/secundárias.
    Args:
        filepath (str): Caminho para o arquivo de texto contendo a tabela ASCII.
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.
    Returns:
        None
    Exemplo:
        >>> sy.help("data/instrucoes.txt")
    """
    rec = " " * NSpaces
    print(f"{rec}{GRAY}{DIM}{message}{RESET}", flush=flush)


def structurelog(message, index="", label="", color="blue", flush=False):
    """
    Exibe uma mensagem de status estruturada no terminal podendo ser estilizada com coloração, index e labels.

    Args:
        message (str): O texto descritivo principal do status ou evento atual a ser exibido.
        index (str): O pré-texto secundário descritivo a ser exibido antes do texto principal.
        label (str): O pós-texto primário descritivo a ser exibido antes do texto principal.
        color (str): A cor a ser exibida. Pode ser "blue", "cyan", "gold", "gray", "red", "lightgreen", "dim", "bold" ,"reset".
        flush (bool, optional): Se True, a saída do buffer será forçada. Default é False.

    Returns:
        None

    Exemplo:
        >>> sy.status(message="Calculando distâncias cosmológicas...", index="'01:15:03'", label="STATUS", color="blue")
    """
    blue = "\033[94m"
    cyan = "\033[96m"
    gold = "\033[33m"
    gray = "\033[90m"
    red = "\033[91m"
    bold = "\033[1m"
    dim = "\033[2m"
    reset = "\033[0m"
    lightgreen = "\033[92m"
    label = label.upper()

    if color == "blue":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {BLUE} {message} {RESET}", flush=flush)
    elif color == "cyan":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {CYAN} {message} {RESET}", flush=flush)
    elif color == "gold":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {GOLD} {message} {RESET}", flush=flush)
    elif color == "gray":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {GRAY} {message} {RESET}", flush=flush)
    elif color == "red":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {RED} {message} {RESET}", flush=flush)
    elif color == "lightgreen":
        print(
            f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {LIGHTGREEN} {message} {RESET}",
            flush=flush
        )
    elif color == "dim":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {DIM} {message} {RESET}", flush=flush)
    elif color == "reset":
        print(
            f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {RESET} {message} {RESET}",
            flush=flush
        )
    elif color == "bold":
        print(f"\n  {GRAY}{BOLD}» {index} {RESET} | {label} | {BOLD} {message} {RESET}", flush=flush)