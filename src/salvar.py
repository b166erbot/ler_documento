import shelve
from json import dump, load
from pathlib import Path
from typing import Optional, Union

from src.hash import hashear_arquivo

listas_textos = Union[list[list[str]], list[str]]


# ----- shelve -----
local_arquivo_shelve = Path('textos_dos_arquivos.pkl')


def salvar(
    textos: list[list[str]], nome_do_arquivo: Path
) -> None:
    """Salva o texto em um arquivo pkl."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with shelve.open(local_arquivo_shelve) as banco:
        banco[hash_do_arquivo] = textos


def obter_texto(nome_do_arquivo: Path) -> listas_textos:
    """Retorna o conteúdo de um arquivo de texto previamente salvo."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with shelve.open(local_arquivo_shelve) as banco:
        return banco.get(hash_do_arquivo)


def verificar_arquivo_shelve(nome_do_arquivo: Path) -> bool:
    """Verifica se o arquivo já foi processado e salvo no shelve."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with shelve.open(local_arquivo_shelve) as banco:
        return hash_do_arquivo in banco
# ----- / -----


# ----- progresso.json -----
local_arquivo_progresso = Path('progresso.json')


def salvar_progresso(nome_do_arquivo: Path, progresso: list[int]) -> None:
    """Salva o progresso do usuário."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    if existe_arquivo(local_arquivo_progresso):
        with open(local_arquivo_progresso) as arquivo:
            configuração = load(arquivo)
    else:
        configuração = dict()
    configuração[hash_do_arquivo] = progresso
    with open(local_arquivo_progresso, 'w') as arquivo:
        dump(configuração, arquivo)


def carregar_progresso(nome_do_arquivo: Path) -> Optional[dict[str, list[int]]]:
    """Carrega o progresso do usuário."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with open(local_arquivo_progresso) as arquivo:
        configuração = load(arquivo)
    return configuração.get(hash_do_arquivo)
# ----- / -----


def existe_arquivo(local_arquivo: Path) -> bool:
    """Verifica se o arquivo existe."""
    return all([local_arquivo.is_file(), local_arquivo.exists()])