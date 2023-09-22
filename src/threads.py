from argparse import Namespace
from pathlib import Path
from time import sleep
from typing import Callable

from textual.screen import Screen

from src.falar import falar, parar_fala
from src.salvar import carregar_progresso, salvar_progresso
from src.utils import ContagensFinitas, Temporizador


class GerenciarFalas:
    def __init__(self, contagens: ContagensFinitas):
        # pausa entre o avançar e voltar fala.
        self.pausar_entre_falas = Temporizador()
        self.sair_: bool = False
        self.contagens = contagens

    def sair(self):
        """Ajuda a função gerenciar_falas a sair."""
        salvar_progresso(
            self.contagens.nome_arquivo,
            [
                self.contagens.número_atual,
                self.contagens.contagem_atual.número_atual
            ]
        )
        self.pausar_entre_falas.ativar(1)
        self.sair_ = True
        parar_fala()

    def resto_codigo_acao(self) -> None:
        """Função auxiliar para as funções neste módulo."""
        self.contagens.contagem_atual.repetir_ao_passar_página = True
        self.pausar_entre_falas.ativar(1)
        parar_fala()

    def voltar(self) -> None:
        """Volta um número na contagem."""
        self.contagens.anterior_sem_restrição
        self.resto_codigo_acao()

    def avancar(self) -> None:
        """Avança um número na contagem."""
        self.contagens.próximo_sem_restrição
        self.resto_codigo_acao()

    def avancar_página(self) -> None:
        """Avança uma página nas contagens."""
        self.contagens.proxima_página
        self.resto_codigo_acao()

    def voltar_página(self) -> None:
        """Volta uma página nas contagens."""
        self.contagens.página_anterior
        self.resto_codigo_acao()

    def gerenciar_falas(
        self, textos: list[int, list[str]], argumentos: Namespace,
        tela_boas_vindas: Screen
    ) -> None:
        """Função que irá gerenciar as falas e precisa rodar como uma tread."""
        sleep(1)
        if tela_boas_vindas._variaveis_compartilhadas['rodando falas']:
            return
        else:
            tela_boas_vindas._variaveis_compartilhadas['rodando falas'] = True
        while self.contagens.tem_próximo:
            tela_boas_vindas._esperar_retomar()
            self.pausar_entre_falas.esperar()
            slice_página, slice_sentença = self.contagens.próximo
            tela_boas_vindas._atualizar_progresso()
            tela_boas_vindas._atualizar_label_status()
            if self.sair_:
                break

            # todo [0] é obrigatório por causa do slice.
            # o único [1] é por causa que os textos agora estão com números
            # das páginas
            texto = textos[slice_página][0][1][slice_sentença][0]
            tela_boas_vindas._atualizar_label_sentenças(texto)
            falar(texto, argumentos.lingua_espeak, argumentos.velocidade)
        tela_boas_vindas._variaveis_compartilhadas['rodando falas'] = False