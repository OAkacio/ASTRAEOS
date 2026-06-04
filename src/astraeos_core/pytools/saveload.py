#
# * =============================================================================
# * SAVE LOAD
# * =============================================================================

# ? --- Bibiliotecas do Projeto ---
import os


def savetable(
    filename,
    data_matrix,
    is_vertical=True,
    header=None,
    separator="\t",
    directory="data",
):
    """
    Salva uma matriz de dados em um arquivo de texto dentro do diretório especificado.

    Args:
        filename (str): Nome do arquivo a ser salvo (sem a extensão .txt).
        data_matrix (list ou tuple): Matriz de dados (1D ou 2D) a ser salva.
        is_vertical (bool, optional): Se True, transpõe a matriz antes de salvar (salva em colunas). Default é True.
        header (str ou list, optional): Cabeçalho a ser inserido no topo do arquivo. Default é None.
        separator (str, optional): Caractere separador entre os dados. Default é "\\t" (tabulação).
        directory (str, optional): Diretório onde o arquivo será salvo. Default é "data".

    Returns:
        None

    Exemplo:
        >>> tempos = [0.1, 0.2, 0.3]
        >>> densidades = [1e4, 1.2e4, 1.5e4]
        >>> sy.savetable("resultados_densidade", [tempos, densidades], header="Tempo(s)\\tDensidade(cm^-3)")
    """
    folder = directory
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, f"{filename}.txt")
    if data_matrix and not isinstance(data_matrix[0], (list, tuple)):
        data_matrix = [data_matrix]
    data_to_save = zip(*data_matrix) if is_vertical else data_matrix
    with open(filepath, "w", encoding="utf-8") as file:
        if header:
            header_lines = header.split("\n") if isinstance(header, str) else header
            for h_line in header_lines:
                file.write(f"# {h_line}\n")
        for row in data_to_save:
            row_string = separator.join(map(str, row))
            file.write(row_string + "\n")


def loadtable(filepath, is_vertical=True, separator="\t"):
    """
    Lê um arquivo de texto e o converte em uma matriz de dados, ignorando comentários.

    Args:
        filepath (str): Caminho completo (ou relativo) do arquivo a ser lido, incluindo extensão.
        is_vertical (bool, optional): Se True, transpõe a matriz lida (retorna colunas como listas). Default é True.
        separator (str, optional): Caractere separador utilizado no arquivo. Default é "\\t".

    Returns:
        list: Matriz contendo os dados lidos. Retorna None se o arquivo não for encontrado.

    Exemplo:
        >>> dados = sy.loadtable("data/resultados_densidade.txt")
        >>> tempos = dados[0]
        >>> densidades = dados[1]
    """
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return None
    read_matrix = []
    with open(filepath, "r", encoding="utf-8-sig") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            values = []
            for item in line.split(separator):
                item = item.strip()
                try:
                    values.append(float(item))
                except ValueError:
                    values.append(item)
            read_matrix.append(values)
    if is_vertical and read_matrix:
        read_matrix = [list(column) for column in zip(*read_matrix)]
    return read_matrix


def identificadora(filepath):
    """
    Identifica automaticamente o caractere separador mais provável de um arquivo de texto de dados.

    Args:
        filepath (str): Caminho completo do arquivo a ser analisado.

    Returns:
        str: O separador identificado ("\\t", ",", ";" ou " "). Retorna "\\t" como fallback.

    Exemplo:
        >>> sep_correto = sy.identificadora("data/meus_dados.csv")
        >>> print(repr(sep_correto))
        ','
    """
    if not os.path.exists(filepath):
        return None
    candidates = ["\t", ",", ";", " "]
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            counts = {sep: line.count(sep) for sep in candidates}
            best_separator = max(counts, key=counts.get)
            return best_separator if counts[best_separator] > 0 else "\t"
    return "\t"


def ler_cabecalho(filepath):
    """
    Lê exclusivamente o cabeçalho (linhas iniciadas por '#') de um arquivo no diretório 'data/'.
    Args:
        filepath (str): Caminho completo do arquivo a ser analisado.
    Returns:
        list: Lista de strings contendo as linhas do cabeçalho. Retorna None se não encontrar o arquivo.
    Exemplo:
        >>> headers = sy.ler_cabecalho("dados/resultados_densidade.txt")
        >>> print(headers)
        ['Tempo(s)\\tDensidade(cm^-3)']
    """
    if not os.path.exists(filepath):
        return None
    header_lines = []
    with open(filepath, "r", encoding="utf-8-sig") as file:
        for line in file:
            if line.startswith("#"):
                header_lines.append(line.replace("#", "").strip())
            else:
                break
    return header_lines


def havefile(filepath):
    """
    Verifica se um arquivo ou diretório existe no caminho especificado.

    Args:
        filepath (str): Caminho completo para o arquivo ou diretório.

    Returns:
        bool: True se o caminho existir, False caso contrário.

    Exemplo:
        >>> existe = sy.havefile("data/resultados_densidade.txt")
        >>> if existe:
        ...     print("O arquivo está disponível para leitura.")
    """
    return os.path.exists(filepath)


def createfile(filepath):
    """
    Cria um novo arquivo no caminho completo especificado.

    Args:
        filepath (str): Caminho completo para o novo arquivo.

    Returns:
        None

    Exemplo:
        >>> sy.createfile("data/novo_diretório")
    """
    os.mkdir(filepath)
