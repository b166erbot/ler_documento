from unittest import TestCase

from src.utils import ContagensFinitas, recortar


class TestContagensFinitas(TestCase):
    def setUp(self):
        # indexes de 3 páginas com 4 linhas
        indexes = [[numero, 0, 3] for numero in range(3)]
        self.contagens = ContagensFinitas(indexes)

    def test_contagens_voltando_1_vez_e_retornando_a_contagem_aterior(self):
        contagem_antiga = self.contagens.contagem_atual
        contagem_nova = self.contagens._contagens[1]
        self.contagens.proximo
        self.contagens.proximo
        self.contagens.proximo
        self.contagens.proximo
        self.contagens.proximo
        self.assertIs(self.contagens.contagem_atual, contagem_nova)
        self.contagens.anterior
        self.assertIs(self.contagens.contagem_atual, contagem_antiga)


class TestRecortar(TestCase):
    def test_retornando_lista_dividida_por_2(self):
        esperado = [['oi', 'ola']] * 3
        resultado = recortar(['oi', 'ola'] * 3, 2)
        self.assertEqual(esperado, resultado)
    
    def test_retornando_lista_dividida_por_2_com_lista_impar(self):
        esperado = [['oi', 'ola'], ['3', 'hello'], ['oi']]
        resultado = recortar(['oi', 'ola', '3', 'hello', 'oi'], 2)
        self.assertEqual(esperado, resultado)
