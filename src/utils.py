import os
import re
from itertools import chain, dropwhile, takewhile
from pathlib import Path
from time import sleep
from typing import Any, Optional


def esta_instalado(programa: str) -> bool:
    """Verifica se o programa está instalado no pc."""
    for local in os.environ["PATH"].split(os.pathsep):
        if programa in os.listdir(local):
            return True
    return False


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
    """Verifica se as páginas digitadas pelo usuário estão erradas."""
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
        """Retorna o próximo número da contagem."""
        if any([self.repetir, self.repetir_ao_passar_pagina]):
            self.repetir_ao_passar_pagina = False
            return self.numero_atual
        self.numero_atual = (
            min([self.numero_atual + 1, self._numero_final])
        )
        return self.numero_atual

    @property
    def proximo_sem_restricao(self) -> int:
        """Retorna o próximo número da contagem sem restrição."""
        if self.repetir:
            return self.numero_atual
        self.numero_atual = (
            min([self.numero_atual + 1, self._numero_final])
        )
        return self.numero_atual

    @property
    def anterior(self) -> int:
        """Retorna o número anterior da contagem."""
        if self.repetir:
            return self.numero_atual
        self.numero_atual = (
            max([self.numero_atual - 1, self._numero_inicial])
        )
        return self.numero_atual

    @property
    def tem_proximo(self) -> bool:
        """Verifica se tem próximo número."""
        if any([self.repetir, self.repetir_ao_passar_pagina]):
            return True
        return True if self.numero_atual < self._numero_final else False

    @property
    def tem_anterior(self) -> bool:
        """Verifica se tem número anterior."""
        if any([self.repetir, self.repetir_ao_passar_pagina]):
            return True
        return True if self.numero_atual > self._numero_inicial else False

    @property
    def tem_proximo_sem_restrição(self) -> bool:
        """Verifica se tem próximo número."""
        if self.repetir:
            return True
        return True if self.numero_atual < self._numero_final else False
    
    @property
    def tem_anterior_sem_restrição(self) -> bool:
        """Verifica se tem número anterior."""
        if self.repetir:
            return True
        return True if self.numero_atual > self._numero_inicial else False

    def atualizar_limites(
        self, numero_inicial: int = None, numero_final: int = None
    ) -> None:
        """Atualiza os limites da contagem."""
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
        """Retrocede a contagem para o início."""
        self.numero_atual = self._numero_inicial

    def ir_para_o_final(self):
        """Avança a contagem para o final."""
        self.numero_atual = self._numero_final
        self.repetir = True
    
    @property
    def retornar_numero_final(self) -> int:
        """Retorna o número final da contagem."""
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
            self._indexes_contagens = {
                index: numero_pagina for index, numero_pagina
                in enumerate(self._contagens)
            }
            self._indexes_contagens_inverso = {
                numero_pagina: index for index, numero_pagina
                in enumerate(self._contagens)
            }
            self.contagem_atual = self._contagens[self._indexes_contagens[0]]
            self._numero_inicial = 0
            self._numero_final = len(self._contagens) - 1
            self.numero_atual = 0
            self.nome_arquivo = nome_arquivo
            self.repetir = False

    @property
    def proximo(self) -> list[slice]:
        """Retorna o próximo número das contagens."""
        if self.contagem_atual.tem_proximo:
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            if self.contagem_atual.repetir:
                self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.repetir = True
            self.numero_atual += 1
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.numero_atual]
            ]
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def proximo_sem_restrição(self) -> list[slice]:
        """Retorna o próximo número das contagens."""
        if self.contagem_atual.tem_proximo_sem_restrição:
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo_sem_restricao
            if self.contagem_atual.repetir:
                self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.repetir = True
            self.numero_atual = min([
                self.numero_atual + 1, self._numero_final
            ])
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.numero_atual]
            ]
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def anterior(self) -> list[slice]:
        """Retorna o número anterior das contagens."""
        if self.contagem_atual.tem_anterior:
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.anterior
            if self.contagem_atual.repetir:
                self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.repetir = True
            self.numero_atual = max([
                self.numero_atual + 1, self._numero_inicial
            ])
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.numero_atual]
            ]
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]
    
    @property
    def anterior_sem_restrição(self) -> list[slice]:
        """Retorna o número anterior das contagens."""
        if self.contagem_atual.tem_anterior_sem_restrição:
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.anterior
            if self.contagem_atual.repetir:
                self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        else:
            self.contagem_atual.repetir = True
            self.numero_atual -= 1
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.numero_atual]
            ]
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.anterior
            self.contagem_atual.repetir = False
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def tem_proximo(self) -> bool:
        """Verifica se tem próximo número das contagens."""
        tem_proximo = any([
            self.contagem_atual.tem_proximo,
            self.numero_atual < self._numero_final
        ])
        return tem_proximo

    @property
    def proxima_pagina(self) -> list[slice]:
        """Retorna os recortes para a próxima página."""
        if self.tem_proxima_pagina:
            # Colocar a contagem da página atual no último e ativar o repetir.
            self.contagem_atual.ir_para_o_final()
            self.contagem_atual.repetir = True

            self.numero_atual += 1
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.numero_atual]
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
            self.repetir = True
            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.numero_atual
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        return [slice1, slice2]

    @property
    def pagina_anterior(self) -> list[slice]:
        """Retorna os recortes para a página anterior."""
        # corrigindo um bug onde ao voltar uma página quando se está no fim,
        # ele retornava duas.
        if self.repetir:
            self.repetir = False
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            slice1 = slice(self.numero_atual, self.numero_atual + 1)
            numero_slice2 = self.contagem_atual.proximo
            slice2 = slice(numero_slice2, numero_slice2 + 1)
        elif self.tem_pagina_anterior:
            # Colocar a contagem da página atual no primeiro e ativar o repetir.
            self.contagem_atual.ir_para_o_inicio()
            self.contagem_atual.repetir = True

            self.numero_atual -= 1
            self.contagem_atual = self._contagens[
                self._indexes_contagens[self.numero_atual]
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
        """Verifica se tem próximo número."""
        return self.numero_atual < self._numero_final
    
    @property
    def tem_pagina_anterior(self) -> bool:
        """Verifica se tem número anterior."""
        return self.numero_atual > self._numero_inicial
    
    def atualizar_contagens(
        self, paginas_indexes: list[list[int]], nome_arquivo: str
    ) -> None:
        """Atualiza as contagens."""
        self.__init__(paginas_indexes, nome_arquivo)
    
    def definir_progresso(self, progresso: list[int]) -> None:
        """Define o progresso."""
        if progresso[0] != None:
            self._definir_progresso_paginas(progresso[0])
        if progresso[1] != None:
            self._definir_progresso_sentença(progresso[1])
        if self.numero_atual == self._numero_final:
            self.repetir = True

    def _definir_progresso_paginas(self, pagina: int) -> None:
        """Define o progresso da página."""
        self.contagem_atual = self._contagens[
            self._indexes_contagens[pagina]
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
        self.numero_atual = pagina
    
    def _definir_progresso_sentença(self, sentença: int) -> None:
        """Define o progresso da sentença."""
        self.contagem_atual.numero_atual = sentença

    @property
    def numero_atual_(self) -> int:
        """Retorna o número atual da contagem de todas as contagens."""
        contagens = list(takewhile(
            lambda contagem: not contagem is self.contagem_atual,
            self._contagens.values()
        ))
        contagens.append(self.contagem_atual)
        numero_atual = sum([
            contagem.numero_atual for contagem in contagens
        ])
        numero_atual += len(contagens) - 1
        return numero_atual
    
    @property
    def numero_maximo(self) -> int:
        """Retorna o número máximo de todas as contagens."""
        numero_maximo = sum([
            contagem.retornar_numero_final
            for contagem
            in self._contagens.values()
        ])
        numero_maximo += len(self._contagens) - 1
        return numero_maximo
    
    @property
    def finalizou(self) -> bool:
        return self.numero_maximo == self.numero_atual_


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
        while bool(self._segundos):
            self._segundos -= 1
            sleep(1)


def recortar(lista: list[Any], numero: int) -> list[list[Any]]:
    """Recorta uma lista conforme do número passado."""
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
        """Calcula a porcentagem dependendo da porcentagem anterior."""
        porcentagem = ((numero_atual - self._numero_atual) * 100) / self._total
        self._numero_atual = numero_atual
        return porcentagem
    
    @property
    def finalizou(self) -> bool:
        """Verifica se a porcentagem chegou ao final."""
        return self._total == self._numero_atual
    
    @property
    def porcentagem_atual(self) -> int:
        """Retorna a porcentagem atual."""
        return (self._numero_atual * 100) / self._total


def colorir(texto: str, cor: str) -> str:
    """Colore um texto de acordo com as regras da lib rich."""
    return f"[{cor}]{texto}[/]"