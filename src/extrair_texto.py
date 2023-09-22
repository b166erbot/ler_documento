from itertools import chain
from pathlib import Path
from re import split, sub
from typing import Optional, Union

from PyPDF4 import PdfFileReader

from src.processar_texto import configurar_nlp, processar

lista_substituir = [
    (r'Œ', '-'),
    # deixe esta linha abaixo nessa sequência e por último.
    (r'\n-\n', ''), (r'-\n', ''),
    (r'[\n\r\t\f\v]+ +', ' '), (r' {2,}', ' ')
]


def tratar_texto(
    textos_nao_tratado: list[list[int, str]]
) -> list[list[int, list[str]]]:
    """Retorna o texto tratado por regex e spacy."""
    textos = []
    for número, texto in textos_nao_tratado:
        for padrao, substituto in lista_substituir:
            texto = sub(padrao, substituto, texto)
        sentenças = list(processar(texto))
        sentenças = list(filter(lambda sentença: bool(sentença), sentenças))
        if bool(sentenças):
            textos.append([número, sentenças])
    return textos


def extrair_texto(local: Path) -> list[list[int, list[str]]]:
    """Retorna texto de um arquivo de texto comum."""
    with open(local) as arquivo:
        texto = arquivo.read()
    texto = tratar_texto([[0, texto]])
    return texto


def extrair_texto_pdf(
    local: Path
) -> list[list[int, list[str]]]:
    """Retorna textos de um arquivo pdf."""
    # tudo precisa ser feito no contexto do with. Se o arquivo fecha, dá erro.
    with open(local, 'rb') as arquivo:
        leitor_pdf = PdfFileReader(arquivo)
        número_páginas = leitor_pdf.numPages
        iterador = range(leitor_pdf.numPages)
        # extrai os textos, filtra pegando somente os que tem texto.
        textos = list(map(
            lambda número: [
                número, leitor_pdf.getPage(número).extractText().strip()
            ],
            iterador
        ))
    textos = tratar_texto(textos)
    return textos


extensoes_e_funcoes = {
    '.pdf': extrair_texto_pdf, '.txt': extrair_texto,
    '': extrair_texto
}


def extrair(
    local: Path, lingua_spacy: str
) -> list[int, list[str]]:
    """Retorna textos de um arquivo."""
    configurar_nlp(lingua_spacy)
    textos = extensoes_e_funcoes[local.suffix](local)
    return textos