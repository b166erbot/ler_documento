"""Módulo feito para corrigir import circular."""

# Este módulo não deveria existir mais. Refatorar depois.


from argparse import Namespace
from pathlib import Path

from src.extrair_texto import extrair
from src.salvar import carregar_progresso, existe_arquivo, obter_texto, salvar
from src.utils import (ContagensFinitas, Porcento, Temporizador,
                       tratar_paginas_usuario)

argumentos: Namespace
textos: list[list[str]]
nome_arquivo: Path
contagens: ContagensFinitas
porcentagem: Porcento


def injetar_argumentos(argumentos_: Namespace) -> None:
    """Injeta argumentos para este módulo para ser importado posteriormente."""
    global argumentos, textos, nome_arquivo, contagens, porcentagem
    argumentos = argumentos_
    nome_arquivo = Path(argumentos.arquivo.strip()).expanduser().absolute()
    textos_ = obter_texto(nome_arquivo)
    condições_if = [
        argumentos.forcar_salvamento, textos_ == None
    ]
    if any(condições_if):
        textos = extrair(
            nome_arquivo, argumentos.lingua_spacy, argumentos.paginas
        )
        salvar(textos, nome_arquivo)
    else:
        textos = textos_
    if argumentos.paginas != None:
        paginas = tratar_paginas_usuario(argumentos.paginas)
        textos = list(filter(
            lambda numero_texto: (numero_texto[0] + 1) in paginas,
            textos
        ))
    contagens = ContagensFinitas(
        ((numero, 0, len(sentenças) - 1) for numero, sentenças in textos),
        nome_arquivo
    )
    condições_if = [
        not existe_arquivo(Path('progresso.pkl')),
        argumentos.zerar_progresso, argumentos.paginas != None
    ]
    if any(condições_if):
        contagens.definir_progresso([0, 0])
        porcentagem = Porcento(contagens.numero_maximo, 0)
    else:
        progresso = carregar_progresso(nome_arquivo)
        if all([progresso != None, not argumentos.forcar_salvamento]):
            # decidi que não vou colocar o progresso no init do contagens.
            contagens.definir_progresso(progresso)
        porcentagem = Porcento(contagens.numero_maximo, contagens.numero_atual_)
        if porcentagem.finalizou:
            contagens.definir_progresso([0, 0])
            porcentagem = Porcento(contagens.numero_maximo, 0)


def retornar_contagens_porcento() -> list[ContagensFinitas, Porcento]:
    """Retorna as contagens e porcento."""
    return [contagens, porcentagem]


def retornar_textos_argumentos() -> list[list[str]]:
    """Retorna os textos e argumentos."""
    return [textos, argumentos]
