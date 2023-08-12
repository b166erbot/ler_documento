from argparse import Namespace
from getpass import getpass
from os import get_terminal_size, system
from pathlib import Path
from threading import Thread
from time import sleep
from typing import Optional

from pynput import keyboard

from src.falar import falar, parar_fala
from src.salvar import (carregar_config_falas, carregar_config_teclado,
                        carregar_progresso, existe_arquivo, salvar_progresso)
from src.utils import Temporizador
from src.modulo_intermediario import contagens

pausar_entre_falas = Temporizador()


# observação: é necessário imprimir sempre com um espaço vazio na frente da
# string pois é um bug onde o pipeline do terminal fica por cima do primeiro
# caractere.


def sair():
    salvar_progresso(
        contagens.nome_arquivo,
        [
            contagens.pagina_atual,
            contagens.contagem_atual.numero_atual
        ]
    )
    pausar_entre_falas.ativar(1)
    parar_fala()
    raise keyboard.Listener.StopException


def limpar_linha() -> None:
    # limpa a linha para imprimir a nova linha. Corrigindo um bug.
    tamanho_linha_terminal = get_terminal_size()[0] - 1
    print(' ' * tamanho_linha_terminal, end = '\r')


def resto_codigo_acao() -> None:
    contagens.contagem_atual.repetir_ao_passar_pagina = True
    pagina = contagens.pagina_atual
    sentença = contagens.contagem_atual.numero_atual
    limpar_linha()
    texto = f" voltando: pagina {pagina + 1}, sentença {sentença + 1}"
    print(texto, end = '\r')
    pausar_entre_falas.ativar(1)
    parar_fala()


def voltar() -> None:
    contagens.anterior
    resto_codigo_acao()


def avancar() -> None:
    contagens.contagem_atual.proximo_sem_restricao
    resto_codigo_acao()


def avancar_pagina() -> None:
    contagens.proxima_pagina
    resto_codigo_acao()


def voltar_pagina() -> None:
    contagens.pagina_anterior
    resto_codigo_acao()


def gerenciar_teclado() -> None:
    # Coloque a ordem das funções de acordo com a ordem no config.json.
    funcoes = [voltar, avancar, voltar_pagina, avancar_pagina, sair]
    atalhos = {
        atalhos: funcao
        for atalhos, funcao
        in zip(carregar_config_teclado(), funcoes)
    }
    escutando_teclado = keyboard.GlobalHotKeys(atalhos)
    return escutando_teclado


def gerenciar_falas(
    textos: list[int, list[str]], argumentos: Namespace
) -> None:
    # nome_arquivo = Path(argumentos.arquivo.strip())
    # contagens.atualizar_contagens(
    #     # Contar o número de sentenças em uma página
    #     [
    #         # Passar o número da página e os indexes iniciais e finais
    #         # parao contagens.
    #         (numero, 0, len(pagina) - 1)
    #         for numero, pagina in textos
    #     ],
    #     nome_arquivo
    # )
    if existe_arquivo(Path('progresso.json')):
        progresso = carregar_progresso(nome_arquivo)
        if progresso != None:
            contagens.definir_progresso(progresso)
    config = carregar_config_falas()
    texto_teclas = ''.join(map(
        lambda atalho: f"\n{atalho} -> {{}}",
        config['teclas_atalho']
    ))
    texto_teclas = texto_teclas.format(*config['teclas_atalho'].values())
    print('Altere as teclas de atalho em ler_documento/scripts/configurar.py')
    print(f"teclas de atalho: {texto_teclas}")
    while contagens.tem_proximo:
        pausar_entre_falas.esperar()
        slice_pagina, slice_linha = contagens.proximo
        pagina = contagens.pagina_atual
        sentença = contagens.contagem_atual.numero_atual

        # limpa a linha para imprimir a nova linha. Corrigindo um bug.
        tamanho_linha_terminal = get_terminal_size()[0] - 1
        print(' ' * tamanho_linha_terminal, end = '\r')

        print(f" página {pagina + 1}, sentença {sentença + 1}", end = '\r')
        # todo [0] é obrigatório por causa do slice.
        # o único [1] é por causa que os textos agora estão com números
        # das páginas
        texto = textos[slice_pagina][0][1][slice_linha][0]
        falar(texto, argumentos.lingua_espeak, argumentos.velocidade)


def bloquear_entradas_usuario():
    while True:
        system('clear || cls')
        getpass('')
