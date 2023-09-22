from unittest import TestCase
from unittest.mock import MagicMock, patch

# mockando o load e download aqui pois não quero que ele demore na importação
load = MagicMock()
download = MagicMock()
patch('spacy.load', load).start()
patch('spacy.cli.download', download).start()

from src.processar_texto import configurar_nlp, processar


class TestConfigurarNlp(TestCase):
    #mockando novamente pois quero que cada load e download sejam novos
    @patch('src.processar_texto.load')
    def test_load_carregando_caso_tenha_a_lingua_selecionada(self, load):
        configurar_nlp('pão')
        load.assert_called_once()
        # tem a língua pão 😃
    
    @patch('src.processar_texto.download')
    @patch('src.processar_texto.load', side_effect = [OSError, ''])
    def test_baixando_e_carregando_a_lingua_caso_não_tenha_a_lingua_disponível(
        self, load, download
    ):
        configurar_nlp('pão')
        self.assertEqual(load.call_count, 2)
        download.assert_called_once()
        # deu erro mas ainda tem a língua pão 😃


class TestProcessar(TestCase):
    @patch('src.processar_texto.nlp')
    def test_processar_retornando_os_textos_das_sentenças(self, nlp):
        nlp().sents = [MagicMock(text = texto) for texto in ['pão'] * 3]
        esperado = ['pão'] * 3
        # é necessário transformar em lista pois ele retorna um map
        resultado = list(processar(
            'tanto faz esse texto aqui, não influencia no teste.'
        ))
        self.assertEqual(esperado, resultado)