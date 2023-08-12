import shelve
from json import dump, load
from pathlib import Path
from typing import Optional, Union

from pynput.keyboard import Key

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
        return banco[hash_do_arquivo]


def verificar_arquivo_shelve(nome_do_arquivo: Path) -> bool:
    """Verifica se o arquivo já foi processado e salvo no shelve."""
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with shelve.open(local_arquivo_shelve) as banco:
        return bool(hash_do_arquivo in banco)
# ----- / -----


# ----- config.json -----
teclas_dicionario = {
    'voltar': ['ctrl', ','],
    'avancar': ['ctrl', '.'],
    'voltar_pagina': ['alt', ','],
    'avancar_pagina': ['alt', '.'],
    'sair': ['ctrl', ';']
}
local_arquivo_config = Path('config.json')


def carregar_config_teclado() -> list[str]:
    chaves = list(map(lambda chave: chave.name, Key))
    # Não altere a ordem das chaves, os valores não importa a ordem
    # nem o conteúdo.
    with open(local_arquivo_config) as arquivo:
        config = load(arquivo)
    # Estou sem criatividade para criar nome de variável.
    retorno = []
    for teclas_atalho in config['teclas_atalho'].values():
        retorno.append(
            '+'.join(map(
                lambda chave: f"<{chave}>" if chave in chaves else chave,
                teclas_atalho
            ))
        )
    return retorno


def carregar_config_falas() -> list[str]:
    with open(local_arquivo_config) as arquivo:
        config = load(arquivo)
    return config


def criar_config() -> None:
    config = dict()
    config['teclas_atalho'] = teclas_dicionario
    with open(local_arquivo_config, 'w') as arquivo:
        dump(config, arquivo, indent = 4)
# ----- / -----


# ----- progresso.json -----
local_arquivo_progresso = Path('progresso.json')


def salvar_progresso(nome_do_arquivo: Path, progresso: list[int]) -> None:
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with open(local_arquivo_progresso) as arquivo:
        configuração = load(arquivo)
    configuração[hash_do_arquivo] = progresso
    with open(local_arquivo_progresso, 'w') as arquivo:
        dump(configuração, arquivo)


def carregar_progresso(nome_do_arquivo: Path) -> Optional[dict[str, list[int]]]:
    hash_do_arquivo = hashear_arquivo(nome_do_arquivo)
    with open(local_arquivo_progresso) as arquivo:
        configuração = load(arquivo)
    return configuração.get(hash_do_arquivo)
# ----- / -----


def existe_arquivo(local_arquivo: Path) -> bool:
    return all([local_arquivo.is_file(), local_arquivo.exists()])