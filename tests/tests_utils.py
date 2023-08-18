from pathlib import Path
from unittest import TestCase

from src.utils import ContagensFinitas, Porcento, recortar


class TestContagensFinitas(TestCase):
    def setUp(self):
        # indexes de 3 páginas com 4 linhas
        indexes = [[numero, 0, 3] for numero in range(3)]
        self.contagens = ContagensFinitas(indexes, Path('sei_la.py'))

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
    
    def test_contagens_passando_para_o_proximo_caso_avance_para_proxima_pagina(
        self
    ):
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        self.contagens.proximo
        self.contagens.proximo
        self.contagens.proximo
        self.contagens.proximo
        resultado = self.contagens.proximo
        self.assertEqual(esperado, resultado)


class TestRecortar(TestCase):
    def test_retornando_lista_dividida_por_2(self):
        esperado = [['oi', 'ola']] * 3
        resultado = recortar(['oi', 'ola'] * 3, 2)
        self.assertEqual(esperado, resultado)
    
    def test_retornando_lista_dividida_por_2_com_lista_impar(self):
        esperado = [['oi', 'ola'], ['3', 'hello'], ['oi']]
        resultado = recortar(['oi', 'ola', '3', 'hello', 'oi'], 2)
        self.assertEqual(esperado, resultado)


class TestPorcento(TestCase):
    def setUp(self):
        self.porcentagem = Porcento(200, 0)
    
    def test_retornando_15_caso_o_numero_antigo_seja_0(self):
        esperado = 15
        resultado = self.porcentagem.calcular(30)
        self.assertEqual(esperado, resultado)

    def test_retornando_1_caso_o_numero_antigo_seja_30_e_porcento_ja_calculou(
        self
    ):
        esperado = 1
        resultado = self.porcentagem.calcular(30)
        self.assertEqual(15, resultado)
        resultado = self.porcentagem.calcular(32)
        self.assertEqual(esperado, resultado)
    
    def test_retornando_menos_1_caso_o_numero_antigo_seja_30_e_porcento_ja_calculou(
        self
    ):
        esperado = -1
        resultado = self.porcentagem.calcular(30)
        self.assertEqual(15, resultado)
        resultado = self.porcentagem.calcular(28)
        self.assertEqual(esperado, resultado)
    
    def test_retornando_porcentagem_atual_0(self):
        esperado = 0
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
    
    def test_retornando_porcentagem_atual_15(self):
        esperado = 15
        self.porcentagem.calcular(30)
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
