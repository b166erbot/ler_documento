from copy import deepcopy
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from time import time

from src.extrair_texto import extrair, extrair_texto, extrair_texto_pdf


tempos = Path('tempos_dos_arquivos.txt')
if tempos.is_file():
    tempos.unlink()


class TestCaseTemporizado(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arquivo = open('tempos_dos_testes.txt', 'a')
    
    @classmethod
    def tearDownClass(cls):
        cls.arquivo.close()
    
    def setUp(self):
        self.inicio = time()
        self.nome_funcao = ''
    
    def tearDown(self):
        fim = time()
        self.arquivo.write(
            f"nome: {self.nome_funcao}, tempo: {fim - self.inicio}\n"
        )


@patch('src.extrair_texto.processar')
@patch('src.extrair_texto.configurar_nlp')
class TestExtrair(TestCaseTemporizado):
    def setUp(self):
        super().setUp()
        self.arquivo_pdf = Path('/local/do/arquivo.pdf')
        self.arquivo_txt = Path('/local/do/arquivo.txt')
        self.arquivo_sem_ext = Path('/local/do/arquivo')
        self.paginas = '0, 1-2'
        self.lingua_spacy = 'pt_core_news_sm'

    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_if_bool_paginas_com_arquivo_pdf(
        self, extensoes_e_funcoes, configurar_nlp, processar
    ):
        self.nome_funcao = str(
            self.test_passando_pelo_if_bool_paginas_com_arquivo_pdf
        )
        esperado = [[numero, ['texto', 'outro texto']] for numero in range(3)]
        extensoes_e_funcoes.__getitem__.return_value.side_effect = deepcopy(
            esperado
        )
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy, self.paginas)
        self.assertEqual(esperado, resultado)

    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_else_com_arquivo_pdf(
        self, extensoes_e_funcoes, configurar_nlp, processar
    ):
        self.nome_funcao = str(self.test_passando_pelo_else_com_arquivo_pdf)
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            (0, ['texto', 'outro texto'])
        ]
        esperado = [(0, ['texto', 'outro texto'])]
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)
    
    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_if_bool_paginas_com_arquivo_txt(
        self, extensoes_e_funcoes, configurar_nlp, processar
    ):
        self.nome_funcao = str(
            self.test_passando_pelo_if_bool_paginas_com_arquivo_txt
        )
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(self.arquivo_txt, self.lingua_spacy, self.paginas)
        self.assertEqual(esperado, resultado)
    
    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_else_com_arquivo_txt(
        self, extensoes_e_funcoes, configurar_nlp, processar
    ):
        self.nome_funcao = str(self.test_passando_pelo_else_com_arquivo_txt)
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(self.arquivo_txt, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)

    @patch('src.extrair_texto.extensoes_e_funcoes')
    def test_passando_pelo_if_bool_paginas_com_arquivo_sem_extensao(
        self, extensoes_e_funcoes, configurar_nlp, processar
    ):
        self.nome_funcao = str(
            self.test_passando_pelo_if_bool_paginas_com_arquivo_sem_extensao
        )
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
        self, extensoes_e_funcoes, configurar_nlp, processar
    ):
        self.nome_funcao = str(
            self.test_passando_pelo_else_com_arquivo_sem_extensao
        )
        extensoes_e_funcoes.__getitem__.return_value.return_value = [
            ['texto', 'outro texto']
        ]
        esperado = [['texto', 'outro texto']]
        resultado = extrair(self.arquivo_sem_ext, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)
    

@patch('src.extrair_texto.processar')
@patch('src.extrair_texto.PdfFileReader')
@patch('src.extrair_texto.open')
class TestReal(TestCaseTemporizado):
    # esses testes só são feitos pois não dá para debugar com o pdb no textual
    def setUp(self):
        super().setUp()
        self.arquivo_pdf = Path('local/do/arquivo.pdf')
        self.arquivo_txt = Path('local/do/arquivo.txt')
        self.arquivo_sem_ext = Path('local/do/arquivo')
        self.paginas = '0, 1-2'
        self.lingua_spacy = 'pt_core_news_sm'
    
    def test_arquivo_pdf_com_paginas(self, open, PdfFileReader, processar):
        self.nome_funcao = str(self.test_arquivo_pdf_com_paginas)
        processar.return_value = ['Olá!', 'Tem alguém ai?']
        leitor_pdf = PdfFileReader()
        leitor_pdf.numPages = 3
        leitor_pdf.getPage().extractText.return_value = 'Olá! Tem alguém ai?'
        esperado = [
            [[numero, ['Olá!', 'Tem alguém ai?']]] for numero in range(3)
        ]
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy, self.paginas)
        self.assertEqual(esperado, resultado)
        processar.assert_any_call()
    
    def test_arquivo_pdf_sem_paginas(self, open, PdfFileReader, processar):
        self.nome_funcao = str(self.test_arquivo_pdf_sem_paginas)
        processar.return_value = ['Olá!', 'Tem alguém ai?']
        leitor_pdf = PdfFileReader()
        leitor_pdf.numPages = 3
        leitor_pdf.getPage().extractText.return_value = 'Olá! Tem alguém ai?'
        esperado = [
            [numero, ['Olá!', 'Tem alguém ai?']] for numero in range(3)
        ]
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)
        processar.assert_any_call()
    
    def test_arquivo_txt_sem_paginas(self, open, PdfFileReader, processar):
        self.nome_funcao = str(self.test_arquivo_txt_sem_paginas)
        processar.return_value = ['Olá!', 'Tem alguém ai?']
        open().__enter__().read.return_value = 'Olá! Tem alguém ai?'
        esperado = [[0, ['Olá!', 'Tem alguém ai?']]]
        resultado = extrair(self.arquivo_txt, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)
        processar.assert_called_once()
    
    def test_arquivo_sem_extensao_sem_paginas(
        self, open, PdfFileReader, processar
    ):
        self.nome_funcao = str(self.test_arquivo_sem_extensao_sem_paginas)
        processar.return_value = ['Olá!', 'Tem alguém ai?']
        open().__enter__().read.return_value = 'Olá! Tem alguém ai?'
        esperado = [[0, ['Olá!', 'Tem alguém ai?']]]
        resultado = extrair(self.arquivo_sem_ext, self.lingua_spacy, None)
        self.assertEqual(esperado, resultado)
        processar.assert_called_once()
