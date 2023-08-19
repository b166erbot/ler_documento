from pathlib import Path
from unittest import TestCase

from src.utils import ContagensFinitas, Porcento, recortar


# vou testar tudo nessa desgrama, cancei de fazer testes manuais.
# quando chegar no proximo/proximo_sem_restricao/definir_progresso, dá uma
# olhada.

class TestContagensFinitas(TestCase):
    def setUp(self):
        # indexes de 3 páginas com 4 linhas
        indexes = [[numero, 0, 3] for numero in range(3)]
        self.contagens = ContagensFinitas(indexes, Path('sei_la.py'))

    def test_proximo_retornando_um_slice_do_primeiro_texto(self):
        esperado = [slice(0, 1, None)] * 2
        resultado = self.contagens.proximo
        self.assertEqual(esperado, resultado)
    
    def test_proximo_retornando_um_slice_do_segundo_texto(self):
        esperado = [slice(0, 1, None), slice(1, 2, None)]
        self.contagens.proximo
        resultado = self.contagens.proximo
        self.assertEqual(esperado, resultado)

    def test_contagens_voltando_1_vez_e_retornando_a_contagem_aterior(self):
        contagem_antiga = self.contagens.contagem_atual
        contagem_nova = self.contagens._contagens[1]
        for i in range(5):
            self.contagens.proximo
        self.assertIs(self.contagens.contagem_atual, contagem_nova)
        self.contagens.anterior
        self.assertIs(self.contagens.contagem_atual, contagem_antiga)
    
    def test_contagens_passando_para_o_proximo_caso_avance_para_proxima_pagina(
        self
    ):
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        for i in range(4):
            self.contagens.proximo
        resultado = self.contagens.proximo
        self.assertEqual(esperado, resultado)
    
    def test_tem_proximo_retornando_true_caso_chegue_ao_final_da_pagina(self):
        for i in range(4):
            self.contagens.proximo
        self.assertTrue(self.contagens.tem_proximo)

    def test_proximo_sem_restricao_avancando_uma_pagina(self):
        contagem_anterior = self.contagens.contagem_atual
        for i in range(4):
            self.contagens.proximo_sem_restricao
        self.assertTrue(self.contagens.tem_proximo)
        self.contagens.proximo_sem_restricao
        nova_contagem = self.contagens.contagem_atual
        self.assertIsNot(contagem_anterior, nova_contagem)

    # ----/---- testes definir_progresso ----/----

    def test_progresso_indo_para_a_pagina_2_caso_a_pagina_seja_2(self):
        self.assertEqual(self.contagens.numero_atual, 0)
        self.contagens.definir_progresso([2, 0])
        self.assertEqual(self.contagens.numero_atual, 2)

    def test_progresso_indo_para_a_pagina_40_caso_a_pagina_seja_40(self):
        self.contagens = ContagensFinitas(
            [[numero, 0, 3] for numero in range(40)],
            Path('sei_lá.py')
        )
        self.assertEqual(self.contagens.numero_atual, 0)
        self.contagens.definir_progresso([39, 0])
        self.assertEqual(self.contagens.numero_atual, 39)

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
