from unittest import TestCase
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.salvar import (
    salvar, obter_texto, salvar_progresso, carregar_progresso, existe_arquivo
)


class TestSalvar(TestCase):
    @patch('src.salvar.shelve')
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.Path')
    def test_estourando_erro_caso_local_da_pasta_arquivos_exista_e_não_seja_uma_pasta(
        self, path, hashear_arquivo, shelve
    ):
        path().exists.return_value = True
        path().is_dir.return_value = False
        with self.assertRaises(IsADirectoryError):
            salvar('', '')
    
    @patch('src.salvar.shelve')
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.Path')
    def test_não_estourando_um_erro_caso_local_da_pasta_arquivos_exista_e_seja_uma_pasta(
        self, path, hashear_arquivo, shelve
    ):
        path().exists.return_value = True
        path().is_dir.return_value = True
        salvar('', '')
    
    @patch('src.salvar.shelve')
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.Path')
    def test_não_estourando_um_erro_caso_local_da_pasta_arquivos_não_exista(
        self, path, hashear_arquivo, shelve
    ):
        path().exists.return_value = False
        salvar('', '')
    
    @patch('src.salvar.shelve')
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.Path')
    def test_criando_pasta_arquivos_caso_pasta_não_exista(
        self, path, hashear_arquivo, shelve
    ):
        path().exists.side_effect = [False, False]
        path().is_dir.side_effect = [False, False]
        salvar('', '')
        path().mkdir.assert_called_once()

    @patch('src.salvar.shelve')
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.Path')
    def test_salvando_o_conteúdo_no_shelve(self, path, hashear_arquivo, shelve):
        path().exists.return_value = False
        path().is_dir.return_value = False
        hash_do_arquivo = 'olá'
        hashear_arquivo.return_value = hash_do_arquivo
        textos = ['isso daqui é uma prova de que minas tem pão de queijo.']
        salvar(textos, '')
        shelve.open().__enter__().__setitem__.assert_called_with(
            hash_do_arquivo, textos
        )


class TestObterTexto(TestCase):
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.shelve.open')
    @patch('src.salvar.Path')
    def test_obtendo_o_texto_do_arquivo_caso_arquivo_exista_e_é_um_arquivo(
        self, path, open, hashear_arquivo
    ):
        hashear_arquivo.return_value = 'hash_do_arquivo'
        path().__truediv__().exists.return_value = True
        path().__truediv__().is_file.return_value = True
        open().__enter__().get.return_value = 'pão'
        esperado = 'pão'
        resultado = obter_texto(Path('pão.pdf'))
        self.assertEqual(esperado, resultado)
    
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.shelve.open')
    @patch('src.salvar.Path')
    def test_não_obtendo_o_texto_caso_arquivo_não_exista(
        self, path, open, hashear_arquivo
    ):
        hashear_arquivo.return_value = 'hash_do_arquivo'
        path().__truediv__().exists.return_value = False
        path().__truediv__().is_file.return_value = True
        self.assertIsNone(obter_texto(Path('pão.pdf')))
    
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.shelve.open')
    @patch('src.salvar.Path')
    def test_não_obtendo_o_texto_caso_arquivo_não_seja_um_arquivo(
        self, path, open, hashear_arquivo
    ):
        hashear_arquivo.return_value = 'hash_do_arquivo'
        path().__truediv__().exists.return_value = True
        path().__truediv__().is_file.return_value = False
        self.assertIsNone(obter_texto(Path('pão.pdf')))
    
    @patch('src.salvar.hashear_arquivo')
    @patch('src.salvar.shelve.open')
    @patch('src.salvar.Path')
    def test_não_obtendo_o_texto_caso_todas_as_condições_sejam_false(
        self, path, open, hashear_arquivo
    ):
        hashear_arquivo.return_value = 'hash_do_arquivo'
        path().__truediv__().exists.return_value = False
        path().__truediv__().is_file.return_value = False
        self.assertIsNone(obter_texto(Path('pão.pdf')))


class TestSalvarProgresso(TestCase):
    @patch('src.salvar.hashear_arquivo', return_value = 'hash')
    @patch('src.salvar.shelve.open')
    def test_salvando_progresso(self, open, hashear_arquivo):
        progresso = [2, 3]
        salvar_progresso('pão', progresso)
        open().__enter__().__setitem__.assert_called_with('hash', progresso)
    
class TestCarregarProgresso(TestCase):
    @patch('src.salvar.shelve.open')
    @patch('src.salvar.hashear_arquivo', return_value = 'hash')
    def test_retornando_progresso(self, hashear_arquivo, open):
        esperado = 'retorno'
        open().__enter__().get.return_value = esperado
        resultado = carregar_progresso('pão')
        self.assertEqual(esperado, resultado)
    

    @patch('src.salvar.shelve.open')
    @patch('src.salvar.hashear_arquivo', return_value = 'hash')
    def test_retornando_progresso(self, hashear_arquivo, open):
        esperado = None
        open().__enter__().get.return_value = esperado
        resultado = carregar_progresso('pão')
        self.assertEqual(esperado, resultado)


class TestExisteArquivo(TestCase):
    def test_retornando_true_caso_todas_as_condições_sejam_true(self):
        local_arquivo = MagicMock()
        local_arquivo.is_file.return_value = True
        local_arquivo.exists.return_value = True
        self.assertTrue(existe_arquivo(local_arquivo))
    
    def test_retornando_false_caso_local_arquivo_não_é_arquivo(self):
        local_arquivo = MagicMock()
        local_arquivo.is_file.return_value = False
        local_arquivo.exists.return_value = True
        self.assertFalse(existe_arquivo(local_arquivo))
    
    def test_retornando_false_caso_local_arquivo_não_existe(self):
        local_arquivo = MagicMock()
        local_arquivo.is_file.return_value = True
        local_arquivo.exists.return_value = False
        self.assertFalse(existe_arquivo(local_arquivo))
    
    def test_retornando_false_caso_todas_as_condições_sejam_false(self):
        local_arquivo = MagicMock()
        local_arquivo.is_file.return_value = False
        local_arquivo.exists.return_value = False
        self.assertFalse(existe_arquivo(local_arquivo))