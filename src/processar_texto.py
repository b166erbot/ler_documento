from typing import Iterable

from spacy import load
from spacy.cli import download

nlp = None


def configurar_nlp(lingua: str):
    """Injeta o idioma e configura o nlp."""
    global nlp
    try:
        nlp = load(lingua)
    except OSError:
        download(lingua)
        nlp = load(lingua)


def processar(texto: str) -> Iterable:
    """Retorna os textos em forma de sentenças."""
    doc = nlp(texto)
    return map(lambda sentenca: sentenca.text, doc.sents)