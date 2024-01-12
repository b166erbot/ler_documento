import os, re, sys
from itertools import chain, combinations, dropwhile, takewhile
from pathlib import Path
from time import sleep
from typing import Any, Optional

from _utils import está_instalado


def tratar_páginas_usuario(páginas: str) -> list[int]:
    """Trata o input do usuário e retorna inteiros e ranges."""
    páginas = páginas.strip()
    compilado = re.compile(r'\b\d+-\d+|\b\d+\b')
    itens = compilado.findall(páginas)

    # filtra as strings e pega só as que são numéricas e depois transforma
    # em inteiros
    números = list(map(
        lambda string: int(string),
        filter(
            lambda string: string.isnumeric(),
            itens
        )
    ))

    # filtra as strings que não são numéricas, corta elas e as transforma
    # em inteiros
    ranges = list(map(
        lambda string: list(map(int, string.split('-'))),
        filter(
            lambda string: not string.isnumeric(),
            itens
        )
    ))
    ranges = [range(inicio, fim + 1) for inicio, fim in ranges]

    # transformar todos os números e ranges em uma lista com números
    páginas_ = list(chain(números, *ranges))
    páginas_.sort()
    return páginas_


def páginas_invalidas(texto: str) -> bool:
    """Verifica se as páginas digitadas pelo usuário estão erradas."""
    padrao = r'^(\d+)(?:-(\d+))?'
    itens = texto.split(', ')
    itens_filtrados = []
    for item in itens:
        match = re.fullmatch(padrao, item)
        if not match:
            return True
        if match.group(2):
            num_anterior, num_posterior = map(int, match.groups())
            if num_anterior >= num_posterior:
                return True
        if '-' in item:
            itens_filtrados.append(set(map(
                str,
                range(num_anterior, num_posterior)
            )))
        else:
            itens_filtrados.append(set([item]))
    for conjunto1, conjunto2 in combinations(itens_filtrados, 2):
        if any(conjunto1 & conjunto2):
            return True
    return False


class ContagemFinita:
    def __init__(self, número_inicial: int = 0, número_final: int = 0) -> None:
        self._número_inicial = número_inicial
        self._número_final = número_final
        self.número_atual = número_inicial
        self.repetir = True
        self.repetir_ao_passar_página = False

    @property
    def próximo(self) -> int:
        """Retorna o próximo número da contagem."""
        if any([self.repetir, self.repetir_ao_passar_página]):
            self.repetir_ao_passar_página = False
            return self.número_atual
        self.número_atual = (
            min([self.número_atual + 1, self._número_final])
        )
        return self.número_atual

    @property
    def próximo_sem_restrição(self) -> int:
        """Retorna o próximo número da contagem sem restrição."""
        if self.repetir:
            return self.número_atual
        self.número_atual = (
            min([self.número_atual + 1, self._número_final])
        )
        return self.número_atual

    @property
    def anterior(self) -> int:
        """Retorna o número anterior da contagem."""
        if self.repetir:
            return self.número_atual
        self.número_atual = (
            max([self.número_atual - 1, self._número_inicial])
        )
        return self.número_atual

    @property
    def tem_próximo(self) -> bool:
        """Verifica se tem próximo número."""
        if any([
            self.repetir, self.repetir_ao_passar_página,
            self.número_atual < self._número_final
        ]):
            return True
        else:
            return False

    @property
    def tem_anterior(self) -> bool:
        """Verifica se tem número anterior."""
        if any([
            self.repetir, self.repetir_ao_passar_página,
            self.número_atual > self._número_inicial
        ]):
            return True
        else:
            return False

    @property
    def tem_próximo_sem_restrição(self) -> bool:
        """Verifica se tem próximo número."""
        if any([self.repetir, self.número_atual < self._número_final]):
            return True
        else:
            return False
    
    @property
    def tem_anterior_sem_restrição(self) -> bool:
        """Verifica se tem número anterior."""
        if any([self.repetir, self.número_atual > self._número_inicial]):
            return True
        return False

    def atualizar_limites(
        self, número_inicial: int = None, número_final: int = None
    ) -> None:
        """Atualiza os limites da contagem."""
        # define os novos limites.
        if isinstance(número_inicial, int):
            self._número_inicial = número_inicial
        if isinstance(número_final, int):
            self._número_final = número_final
        # corrige o número atual caso ele esteja fora dos limites.
        condicao = [
            self.número_atual < self._número_inicial,
            self.número_atual > self._número_final
        ]
        if any(condicao):
            self.número_atual = min([self.número_atual, self._número_final])
            self.número_atual = max([self.número_atual, self._número_inicial])

    def ir_para_o_inicio(self):
        """Retrocede a contagem para o início."""
        self.número_atual = self._número_inicial

    def ir_para_o_final(self):
        """Avança a contagem para o final."""
        self.número_atual = self._número_final
        self.repetir = True
    
    @property
    def retornar_número_final(self) -> int:
        """Retorna o número final da contagem."""
        return self._número_final


class ContagensFinitas:
    def __init__(
        self, páginas_indexes: Optional[list[list[int]]] = None,
        nome_arquivo: Optional[Path] = None
    ) -> None:
        if all(map(
            lambda item: item != None,
            [páginas_indexes, nome_arquivo]
        )):
            self._contagens = {
                número: ContagemFinita(inicio, fim)
                for (número, inicio, fim) in páginas_indexes
            }
            self._indexes_contagens = {
                index: número_página for index, número_página
                in enumerate(self._contagens)
            }
            self._indexes_contagens_inverso = {
                número_página: index for index, número_página
                in enumerate(self._contagens)
            }
            self.contagem_atual = self._contagens[self._indexes_contagens[0]]
            self._número_inicial = 0
            self._número_final = len(self._contagens) - 1
            self.número_atual = 0
            self.nome_arquivo = nome_arquivo
            # o repetir do ContagemFinita e esse repetir aqui tem propósitos
            # diferentes.
            self.repetir = False

    @property
    def próximo(self) -> list[slice]:
        """Retorna o próximo número das contagens."""
        if self.contagem_atual.tem_próximo:
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        else:
            self.número_atual = min([
                self.número_atual + 1, self._número_final
            ])
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.número_atual]
            ]
            self.contagem_atual.repetir = True
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo
            slice2 = slice(número_slice2, número_slice2 + 1)
        return [slice1, slice2]

    @property
    def próximo_sem_restrição(self) -> list[slice]:
        """Retorna o próximo número das contagens."""
        if self.contagem_atual.tem_próximo_sem_restrição:
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo_sem_restrição
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        else:
            self.número_atual = min([
                self.número_atual + 1, self._número_final
            ])
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.número_atual]
            ]
            self.contagem_atual.repetir = True
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo
            slice2 = slice(número_slice2, número_slice2 + 1)
        return [slice1, slice2]

    @property
    def anterior(self) -> list[slice]:
        """Retorna o número anterior das contagens."""
        if self.contagem_atual.tem_anterior:
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        else:
            self.número_atual = max([
                self.número_atual - 1, self._número_inicial
            ])
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.número_atual]
            ]
            self.contagem_atual.repetir = True
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        return [slice1, slice2]

    @property
    def anterior_sem_restrição(self) -> list[slice]:
        """Retorna o número anterior das contagens."""
        if self.contagem_atual.tem_anterior_sem_restrição:
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        else:
            self.número_atual = max([
                self.número_atual - 1, self._número_inicial
            ])
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.número_atual]
            ]
            self.contagem_atual.repetir = True
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        return [slice1, slice2]

    @property
    def tem_próximo(self) -> bool:
        """Verifica se tem próximo número das contagens."""
        tem_próximo = any([
            self.contagem_atual.tem_próximo,
            self.número_atual < self._número_final
        ])
        return tem_próximo

    @property
    def proxima_página(self) -> list[slice]:
        """Retorna os recortes para a próxima página."""
        if self.tem_proxima_página:
            # Colocar a contagem da página atual no último e ativar o repetir.
            self.contagem_atual.ir_para_o_final()
            self.contagem_atual.repetir = True

            self.número_atual += 1
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.número_atual]
            ]

            # Voltando para o início pois não sei se o próximo está no início.
            self.contagem_atual.ir_para_o_inicio()

            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        else:
            self.contagem_atual.ir_para_o_final()
            self.contagem_atual.repetir = True
            self.repetir = True
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.número_atual
            slice2 = slice(número_slice2, número_slice2 + 1)
        return [slice1, slice2]

    @property
    def página_anterior(self) -> list[slice]:
        """Retorna os recortes para a página anterior."""
        # corrigindo um bug onde ao voltar uma página quando se está no fim,
        # ele retornava duas.
        if self.repetir:
            self.repetir = False
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo
            slice2 = slice(número_slice2, número_slice2 + 1)
        elif self.tem_página_anterior:
            # Colocar a contagem da página atual no primeiro e ativar o repetir.
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            self.número_atual -= 1
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.número_atual]
            ]

            # Voltando para o início pois não sei se o anterior estava no início
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.próximo
            self.contagem_atual.repetir = False
            slice2 = slice(número_slice2, número_slice2 + 1)
        else:
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True
            slice1 = slice(self.número_atual, self.número_atual + 1)
            número_slice2 = self.contagem_atual.número_atual
            slice2 = slice(número_slice2, número_slice2 + 1)
        return [slice1, slice2]

    @property
    def tem_proxima_página(self) -> bool:
        """Verifica se tem próximo número."""
        return self.número_atual < self._número_final
    
    @property
    def tem_página_anterior(self) -> bool:
        """Verifica se tem número anterior."""
        return self.número_atual > self._número_inicial
    
    def atualizar_contagens(
        self, páginas_indexes: list[list[int]], nome_arquivo: str
    ) -> None:
        """Atualiza as contagens."""
        self.__init__(páginas_indexes, nome_arquivo)
    
    def definir_progresso(self, progresso: list[int]) -> None:
        """Define o progresso."""
        if progresso[0] != None:
            self._definir_progresso_páginas(progresso[0])
        if progresso[1] != None:
            self._definir_progresso_sentença(progresso[1])
        if self.número_atual == self._número_final:
            self.repetir = True

    def _definir_progresso_páginas(self, página: int) -> None:
        """Define o progresso da página."""
        self.contagem_atual = self._contagens[
            self._indexes_contagens[página]
        ]
        contagens_antes = takewhile(
            lambda contagem: contagem != self.contagem_atual,
            self._contagens.values()
        )
        contagens_depois = dropwhile(
            lambda contagem: contagem != self.contagem_atual,
            self._contagens.values()
        )
        for contagem in contagens_antes:
            contagem.ir_para_o_final()
        for contagem in contagens_depois:
            contagem.ir_para_o_inicio()
        self.número_atual = página
    
    def _definir_progresso_sentença(self, sentença: int) -> None:
        """Define o progresso da sentença."""
        self.contagem_atual.número_atual = sentença

    @property
    def número_atual_(self) -> int:
        """Retorna o número atual da contagem de todas as contagens."""
        contagens = list(takewhile(
            lambda contagem: not contagem is self.contagem_atual,
            self._contagens.values()
        ))
        contagens.append(self.contagem_atual)
        número_atual = sum([
            contagem.número_atual for contagem in contagens
        ])
        número_atual += len(contagens) - 1
        return número_atual
    
    @property
    def número_maximo(self) -> int:
        """Retorna o número máximo de todas as contagens."""
        número_maximo = sum([
            contagem.retornar_número_final
            for contagem
            in self._contagens.values()
        ])
        número_maximo += len(self._contagens) - 1
        return número_maximo
    
    @property
    def finalizou(self) -> bool:
        return self.número_maximo == self.número_atual_


class Temporizador:
    def __init__(self):
        self._segundos = 0
    
    def ativar(self, segundos: int) -> None:
        """Define os segundos para esperar."""
        if segundos < 0:
            raise ValueError("O valor de segundos precisa ser 'segundos >= 0'.")
        self._segundos = segundos
    
    def esperar(self):
        """Espera os segundos definidos previamente."""
        # fiz dessa maneira pois os segundos podem alterar com o tempo.
        while bool(self._segundos):
            self._segundos -= 1
            sleep(1)


def recortar(lista: list[Any], número: int) -> list[list[Any]]:
    """Recorta uma lista conforme do número passado."""
    return [
        lista[pulo: pulo + número]
        for pulo
        in range(0, len(lista), número)
    ]


class Porcento:
    def __init__(self, total: int, número_atual: int) -> None:
        self._total = total
        self._número_atual = número_atual
    
    def calcular(self, número_atual: int, ) -> int:
        """Calcula a porcentagem dependendo da porcentagem anterior."""
        porcentagem = ((número_atual - self._número_atual) * 100) / self._total
        self._número_atual = número_atual
        return porcentagem
    
    @property
    def finalizou(self) -> bool:
        """Verifica se a porcentagem chegou ao final."""
        return self._total == self._número_atual
    
    @property
    def porcentagem_atual(self) -> int:
        """Retorna a porcentagem atual."""
        return (self._número_atual * 100) / self._total


def colorir(texto: str, cor: str) -> str:
    """Colore um texto de acordo com as regras da lib rich."""
    return f"[{cor}]{texto}[/{cor}]"