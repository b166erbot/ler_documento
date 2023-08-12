from typing import Iterable

from spacy import load
from spacy.cli import download

nlp = None


def configurar_nlp(lingua: str):
    global nlp
    try:
        nlp = load(lingua)
    except OSError:
        download(lingua)
        nlp = load(lingua)


def processar(texto: str) -> Iterable:
    doc = nlp(texto)
    return map(lambda sentenca: sentenca.text, doc.sents)