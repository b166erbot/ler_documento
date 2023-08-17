import re
from itertools import chain, dropwhile, takewhile
from pathlib import Path
from subprocess import getoutput
from time import sleep
from typing import Any, Optional


def esta_instalado(programa: str) -> bool:
    resposta = getoutput(f'apt list {programa} --installed')
    return programa in resposta


def tratar_paginas_usuario(paginas: str) -> list[int]:
    """Trata o input do usuário e retorna inteiros e ranges."""
    paginas = paginas.strip()
    compilado = re.compile(r'\b\d+-\d+|\b\d+\b')
    itens = compilado.findall(paginas)

    # filtra as strings e pega só as que são numéricas e depois transforma
    # em inteiros
    numeros = list(map(
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
    paginas_ = list(chain(numeros, *ranges))
    paginas_.sort()
    return paginas_


def paginas_invalidas(texto: str) -> bool:
    padrao = r'^(\d+)(?:-(\d+))?'
    itens = texto.split(', ')
    for item in itens:
        match = re.fullmatch(padrao, item)
        if not match:
            return True
        if match.group(2):
            num_anterior, num_posterior = map(int, match.groups())
            if num_anterior >= num_posterior:
                return True
    return False


class ContagemFinita:
    def __init__(self, numero_inicial: int = 0, numero_final: int = 0) -> None:
        self._numero_inicial = numero_inicial
        self._numero_final = numero_final
        self.numero_atual = numero_inicial
        self.repetir = True
        self.repetir_ao_passar_pagina = False

    @property
    def proximo(self) -> int:
        if any([self.repetir, self.repetir_ao_passar_pagina]):
            self.repetir_ao_passar_pagina = False
            return self.numero_atual
        self.numero_atual = (
            min([self.numero_atual + 1, self._numero_final])
        )
        return self.numero_atual

    @property
    def proximo_sem_restricao(self) -> int:
        if self.repetir:
            return self.numero_atual
        self.numero_atual = (
            min([self.numero_atual + 1, self._numero_final])
        )
        return self.numero_atual

    @property
    def anterior(self) -> int:
        if self.repetir:
            return self.numero_atual
        self.numero_atual = (
            max([self.numero_atual - 1, self._numero_inicial])
        )
        return self.numero_atual

    @property
    def tem_proximo(self) -> bool:
        # retorna falso caso não tenha mais um próximo número
        if any([self.repetir, self.repetir_ao_passar_pagina]):
            return True
        return True if self.numero_atual < self._numero_final else False

    @property
    def tem_anterior(self) -> bool:
        # retorna falso caso não tenha mais um número anterior
        if any([self.repetir, self.repetir_ao_passar_pagina]):
            return True
        return True if self.numero_atual > self._numero_inicial else False

    def atualizar_limites(
        self, numero_inicial: int = None, numero_final: int = None
    ) -> None:
        # define os novos limites.
        if isinstance(numero_inicial, int):
            self._numero_inicial = numero_inicial
        if isinstance(numero_final, int):
            self._numero_final = numero_final
        # resetando o número atual
        self.numero_atual = numero_inicial or self._numero_inicial
        # corrige o número atual caso ele esteja fora dos limites.
        condicao = [
            self.numero_atual < self._numero_inicial,
            self.numero_atual > self._numero_final
        ]
        if any(condicao):
            self.numero_atual = min([self.numero_atual, self._numero_final])
            self.numero_atual = max([self.numero_atual, self._numero_inicial])

    def ir_para_o_inicio(self):
        self.numero_atual = self._numero_inicial

    def ir_para_o_final(self):
        self.numero_atual = self._numero_final
    
    @property
    def retornar_numero_final(self) -> int:
        return self._numero_final


class ContagensFinitas:
    def __init__(
        self, paginas_indexes: Optional[list[list[int]]] = None,
        nome_arquivo: Optional[Path] = None
    ) -> None:
        if all(map(
            lambda item: item != None,
            [paginas_indexes, nome_arquivo]
        )):
            self._contagens = {
                numero: ContagemFinita(inicio, fim)
                for (numero, inicio, fim) in paginas_indexes
            }
            self._indexes_paginas = list(self._contagens)
            self.contagem_atual = self._contagens[self._indexes_paginas[0]]
            self._numero_inicial = 0
            self._numero_final = len(self._contagens) - 1
            self.numero_atual = 0
            self.nome_arquivo = nome_arquivo

    @property
    def proximo(self) -> list[slice]:
        if self.contagem_atual.tem_proximo:
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            if self.contagem_atual.repetir:
                self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        elif self.tem_proximo:
            self.contagem_atual.repetir = True
            self.numero_atual += 1
            self.contagem_atual = self._contagens[
                self._indexes_paginas[self.numero_atual]
            ]
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.repetir = True
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.numero_atual
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def anterior(self) -> list[slice]:
        if self.contagem_atual.tem_anterior:
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.anterior
            if self.contagem_atual.repetir:
                self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        elif self.tem_anterior:
            self.contagem_atual.repetir = True
            self.numero_atual -= 1
            self.contagem_atual = self._contagens[
                self._indexes_paginas[self.numero_atual]
            ]
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.repetir = True
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.numero_atual
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def tem_proximo(self) -> bool:
        tem_proximo = any([
            self.contagem_atual.tem_proximo,
            self.numero_atual < self._numero_final
        ])
        return tem_proximo

    @property
    def tem_anterior(self) -> bool:
        tem_anterior = any([
            self.contagem_atual.tem_anterior,
            self.numero_atual > self._numero_inicial
        ])
        return tem_anterior
    
    # Não há necessidade de retornar slices na próxima_página e página_anterior.
    # Refatorar ou irá precisar no futuro?
    @property
    def proxima_pagina(self) -> list[slice]:
        if self.tem_proxima_pagina:
            # Colocar a contagem da página atual no último e ativar o repetir.
            self.contagem_atual.ir_para_o_final()
            self.contagem_atual.repetir = True

            self.numero_atual += 1
            self.contagem_atual = self._contagens[
                self._indexes_paginas[self.numero_atual]
            ]

            # Voltando para o início pois não sei se o próximo estava no início.
            self.contagem_atual.ir_para_o_inicio()

            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.ir_para_o_final()
            self.contagem_atual.repetir = True
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.numero_atual
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def pagina_anterior(self) -> list[slice]:
        if self.tem_pagina_anterior:
            # Colocar a contagem da página atual no primeiro e ativar o repetir.
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            self.numero_atual -= 1
            self.contagem_atual = self._contagens[
                self._indexes_paginas[self.numero_atual]
            ]

            # Voltando para o início pois não sei se o anterior estava no início
            # Precisa ir para o início pois a troca de página é diferente.
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.numero_atual
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def tem_proxima_pagina(self) -> bool:
        return self.numero_atual < self._numero_final
    
    @property
    def tem_pagina_anterior(self) -> bool:
        return self.numero_atual > self._numero_inicial
    
    def atualizar_contagens(
        self, paginas_indexes: list[list[int]], nome_arquivo: str
    ) -> None:
        self.__init__(paginas_indexes, nome_arquivo)
    
    @property
    def pagina_atual(self) -> int:
        return self._indexes_paginas[self.numero_atual]
    
    def definir_progresso(self, progresso: list[int]) -> None:
        self.contagem_atual = self._contagens[
            self._indexes_paginas[progresso[0]]
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
        self.numero_atual, self.contagem_atual.numero_atual = progresso

    @property
    def numero_atual_(self) -> int:
        return sum([
            contagem.numero_atual for contagem in self._contagens.values()
        ])
    
    @property
    def numero_maximo(self) -> int:
        return sum([
            contagem.retornar_numero_final
            for contagem
            in self._contagens.values()
        ])


class Temporizador:
    def __init__(self):
        self._segundos = 0
    
    def ativar(self, segundos: int) -> None:
        if segundos < 0:
            raise ValueError("O valor de segundos precisa ser 'segundos >= 0'.")
        self._segundos = segundos
    
    def esperar(self):
        while bool(self._segundos):
            self._segundos -= 1
            sleep(1)


def recortar(lista: list[Any], numero: int) -> list[list[Any]]:
    return [
        lista[pulo: pulo + numero]
        for pulo
        in range(0, len(lista), numero)
    ]


class Porcento:
    def __init__(self, total: int, numero_atual: int) -> None:
        self._total = total
        self._numero_atual = numero_atual
    
    def calcular(self, numero_atual: int, ) -> int:
        porcentagem = ((numero_atual - self._numero_atual) * 100) / self._total
        self._numero_atual = numero_atual
        return porcentagem
    
    @property
    def finalizou(self) -> bool:
        return self._total == self._numero_atual
    
    @property
    def porcentagem_atual(self) -> int:
        return (self._numero_atual * 100) / self._total


def colorir(texto: str, cor: str) -> str:
    return f"[{cor}]{texto}[/]"