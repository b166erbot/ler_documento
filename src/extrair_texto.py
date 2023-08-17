from itertools import chain
from pathlib import Path
from re import split, sub
from typing import Optional, Union

from PyPDF4 import PdfFileReader

from src.processar_texto import configurar_nlp, processar
from src.utils import recortar, tratar_paginas_usuario

lista_strings_opcional = list[Optional[str], Optional[list[str]]]


lista_substituir = [
    (r'Œ', '-'), (r'\n-\n', ''),
    # deixe esta linha abaixo nessa sequência e por último.
    (r'[\n\r\t\v\f]+', ' '), (r' {2,}', ' ')
]


def tratar_texto(
    textos_nao_tratado: list[list[int, str]]
) -> list[list[int, list[str]]]:
    """Retorna o texto tratado por regex e spacy."""
    textos = []
    for numero, texto in textos_nao_tratado:
        for padrao, substituto in lista_substituir:
            texto = sub(padrao, substituto, texto)
        sentenças = list(processar(texto))
        sentenças = list(filter(lambda sentença: bool(sentença), sentenças))
        textos.append([numero, sentenças])
    return textos


def extrair_texto(local: Path, *args, **kwargs) -> list[list[int, list[str]]]:
    """Retorna texto de um arquivo de texto comum."""
    with open(local) as arquivo:
        texto = arquivo.read()
    # Primeira lista abaixo é para dizer que é uma lista de textos.
    # A segunda lista abaixo é para dizer que está numerada e tem textos.
    texto = tratar_texto([[0, texto]])
    return texto


def extrair_texto_pdf(
    local: Path, pagina: Optional[int] = None
) -> list[list[int, list[str]]]:
    """Retorna textos de um arquivo pdf."""
    # tudo precisa ser feito no contexto do with. Se o arquivo fecha, dá erro.
    with open(local, 'rb') as arquivo:
        leitor_pdf = PdfFileReader(arquivo)
        numero_paginas = leitor_pdf.numPages
        iterador = range(leitor_pdf.numPages) if pagina is None else [pagina]
        # extrai os textos, filtra pegando somente os que tem texto.
        textos = list(map(
            lambda numero: [
                numero, leitor_pdf.getPage(numero).extractText().strip()
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
    local: Path, lingua_spacy: str, paginas: str = None
) -> list[int, list[str]]:
    """Retorna textos de um arquivo."""
    configurar_nlp(lingua_spacy)
    # discerne se tem ou se não tem páginas passadas pelo usuário.
    if all([bool(paginas), local.suffix in ['.pdf']]):
        numeros_paginas = tratar_paginas_usuario(paginas)

        textos = []
        for numero in numeros_paginas:
            textos_ = extensoes_e_funcoes[local.suffix](
                local, numero
            )
            textos.append(textos_)
    else:
        textos = extensoes_e_funcoes[local.suffix](local)
    return textos