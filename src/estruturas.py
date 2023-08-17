# nome em inglês: structures
from argparse import Namespace
from dataclasses import dataclass


@dataclass
class Progresso:
    nome_arquivo: str
    argumentos: Namespace