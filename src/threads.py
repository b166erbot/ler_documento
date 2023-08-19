from argparse import Namespace
from pathlib import Path
from time import sleep
from typing import Callable

from textual.screen import Screen

from src.falar import falar, parar_fala
from src.salvar import carregar_progresso, existe_arquivo, salvar_progresso
from src.utils import ContagensFinitas, Temporizador

# pausa entre o avançar e voltar fala.
pausar_entre_falas = Temporizador()
sair_: bool = False

# observação: é necessário imprimir sempre com um espaço vazio na frente da
# string pois é um bug onde o pipeline do terminal fica por cima do primeiro
# caractere.


def sair(contagens: ContagensFinitas):
    """Ajuda a função gerenciar_falas a sair."""
    global sair_
    salvar_progresso(
        contagens.nome_arquivo,
        [
            contagens.numero_atual,
            contagens.contagem_atual.numero_atual
        ]
    )
    pausar_entre_falas.ativar(1)
    sair_ = True
    parar_fala()


def resto_codigo_acao(contagens: ContagensFinitas) -> None:
    """Função auxiliar para as funções neste módulo."""
    contagens.contagem_atual.repetir_ao_passar_pagina = True
    pausar_entre_falas.ativar(1)
    parar_fala()


def voltar(contagens: ContagensFinitas) -> None:
    """Volta um número na contagem."""
    contagens.anterior_sem_restrição
    resto_codigo_acao(contagens)


def avancar(contagens: ContagensFinitas) -> None:
    """Avança um número na contagem."""
    contagens.proximo_sem_restrição
    resto_codigo_acao(contagens)


def avancar_pagina(contagens: ContagensFinitas) -> None:
    """Avança uma página nas contagens."""
    contagens.proxima_pagina
    resto_codigo_acao(contagens)


def voltar_pagina(contagens: ContagensFinitas) -> None:
    """Volta uma página nas contagens."""
    contagens.pagina_anterior
    resto_codigo_acao(contagens)


def gerenciar_falas(
    textos: list[int, list[str]], argumentos: Namespace,
    contagens: ContagensFinitas, tela_boas_vindas: Screen
) -> None:
    """Função que irá gerenciar as falas e precisa rodar como uma tread."""
    sleep(1)
    while contagens.tem_proximo:
        tela_boas_vindas._esperar_retomar()
        pausar_entre_falas.esperar()
        slice_pagina, slice_sentença = contagens.proximo
        tela_boas_vindas._atualizar_progresso()
        tela_boas_vindas._atualizar_label_status()
        if sair_:
            break

        # todo [0] é obrigatório por causa do slice.
        # o único [1] é por causa que os textos agora estão com números
        # das páginas
        texto = textos[slice_pagina][0][1][slice_sentença][0]
        tela_boas_vindas._atualizar_label_sentenças(texto)
        falar(texto, argumentos.lingua_espeak, argumentos.velocidade)