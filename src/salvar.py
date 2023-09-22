import shelve
from pathlib import Path
from typing import Optional, Union

from src.hash import hashear_arquivo

listas_textos = Union[list[list[str]], list[str]]


# ---------// shelve textos //---------
def salvar(
    textos: list[list[str]], nome_do_arquivo: Path
) -> None:
    """Salva o texto em um arquivo pkl."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    pasta = Path('arquivos')
    if all([pasta.exists(), not pasta.is_dir()]):
        texto_erro = (
            "Existe algum arquivo/link com o mesmo nome do diretório 'arquivos'"
            ". Mova ou renomeie esse arquivo/link."
        )
        raise IsADirectoryError(texto_erro)
    elif not all([pasta.exists(), pasta.is_dir()]):
        pasta.mkdir()
    local_do_arquivo = pasta / Path(f"{hash_do_arquivo}.pkl")
    with shelve.open(local_do_arquivo) as banco:
        banco[hash_do_arquivo] = textos


def obter_texto(nome_do_arquivo: Path) -> Optional[listas_textos]:
    """Retorna o conteúdo de um arquivo de texto previamente salvo."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    pasta = Path('arquivos')
    local_do_arquivo = pasta / Path(f"{hash_do_arquivo}.pkl")
    if all([local_do_arquivo.exists(), local_do_arquivo.is_file()]):
        with shelve.open(local_do_arquivo) as banco:
            return banco.get(hash_do_arquivo)


# ---------// shelve progresso //---------
local_arquivo_progresso = Path('progresso.pkl')


def salvar_progresso(nome_do_arquivo: Path, progresso: list[int]) -> None:
    """Salva o progresso do usuário."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with shelve.open(local_arquivo_progresso) as banco:
        banco[hash_do_arquivo] = progresso


def carregar_progresso(nome_do_arquivo: Path) -> Optional[list[int]]:
    """Carrega o progresso do usuário."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with shelve.open(local_arquivo_progresso) as banco:
        return banco.get(hash_do_arquivo)


# ---------// funções extras //---------
def existe_arquivo(local_arquivo: Path) -> bool:
    """Verifica se o arquivo existe."""
    return all([local_arquivo.is_file(), local_arquivo.exists()])