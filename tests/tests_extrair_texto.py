from copy import deepcopy
from pathlib import Path
from time import time
from unittest import TestCase, skip
from unittest.mock import MagicMock, patch

# é necessário mockar antes para que substitua o objeto antes de ser importado
load = MagicMock()
download = MagicMock()
PdfFileReader = MagicMock()
patch('spacy.load', load).start()
patch('spacy.cli.download', download).start()
patch('PyPDF4.PdfFileReader', PdfFileReader).start()

from src.extrair_texto import (
    extrair, extrair_texto, extrair_texto_pdf, tratar_texto)


class TestExtrair(TestCase):
    def setUp(self):
        self.arquivo_pdf = Path('/local/do/arquivo.pdf')
        self.arquivo_txt = Path('/local/do/arquivo.txt')
        self.arquivo_sem_ext = Path('/local/do/arquivo')
        self.lingua_spacy = 'pt_core_news_sm'

    # mockando aqui novamente para criar um objeto novo e não interferir nos
    # testes
    @patch('src.extrair_texto.PdfFileReader')
    @patch('src.extrair_texto.open')
    @patch('src.extrair_texto.processar')
    @patch('src.extrair_texto.configurar_nlp')
    def test_com_arquivo_pdf(
        self, configurar_nlp, processar, open, PdfFileReader
    ):
        leitor_pdf = PdfFileReader()
        leitor_pdf.numPages = 1
        leitor_pdf.getPage().extractText().strip.return_value = (
            'texto.\noutro texto.'
        )
        processar.return_value = ['texto.', 'outro texto.']
        esperado = [[0, ['texto.', 'outro texto.']]]
        resultado = extrair(self.arquivo_pdf, self.lingua_spacy)
        self.assertEqual(esperado, resultado)
    
    @patch('src.extrair_texto.open')
    @patch('src.extrair_texto.processar')
    @patch('src.extrair_texto.configurar_nlp')
    def test_com_arquivo_txt(
        self, configurar_nlp, processar, open
    ):
        open().__enter__().read.return_value = 'texto.\noutro texto.'
        processar.return_value = ['texto.', 'outro texto.']
        esperado = [[0, ['texto.', 'outro texto.']]]
        resultado = extrair(self.arquivo_txt, self.lingua_spacy)
        self.assertEqual(esperado, resultado)

    @patch('src.extrair_texto.open')
    @patch('src.extrair_texto.processar')
    @patch('src.extrair_texto.configurar_nlp')
    def test_com_arquivo_sem_extensao(
        self, configurar_nlp, processar, open
    ):
        open().__enter__().read.return_value = 'texto.\noutro texto.'
        processar.return_value = ['texto.', 'outro texto.']
        esperado = [[0, ['texto.', 'outro texto.']]]
        resultado = extrair(
            self.arquivo_sem_ext, self.lingua_spacy
        )
        self.assertEqual(esperado, resultado)


@patch('src.extrair_texto.processar', lambda texto: [texto])
@patch('src.extrair_texto.configurar_nlp')
class TestTratarTexto(TestCase):
    def test_trocando_caracter_de_traço(self, configurar_nlp):
        texto = 'um Œ texto qualquer.'
        esperado = [[0, ['um - texto qualquer.']]]
        resultado = tratar_texto([[0, texto]])
        self.assertEqual(esperado, resultado)

    def test_removendo_hifen_e_concatenando_palavas_que_foram_cortadas(
        self, configurar_nlp
    ):
        texto = 'texto co\n-\nrtado no meio.'
        esperado = [[0, ['texto cortado no meio.']]]
        resultado = tratar_texto([[0, texto]])
        self.assertEqual(esperado, resultado)
    
    def test_removendo_quebras_de_linha_quando_não_há_texto_a_seguir(
        self, configurar_nlp
    ):
        texto = 'texto\n quebrado no meio'
        esperado = [[0, ['texto quebrado no meio']]]
        resultado = tratar_texto([[0, texto]])
        self.assertEqual(esperado, resultado)
    
    def test_removendo_espaços_em_excesso(self, configurar_nlp):
        texto = 'texto  com muitos espaços'
        esperado = [[0, ['texto com muitos espaços']]]
        resultado = tratar_texto([[0, texto]])
        self.assertEqual(esperado, resultado)
    
    def test_removendo_hifen_e_concatenando_palavas_que_foram_cortadas2(
        self, configurar_nlp
    ):
        texto = 'texto co-\nrtado no meio.'
        esperado = [[0, ['texto cortado no meio.']]]
        resultado = tratar_texto([[0, texto]])
        self.assertEqual(esperado, resultado)