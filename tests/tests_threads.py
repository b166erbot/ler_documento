from unittest import TestCase
from unittest.mock import patch, MagicMock


from src.threads import GerenciarFalas
from src.utils import ContagensFinitas


class TestGerenciarFalas(TestCase):
    @patch('src.threads.Temporizador')
    def setUp(self, temporizador):
        self.temporizador = temporizador
        páginas_indexes = [(número, 0, 4) for número in range(0, 4)]
        self.nome_arquivo = MagicMock()
        self.contagens = ContagensFinitas(páginas_indexes, self.nome_arquivo)
        self.gerenciar_falas = GerenciarFalas(self.contagens)
    
    # ---------// sair //---------

    @patch('src.threads.parar_fala')
    @patch('src.threads.salvar_progresso')
    def test_sair_salvando_progresso(
        self, salvar_progresso, parar_fala
    ):
        self.temporizador().ativar.assert_not_called()
        esperado = (
            self.nome_arquivo, [0, 0]
        )
        self.gerenciar_falas.sair()
        salvar_progresso.assert_called_with(*esperado)
        self.temporizador().ativar.assert_called_with(1)
        self.assertTrue(self.gerenciar_falas.sair_)
        parar_fala.assert_called_once()

    # ---------// resto_codigo_acao //---------

    @patch('src.threads.parar_fala')
    def test_resto_do_codigo_auxiliando_as_outras_funções(self, parar_fala):
        self.assertFalse(
            self.gerenciar_falas.contagens.contagem_atual.repetir_ao_passar_página
        )
        self.temporizador().ativar.assert_not_called()
        self.gerenciar_falas.resto_codigo_acao()
        self.assertTrue(
            self.gerenciar_falas.contagens.contagem_atual.repetir_ao_passar_página
        )
        self.temporizador().ativar.assert_called_with(1)
        parar_fala.assert_called_once()
    
    # ---------// voltar //---------
    
    @patch('src.threads.GerenciarFalas.resto_codigo_acao')
    def test_voltar_voltando_um_numero_na_contagem(self, resto_codigo_acao):
        self.gerenciar_falas.contagens.definir_progresso([1, 2])
        self.gerenciar_falas.contagens.contagem_atual.repetir = False
        self.gerenciar_falas.voltar()
        esperado = [1, 1]
        resultado = [
            self.gerenciar_falas.contagens.número_atual,
            self.gerenciar_falas.contagens.contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
        resto_codigo_acao.assert_called_once()
    
    # ---------// avançar //---------

    @patch('src.threads.GerenciarFalas.resto_codigo_acao')
    def test_avançar_avançando_um_numero_na_contagem(self, resto_codigo_acao):
        self.gerenciar_falas.contagens.definir_progresso([1, 2])
        self.gerenciar_falas.contagens.contagem_atual.repetir = False
        self.gerenciar_falas.avancar()
        esperado = [1, 3]
        resultado = [
            self.gerenciar_falas.contagens.número_atual,
            self.gerenciar_falas.contagens.contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
        resto_codigo_acao.assert_called_once()
    
    # ---------// avançar_página //---------

    @patch('src.threads.GerenciarFalas.resto_codigo_acao')
    def test_avançar_página_avançando_um_numero_na_contagem(
        self, resto_codigo_acao
    ):
        self.gerenciar_falas.contagens.definir_progresso([1, 2])
        self.gerenciar_falas.contagens.contagem_atual.repetir = False
        self.gerenciar_falas.avancar_página()
        esperado = [2, 0]
        resultado = [
            self.gerenciar_falas.contagens.número_atual,
            self.gerenciar_falas.contagens.contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
        resto_codigo_acao.assert_called_once()
    
    # ---------// voltar_página //---------

    @patch('src.threads.GerenciarFalas.resto_codigo_acao')
    def test_voltar_página_voltando_um_numero_na_contagem(
        self, resto_codigo_acao
    ):
        self.gerenciar_falas.contagens.definir_progresso([1, 2])
        self.gerenciar_falas.contagens.contagem_atual.repetir = False
        self.gerenciar_falas.voltar_página()
        esperado = [0, 0]
        resultado = [
            self.gerenciar_falas.contagens.número_atual,
            self.gerenciar_falas.contagens.contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
        resto_codigo_acao.assert_called_once()
    

class TestGerenciarFalasMétodoGerenciarFalas(TestCase):
    @patch('src.threads.Temporizador')
    def setUp(self, temporizador):
        self.textos = MagicMock()
        self.argumentos = MagicMock()
        self.tela_boas_vindas = MagicMock()
        self.temporizador = temporizador
        páginas_indexes = [(número, 0, 4) for número in range(0, 4)]
        self.nome_arquivo = MagicMock()
        self.contagens = ContagensFinitas(páginas_indexes, self.nome_arquivo)
        self.gerenciar_falas = GerenciarFalas(self.contagens)
    
    @patch('src.threads.parar_fala')
    @patch('src.threads.falar')
    @patch('src.threads.sleep')
    def test_gerenciar_falas_saindo_caso_o_mesmo_método_esteja_rodando(
        self, sleep, falar, parar_fala
    ):
        self.tela_boas_vindas._variaveis_compartilhadas.__getitem__.return_value = True
        self.gerenciar_falas.gerenciar_falas(
            self.textos, self.argumentos, self.tela_boas_vindas
        )
        self.tela_boas_vindas._variaveis_compartilhadas.__setitem__.assert_not_called()
    
    @patch('src.threads.parar_fala')
    @patch('src.threads.falar')
    @patch('src.threads.sleep')
    def test_gerenciar_falas_definindo_variável_rodando_falas_true_caso_variável_false(
        self, sleep, falar, parar_fala
    ):
        self.tela_boas_vindas._variaveis_compartilhadas.__getitem__.return_value = False
        esperado = [('rodando falas', True), ('rodando falas', False)]
        self.gerenciar_falas.gerenciar_falas(
            self.textos, self.argumentos, self.tela_boas_vindas
        )
        chamadas = self.tela_boas_vindas._variaveis_compartilhadas.__setitem__.call_args_list
        resultado = list(map(lambda chamada: list(chamada)[0], chamadas))
        self.assertEqual(esperado, resultado)
    
    @patch('src.threads.parar_fala')
    @patch('src.threads.falar')
    @patch('src.threads.sleep')
    def test_gerenciar_falas_parando_caso_variável_sair_for_true(
        self, sleep, falar, parar_fala
    ):
        self.gerenciar_falas.sair_ = True
        self.tela_boas_vindas._variaveis_compartilhadas.__getitem__.return_value = False
        self.gerenciar_falas.gerenciar_falas(
            self.textos, self.argumentos, self.tela_boas_vindas
        )
        self.tela_boas_vindas._atualizar_label_sentenças.assert_not_called()