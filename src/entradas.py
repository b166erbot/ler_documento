from typing import Callable


def pegar_entrada(funcao: Callable, texto: str, texto_erro: str) -> str:
    """Requisita um texto até ele passar pela funcao e a retorna."""
    entrada = input(texto)
    while not funcao(entrada):
        print(texto_erro)
        entrada = input(texto)
    return entrada