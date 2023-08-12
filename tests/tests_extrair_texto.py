from copy import deepcopy
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from src.extrair_texto import extrair, extrair_texto, extrair_texto_pdf


@patch('src.extrair_texto.configurar_nlp')
class TestExtrair(TestCase):
    def setUp(self):
        self.arquivo_pdf = Path('/local/do/arquivo.pdf')
        self.arquivo_txt = Path('/local/do/arquivo.txt')
        self.arquivo_sem_ext = Path('/local/do/arquivo')
        self.paginas = '0, 1-2'
        self.lingua_spacy = 'pt_core_news_sm'

    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_if_bool_paginas_com_arquivo_pdf(
        self, extensoes_e_funcoes, configurar_nlp
    ):
        esperado = [[numero, ['texto', 'outro texto']] for numero in range(3)]
        extensoes_e_funcoes.__getitem__.return_value.side_effect = deepcopy(
            esperado
        )
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy, self.paginas)
        self.assertEqual(esperado, resultado)

    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_else_com_arquivo_pdf(
        self, extensoes_e_funcoes, configurar_nlp
    ):
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            (0, ['texto', 'outro texto'])
        ]
        esperado = [(0, ['texto', 'outro texto'])]
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)
    
    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_if_bool_paginas_com_arquivo_txt(
        self, extensoes_e_funcoes, configurar_nlp
    ):
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(self.arquivo_txt, self.lingua_spacy, self.paginas)
        self.assertEqual(esperado, resultado)
    
    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_else_com_arquivo_txt(
        self, extensoes_e_funcoes, configurar_nlp
    ):
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(self.arquivo_txt, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)

    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_if_bool_paginas_com_arquivo_sem_extensao(
        self, extensoes_e_funcoes, configurar_nlp
    ):
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(
            self.arquivo_sem_ext, self.lingua_spacy, self.paginas
        )
        self.assertEqual(esperado, resultado)
    
    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_else_com_arquivo_sem_extensao(
        self, extensoes_e_funcoes, configurar_nlp
    ):
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(self.arquivo_sem_ext, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)