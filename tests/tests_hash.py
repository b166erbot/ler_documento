from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock
from hashlib import sha256

from src.hash import hashear_arquivo


class TestHashearArquivo(TestCase):
    @patch('src.hash.open', mock_open(read_data = b'ala um canguru voando!'))
    def test_retornando_o_hash_de_um_arquivo(self):
        mensagem = b'ala um canguru voando!'
        local_arquivo = MagicMock()
        local_arquivo.exists.return_value = True
        local_arquivo.is_file.return_value = True
        esperado = sha256(mensagem).hexdigest()
        resultado = hashear_arquivo(local_arquivo)
        self.assertEqual(esperado, resultado)
        # o canguru tá voando 😃
    
    def test_estourando_um_erro_caso_local_arquivo_não_exista(self):
        local_arquivo = MagicMock()
        local_arquivo.exists.return_value = False
        local_arquivo.is_file.return_value = True
        with self.assertRaises(FileNotFoundError):
            hashear_arquivo(local_arquivo)
    
    def test_estourando_um_erro_caso_local_arquivo_não_seja_arquivo(self):
        local_arquivo = MagicMock()
        local_arquivo.exists.return_value = True
        local_arquivo.is_file.return_value = False
        with self.assertRaises(FileNotFoundError):
            hashear_arquivo(local_arquivo)
        
    def test_estourando_um_erro_caso_local_arquivo_não_exista_e_não_seja_arquivo(
        self
    ):
        local_arquivo = MagicMock()
        local_arquivo.exists.return_value = False
        local_arquivo.is_file.return_value = False
        with self.assertRaises(FileNotFoundError):
            hashear_arquivo(local_arquivo)