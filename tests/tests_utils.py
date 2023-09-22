from pathlib import Path
from unittest import TestCase, skip
from unittest.mock import MagicMock, patch

from src.utils import (
    ContagemFinita, ContagensFinitas, Porcento, Temporizador, colorir,
    está_instalado, páginas_invalidas, recortar, tratar_páginas_usuario)


class TestContagensFinitas(TestCase):
    def setUp(self):
        # indexes de 3 páginas com 4 linhas
        indexes = [[número, 0, 3] for número in range(3)]
        self.contagens = ContagensFinitas(indexes, Path('sei_la.py'))

    # ---------// próximo //---------

    def test_próximo_retornando_a_primeira_lista_slice(self):
        esperado = [slice(0, 1, None)] * 2
        resultado = self.contagens.próximo
        self.assertEqual(esperado, resultado)
    
    def test_próximo_retornando_a_segunda_lista_slice(self):
        esperado = [slice(0, 1, None), slice(1, 2, None)]
        self.contagens.próximo
        resultado = self.contagens.próximo
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagemFinita.tem_próximo', False)
    @patch('src.utils.ContagensFinitas.tem_proxima_página', False)
    def test_próximo_repetindo_o_retorno_caso_não_tenha_mais_próximo(
        self
    ):
        self.contagens.definir_progresso([2, 0])
        esperado = self.contagens.próximo
        for _ in range(4):
            self.contagens.próximo
        resultado = self.contagens.próximo
        self.assertEqual(esperado, resultado)
    
    def test_próximo_passando_para_a_proxima_página_caso_chegue_no_fim_da_contagem(
        self
    ):
        for _ in range(4):
            self.contagens.próximo
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        resultado = self.contagens.próximo
        self.assertEqual(esperado, resultado)
    
    # ---------// próximo_sem_restrição //---------

    def test_próximo_sem_restrição_retornando_a_primeira_list_slice(
        self
    ):
        esperado = [slice(0, 1, None), slice(0, 1, None)]
        resultado = self.contagens.próximo_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def text_próximo_sem_restrição_retornando_a_segunda_lista_slice(self):
        esperado = [slice(0, 1, None), slice(1, 2, None)]
        self.contagens.próximo_sem_restrição
        resultado = self.contagens.próximo_sem_restrição
        self.assertNotEqual(esperado, resultado)
    
    @patch('src.utils.ContagensFinitas.tem_proxima_página', False)
    @patch('src.utils.ContagemFinita.tem_próximo_sem_restrição', False)
    def test_próximo_sem_restrição_repetindo_o_retorno_caso_não_tenha_mais_próximo(
        self
    ):
        self.contagens.definir_progresso([2, 0])
        for _ in range(4):
            self.contagens.próximo_sem_restrição
        esperado = self.contagens.próximo_sem_restrição
        resultado = self.contagens.próximo_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def test_próximo_sem_restrição_passando_para_a_proxima_página_caso_chegue_no_fim_da_contagem(
        self
    ):
        for _ in range(4):
            self.contagens.próximo_sem_restrição
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        resultado = self.contagens.próximo_sem_restrição
        self.assertEqual(esperado, resultado)

    # ---------// anterior //---------

    def test_anterior_retornando_a_última_lista_caso_esteja_no_fim(self):
        self.contagens.definir_progresso([2, 3])
        esperado = [slice(2, 3, None), slice(3, 4, None)]
        resultado = self.contagens.anterior
        self.assertEqual(esperado, resultado)
    
    def test_anterior_retornando_a_penultima_lista_caso_esteja_no_fim(self):
        self.contagens.definir_progresso([2, 3])
        self.contagens.anterior
        esperado = [slice(2, 3), slice(2, 3, None)]
        resultado = self.contagens.anterior
        self.assertEqual(esperado, resultado)

    @patch('src.utils.ContagemFinita.tem_anterior', False)
    @patch('src.utils.ContagensFinitas.tem_página_anterior', False)
    def test_anterior_repetindo_o_retorno_caso_não_tenha_mais_anterior(self):
        esperado = [slice(0, 1, None), slice(0, 1, None)]
        resultado = self.contagens.anterior
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagemFinita.tem_anterior', False)
    def test_anterior_não_passando_para_a_lista_slice_anterior(
        self
    ):
        self.contagens.contagem_atual.repetir = True
        esperado = self.contagens.anterior
        self.contagens.contagem_atual.repetir = True
        resultado = self.contagens.anterior
        self.assertEqual(esperado, resultado)
    
    def test_anterior_retornando_para_a_página_anterior_caso_chegue_no_fim_da_contagem(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        for _ in range(4):
            self.contagens.anterior
        esperado = [slice(1, 2, None), slice(3, 4, None)]
        resultado = self.contagens.anterior
        self.assertEqual(esperado, resultado)

    # ---------// anterior_sem_restrição //---------

    def test_anterior_sem_restrição_retornando_a_última_lista_caso_esteja_no_fim(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        esperado = [slice(2, 3, None), slice(3, 4, None)]
        resultado = self.contagens.anterior_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def test_anterior_sem_restrição_retornando_a_penultima_lista_caso_esteja_no_fim(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        esperado = [slice(2, 3, None), slice(2, 3, None)]
        self.contagens.anterior_sem_restrição
        resultado = self.contagens.anterior_sem_restrição
        self.assertEqual(esperado, resultado)

    @patch('src.utils.ContagemFinita.tem_anterior_sem_restrição', False)
    def test_anterior_sem_restrição_repetindo_o_retorno_caso_não_tenha_mais_anterior(self):
        # self.contagens.contagem_atual.repetir = False
        esperado = [slice(0, 1, None), slice(0, 1, None)]
        self.contagens.anterior_sem_restrição
        resultado = self.contagens.anterior_sem_restrição
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagemFinita.tem_anterior', False)
    def test_anterior_sem_restrição_não_passando_para_a_lista_slice_anterior(
        self
    ):
        self.contagens.contagem_atual.repetir = True
        esperado = self.contagens.anterior_sem_restrição
        self.contagens.contagem_atual.repetir = True
        resultado = self.contagens.anterior_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def test_anterior_sem_restrição_retornando_para_a_página_anterior_caso_chegue_no_fim_da_contagem(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        for _ in range(4):
            self.contagens.anterior_sem_restrição
        esperado = [slice(1, 2, None), slice(3, 4, None)]
        resultado = self.contagens.anterior_sem_restrição
        self.assertEqual(esperado, resultado)

    # ---------// tem_próximo //---------

    @patch('src.utils.ContagemFinita.tem_próximo', True)
    def test_tem_próximo_retornando_true_caso_contagem_atual_tenha_um_próximo(
        self
    ):
        self.contagens.número_atual = float('inf')
        resultado = self.contagens.tem_próximo
        self.assertTrue(resultado)
    
    @patch('src.utils.ContagemFinita.tem_próximo', False)
    def test_tem_próximo_retornando_true_caso_número_atual_seja_menor_que_número_final(
        self
    ):
        self.assertTrue(self.contagens.tem_próximo)
    
    @patch('src.utils.ContagemFinita.tem_próximo', False)
    def test_tem_próximo_retornando_false_caso_nao_tenha_próximo_na_contgem_e_número_atual_maior_ao_número_final(
        self
    ):
        self.contagens.número_atual = float('inf')
        self.assertFalse(self.contagens.tem_próximo)
    
    @patch('src.utils.ContagemFinita.tem_próximo', True)
    def test_tem_próximo_retornando_true_caso_em_todos_os_casos_retorne_true(
        self
    ):
        self.assertTrue(self.contagens.tem_próximo)

    # ---------// proxima_página //---------

    @patch('src.utils.ContagensFinitas.tem_proxima_página', True)
    def test_proxima_página_retornando_proxima_lista_slice(self):
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        resultado = self.contagens.proxima_página
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagensFinitas.tem_proxima_página', True)
    def test_proxima_página_retornando_segunda_lista_caso_chamado_duas_vezes(
        self
    ):
        esperado = [slice(2, 3, None), slice(0, 1, None)]
        self.contagens.proxima_página
        resultado = self.contagens.proxima_página
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagensFinitas.tem_proxima_página', False)
    def test_proxima_página_retornando_o_final_da_lista_caso_nao_tenha_proxima_página(
        self
    ):
        esperado = [slice(0, 1, None), slice(3, 4, None)]
        resultado1 = self.contagens.proxima_página
        resultado2 = self.contagens.proxima_página
        self.assertEqual(esperado, resultado1)
        self.assertEqual(esperado, resultado2)

    # ---------// página_anterior //---------

    def test_página_anterior_retornando_ultima_lista_no_inicio_caso_repetir_true(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        esperado = [slice(2, 3, None), slice(0, 1, None)]
        resultado = self.contagens.página_anterior
        self.assertEqual(esperado, resultado)
    
    def test_página_anterior_retornando_penultima_lista_no_inicio_caso_repetir_true(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        self.contagens.página_anterior
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        resultado = self.contagens.página_anterior
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagensFinitas.tem_página_anterior', True)
    def test_página_anterior_retornando_última_lista_anterior_slice_caso_tem_página_anterior_true(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        self.contagens.repetir = False
        esperado = [slice(1, 2, None), slice(0, 1, None)]
        resultado = self.contagens.página_anterior
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagensFinitas.tem_página_anterior', True)
    def test_página_anterior_retornando_penultima_lista_anterior_caso_tem_página_anterior_true(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        self.contagens.repetir = False
        self.contagens.página_anterior
        esperado = [slice(0, 1, None), slice(0, 1, None)]
        resultado = self.contagens.página_anterior
        self.assertEqual(resultado, esperado)
    
    @patch('src.utils.ContagensFinitas.tem_página_anterior', False)
    def test_página_anterior_retornando_a_mesma_página_caso_tem_página_anterior_false(
        self
    ):
        self.contagens.repetir = False
        esperado = self.contagens.página_anterior
        resultado = self.contagens.página_anterior
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.ContagensFinitas.tem_página_anterior', False)
    def test_página_anterior_retornando_no_inicio_da_página_caso_tem_página_anterior_false(
        self
    ):
        self.contagens.definir_progresso([0, 3])
        self.contagens.repetir = False
        esperado = [slice(0, 1, None), slice(0, 1, None)]
        resultado = self.contagens.página_anterior
        self.assertEqual(esperado, resultado)

    # ---------// tem_proxima_página //---------

    def test_tem_proxima_página_retornando_true_caso_número_atual_menor_número_final(
        self
    ):
        self.assertTrue(self.contagens.tem_proxima_página)
    
    def test_tem_proxima_página_retornando_false_caso_número_atual_igual_número_final(
        self
    ):
        self.contagens.número_atual = self.contagens._número_final
        self.assertFalse(self.contagens.tem_proxima_página)

    # ---------// tem_página_anterior //---------

    def test_tem_página_anterior_retornando_true_caso_número_atual_maior_número_inicial(
        self
    ):
        self.contagens.número_atual = float('inf')
        self.assertTrue(self.contagens.tem_página_anterior)
    
    def test_tem_página_anterior_retornando_false_caso_número_atual_igual_número_inicial(
        self
    ):
        self.contagens.número_atual = self.contagens._número_inicial
        self.assertFalse(self.contagens.tem_página_anterior)

    # ---------// atualizar_contagens //---------

    def test_atualizando_as_contagens(self):
        páginas_indexes = [[número, 0, 4] for número in range(4)]
        nome_arquivo = Path('seilá2.py')
        self.contagens.atualizar_contagens(páginas_indexes, nome_arquivo)
        for contagem in self.contagens._contagens.values():
            self.assertIsInstance(contagem, ContagemFinita)
        self.assertEqual(len(self.contagens._contagens), 4)

    # ---------// definir_progresso //---------

    def test_definir_progresso_definindo_página_e_sentença_caso_progresso_seja_lista_2_3(
        self
    ):
        self.contagens.definir_progresso([2, 3])
        esperado = [2, 3]
        resultado = [
            self.contagens.número_atual,
            self.contagens.contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
    
    def test_definir_progresso_definindo_página_caso_progresso_seja_lista_2_none(
        self
    ):
        self.contagens.definir_progresso([2, None])
        esperado = 2
        resultado = self.contagens.número_atual
        self.assertEqual(esperado, resultado)
    
    def test_definir_progresso_definindo_sentença_caso_progresso_seja_lista_none_3(
        self
    ):
        self.contagens.definir_progresso([None, 3])
        esperado = 3
        resultado = self.contagens.contagem_atual.número_atual
        self.assertEqual(esperado, resultado)
    
    def test_definir_progresso_definindo_para_o_inicio_caso_progresso_seja_lista_0_0(
        self
    ):
        self.contagens.definir_progresso([0, 0])
        esperado = [0, 0]
        resultado = [
            self.contagens.número_atual,
            self.contagens.contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
    
    def test_definir_progresso_voltando_a_contagem_para_o_inicio_caso_progresso_seja_lista_2_0(
        self
    ):
        # range = páginas, lista = linhas
        indexes = [[número, 0, 3] for número in range(5)]
        self.contagens = ContagensFinitas(indexes, Path('sei_la.py'))
        self.contagens.definir_progresso([2, 0])
        for número in range(2, 5):
            contagem = self.contagens._contagens[número]
            self.assertEqual(contagem.número_atual, contagem._número_inicial)
    
    def test_definir_progresso_voltando_a_contagem_para_o_final_caso_progresso_seja_list_2_0(
        self
    ):
        # range = páginas, lista = linhas
        indexes = [[número, 0, 3] for número in range(5)]
        self.contagens = ContagensFinitas(indexes, Path('sei_la.py'))
        self.contagens.definir_progresso([2, 0])
        for número in range(2):
            contagem = self.contagens._contagens[número]
            self.assertEqual(contagem.número_atual, contagem._número_final)

    # ---------// _definir_progresso_páginas //---------

    # não irei testar pois já testei no "definir_progresso"

    # ---------// _definir_progresso_sentença //---------

    # não irei testar pois já testei no "definir_progresso"

    # ---------// número_atual_ //---------

    def test_número_atual_retornando_7_caso_progresso_seja_1_3(self):
        self.contagens.definir_progresso([1, 3])
        esperado = 7
        resultado = self.contagens.número_atual_
        self.assertEqual(esperado, resultado)

    def test_número_atual_retornando_11_caso_progresso_seja_2_3(self):
        self.contagens.definir_progresso([2, 3])
        esperado = 11
        resultado = self.contagens.número_atual_
        self.assertEqual(esperado, resultado)
    
    def test_número_atual_retornando_0_caso_progresso_seja_0_0(self):
        self.contagens.definir_progresso([0, 0])
        esperado = 0
        resultado = self.contagens.número_atual_
        self.assertEqual(esperado, resultado)

    # ---------// número_maximo //---------
    
    def test_número_maximo_retornando_o_total(self):
        self.assertEqual(self.contagens.número_maximo, 11)

    # ---------// finalizou //---------

    def test_finalizou_retornando_false_caso_não_finalizou(self):
        self.assertFalse(self.contagens.finalizou)
    
    def test_finalizou_retornando_true_caso_finalizou(self):
        self.contagens.definir_progresso([2, 3])
        self.assertTrue(self.contagens.finalizou)

class TestRecortar(TestCase):
    def test_retornando_lista_dividida_por_2(self):
        esperado = [['oi', 'ola']] * 3
        resultado = recortar(['oi', 'ola'] * 3, 2)
        self.assertEqual(esperado, resultado)
    
    def test_retornando_lista_dividida_por_2_com_lista_impar(self):
        esperado = [['oi', 'ola'], ['3', 'hello'], ['oi']]
        resultado = recortar(['oi', 'ola', '3', 'hello', 'oi'], 2)
        self.assertEqual(esperado, resultado)
    
    def test_retornand_lista_dividida_por_1(self):
        esperado = [['oi']] * 5
        resultado = recortar(['oi'] * 5, 1)
        self.assertEqual(esperado, resultado)


class TestContagemFinita(TestCase):
    # quem controla a classe ContagemFinita é a ContagensFinitas. Lembre-se
    # disso quando for fazer os testes para a classe ContagemFinita.
    def setUp(self):
        self.contagem = ContagemFinita(0, 4)
    
    # ---------// próximo //---------

    def test_próximo_retornando_o_primeiro_número(self):
        esperado = 0
        resultado = self.contagem.próximo
        self.assertEqual(esperado, resultado)
    
    def test_próximo_retornando_o_segundo_número(self):
        self.contagem.próximo
        # é necessário mudar o repetir para false.
        self.contagem.repetir = False
        esperado = 1
        resultado = self.contagem.próximo
        self.assertEqual(esperado, resultado)
    
    def test_próximo_retornando_o_último_número(self):
        self.contagem.repetir = False
        for _ in range(4):
            self.contagem.próximo
        esperado = 4
        resultado = self.contagem.próximo
        self.assertEqual(esperado, resultado)
    
    def test_próximo_repetindo_o_retorno_caso_chegue_no_fim(self):
        self.contagem.repetir = False
        for _ in range(5):
            self.contagem.próximo
        esperado = 4
        resultado = self.contagem.próximo
        self.assertEqual(esperado, resultado)
    
    def test_próximo_retornando_o_mesmo_número_2_vezes_caso_repetir_true(self):
        esperado = 0
        resultado1 = self.contagem.próximo
        resultado2 = self.contagem.próximo
        self.assertEqual(esperado, resultado1)
        self.assertEqual(esperado, resultado2)
    
    def test_próximo_retornando_o_mesmo_número_1_vez_caso_repetir_ao_passar_página_true(
        self
    ):
        self.contagem.repetir = False
        self.contagem.repetir_ao_passar_página = True
        esperado = 0
        resultado1 = self.contagem.próximo
        resultado2 = self.contagem.próximo
        self.assertEqual(esperado, resultado1)
        self.assertNotEqual(esperado, resultado2)
    
    def test_próximo_retornando_o_mesmo_número_2_vezes_caso_repetir_e_repetir_ao_passar_página_true(
        self
    ):
        self.contagem.repetir_ao_passar_página = True
        esperado = 0
        resultado1 = self.contagem.próximo
        resultado2 = self.contagem.próximo
        self.assertEqual(esperado, resultado1)
        self.assertEqual(esperado, resultado2)
    
    # ---------// próximo_sem_restrição //---------

    def test_próximo_sem_restrição_retornando_o_primeiro_número(self):
        esperado = 0
        resultado = self.contagem.próximo_sem_restrição
        self.assertEqual(esperado, resultado)

    def test_próximo_sem_restrição_retornando_o_segundo_número_caso_repetir_false(
        self
    ):
        self.contagem.repetir = False
        esperado = 2
        self.contagem.próximo_sem_restrição
        resultado = self.contagem.próximo_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def test_próximo_sem_restrição_retornando_último_número_caso_repetir_false(self):
        self.contagem.repetir = False
        for _ in range(4):
            self.contagem.próximo_sem_restrição
        esperado = 4
        resultado = self.contagem.próximo_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def test_próximo_sem_restrição_repetindo_o_retorno_caso_chegue_no_fim(self):
        self.contagem.repetir = False
        for _ in range(5):
            self.contagem.próximo_sem_restrição
        esperado = 4
        resultado = self.contagem.próximo_sem_restrição
        self.assertEqual(esperado, resultado)
    
    def test_próximo_sem_restrição_retornando_o_número_2_vezes_caso_repetir_true(
        self
    ):
        self.contagem.próximo_sem_restrição
        esperado = 0
        resultado = self.contagem.próximo_sem_restrição
        self.assertEqual(esperado, resultado)
    
    # ---------// anterior //---------

    def test_anterior_retornando_o_último_número_caso_repetir_false(self):
        self.contagem.número_atual = 4
        self.contagem.repetir = False
        esperado = 3
        resultado = self.contagem.anterior
        self.assertEqual(esperado, resultado)
    
    def test_anterior_retornando_o_penúltimo_caso_repetir_false(self):
        self.contagem.número_atual = 4
        self.contagem.repetir = False
        self.contagem.anterior
        esperado = 2
        resultado = self.contagem.anterior
        self.assertEqual(esperado, resultado)
    
    def test_anterior_retornando_o_primeiro_número_caso_repetir_false(self):
        self.contagem.número_atual = 4
        self.contagem.repetir = False
        for _ in range(3):
            self.contagem.anterior
        esperado = 0
        resultado = self.contagem.anterior
        self.assertEqual(esperado, resultado)
    
    def test_anterior_repetindo_o_retorno_caso_chegue_ao_início(self):
        self.contagem.número_atual = 4
        self.contagem.repetir = False
        for _ in range(4):
            self.contagem.anterior
        esperado = 0
        resultado = self.contagem.anterior
        self.assertEqual(esperado, resultado)
    
    def test_anterior_retornando_o_número_2_vezes_caso_repetir_true(self):
        self.contagem.número_atual = 4
        esperado = 4
        resultado1 = self.contagem.anterior
        resultado2 = self.contagem.anterior
        self.assertEqual(esperado, resultado1)
        self.assertEqual(esperado, resultado2)
    
    # ---------// tem_próximo //---------

    def test_tem_próximo_retornando_true_caso_repetir_true(self):
        self.contagem.número_atual = float('inf')
        self.assertTrue(self.contagem.tem_próximo)

    def test_tem_próximo_retornando_true_caso_repetir_ao_passar_página_true(
        self
    ):
        self.contagem.número_atual = float('inf')
        self.contagem.repetir = False
        self.contagem.repetir_ao_passar_página = True
        self.assertTrue(self.contagem.tem_próximo)
    
    def test_tem_próximo_retornando_true_caso_número_atual_menor_número_final(
        self
    ):
        self.contagem.repetir = False
        self.assertTrue(self.contagem.tem_próximo)
    
    def test_tem_próximo_retornando_false_caso_tudo_seja_false(self):
        self.contagem.repetir = False
        self.contagem.número_atual = float('inf')
        self.assertFalse(self.contagem.tem_próximo)
    
    # ---------// tem_anterior //---------

    def test_tem_anterior_retornando_true_caso_repetir_true(self):
        self.contagem.número_atual = -float('inf')
        self.assertTrue(self.contagem.tem_anterior)
    
    def test_tem_anterior_retornando_true_caso_repetir_ao_passar_página_true(
        self
    ):
        self.contagem.número_atual = -float('inf')
        self.contagem.repetir = False
        self.contagem.repetir_ao_passar_página = True
        self.assertTrue(self.contagem.tem_anterior)

    def test_tem_anterior_retornando_true_caso_número_atual_maior_que_número_inicial(
        self
    ):
        self.contagem.número_atual = float('inf')
        self.contagem.repetir = False
        self.assertTrue(self.contagem.tem_anterior)
    
    def test_tem_anterior_retornando_false_caso_tudo_seja_false(self):
        self.contagem.número_atual = -float('inf')
        self.contagem.repetir = False
        self.assertFalse(self.contagem.tem_anterior)
    
    # ---------// tem_próximo_sem_restrição //---------

    def test_tem_próximo_sem_restrição_retornando_true_caso_repetir_true(self):
        self.contagem.número_atual = float('inf')
        self.assertTrue(self.contagem.tem_próximo_sem_restrição)
    
    def test_tem_próximo_sem_restrição_retornando_true_caso_número_atual_menor_número_final(
        self
    ):
        self.contagem.número_atual = -float('inf')
        self.contagem.repetir = False
        self.assertTrue(self.contagem.tem_próximo_sem_restrição)
    
    def test_tem_próximo_sem_restrição_retornando_false_caso_tudo_seja_false(
        self
    ):
        self.contagem.número_atual = float('inf')
        self.contagem.repetir = False
        self.assertFalse(self.contagem.tem_próximo_sem_restrição)
    
    # ---------// tem_anterior_sem_restrição //---------

    def test_tem_anterior_sem_restrição_retornando_true_caso_repetir_true(self):
        self.contagem.número_atual = -float('inf')
        self.assertTrue(self.contagem.tem_anterior_sem_restrição)
    
    def test_tem_anterior_sem_restrição_retornando_true_caso_número_atual_maior_número_inicial(
        self
    ):
        self.contagem.repetir = False
        self.contagem.número_atual = float('inf')
        self.assertTrue(self.contagem.tem_anterior_sem_restrição)
    
    def test_tem_anterior_retornando_false_caso_tudo_seja_false(self):
        self.contagem.repetir = False
        self.contagem.número_atual = -float('inf')
        self.assertFalse(self.contagem.tem_anterior_sem_restrição)
    
    # ---------// atualizar_limites //---------

    def test_atualizar_limites_definindo_número_inicial_caso_entrada_seja_1_none(
        self
    ):
        self.contagem.atualizar_limites(1, None)
        esperado = [1, 4]
        resultado = [self.contagem._número_inicial, self.contagem._número_final]
        self.assertEqual(esperado, resultado)
    
    def test_atualizar_limites_definindo_número_final_caso_entrada_seja_none_3(
        self
    ):
        self.contagem.atualizar_limites(None, 3)
        esperado = [0, 3]
        resultado = [self.contagem._número_inicial, self.contagem._número_final]
        self.assertEqual(esperado, resultado)
    
    def test_atualizar_limites_definindo_limites_para_2_5(self):
        self.contagem.atualizar_limites(2, 5)
        esperado = [2, 5]
        resultado = [self.contagem._número_inicial, self.contagem._número_final]
        self.assertEqual(esperado, resultado)
    
    def test_atualizar_limites_nao_definindo_limites_caso_entrada_seja_none_none(
        self
    ):
        self.contagem.atualizar_limites(None, None)
        esperado = [0, 4]
        resultado = [self.contagem._número_inicial, self.contagem._número_final]
        self.assertEqual(esperado, resultado)
    
    def test_atualizar_limites_corrigindo_limite_caso_número_atual_seja_menor_que_número_inicial(
        self
    ):
        self.contagem.atualizar_limites(1, 5)
        esperado = 1
        resultado = self.contagem.número_atual
        self.assertEqual(esperado, resultado)
    
    def test_atualizar_limites_corrigindo_limite_caso_número_atual_seja_maior_que_número_final(
        self
    ):
        self.contagem.número_atual = 8
        self.contagem.atualizar_limites(1, 5)
        esperado = 5
        resultado = self.contagem.número_atual
        self.assertEqual(esperado, resultado)
    
    # ---------// ir_para_o_inicio //---------

    def test_ir_para_o_início_definindo_o_número_atual_para_o_início(self):
        self.contagem.número_atual = 4
        self.contagem.ir_para_o_inicio()
        esperado = 0
        resultado = self.contagem.número_atual
        self.assertEqual(esperado, resultado)
    
    # ---------// ir_para_o_final //---------

    def test_ir_para_o_final_definindo_o_número_atual_para_o_final(self):
        self.contagem.ir_para_o_final()
        esperado = 4
        resultado = self.contagem.número_atual
        self.assertEqual(esperado, resultado)
    
    def test_ir_para_o_final_definindo_repetir_true(self):
        self.contagem.repetir = False
        self.contagem.ir_para_o_final()
        self.assertTrue(self.contagem.repetir)
    
    # ---------// retornar_número_final //---------

    def test_retornando_número_final_fazendo_o_óbvio(self):
        esperado = 4
        resultado = self.contagem.retornar_número_final
        self.assertEqual(esperado, resultado)
    


class TestPorcento(TestCase):
    def setUp(self):
        self.porcentagem = Porcento(200, 0)
    
    # ---------// calcular //---------

    def test_calcular_retornando_15_caso_o_número_antigo_seja_0(self):
        esperado = 15
        resultado = self.porcentagem.calcular(30)
        self.assertEqual(esperado, resultado)

    def test_calcular_retornando_1_caso_o_número_antigo_seja_30_e_porcento_ja_calculou(
        self
    ):
        esperado = 1
        resultado = self.porcentagem.calcular(30)
        self.assertEqual(15, resultado)
        resultado = self.porcentagem.calcular(32)
        self.assertEqual(esperado, resultado)
    
    def test_calcular_retornando_menos_1_caso_o_número_antigo_seja_30_e_porcento_ja_calculou(
        self
    ):
        esperado = -1
        resultado = self.porcentagem.calcular(30)
        self.assertEqual(15, resultado)
        resultado = self.porcentagem.calcular(28)
        self.assertEqual(esperado, resultado)
    
    def test_calcular_retornando_porcentagem_atual_0(self):
        esperado = 0
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
    
    def test_calcular_retornando_porcentagem_atual_15(self):
        esperado = 15
        self.porcentagem.calcular(30)
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
    
    def test_calcular_retornando_99_caso_o_número_antigo_seja_0(self):
        esperado = 99.95
        self.porcentagem.calcular(199.9)
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
    
    # ---------// finalizou //---------

    def test_finalizou_retornando_true_caso_porcentagem_chegue_ao_fim(self):
        self.porcentagem.calcular(200)
        self.assertTrue(self.porcentagem.finalizou)
    
    def test_finalizou_retornando_falso_caso_porcentagem_não_chegue_ao_fim(
        self
    ):
        self.porcentagem.calcular(1)
        self.assertFalse(self.porcentagem.finalizou)
    
    # ---------// porcentagem_atual //---------

    def test_porcentagem_atual_retornando_0_caso_calcular_não_for_chamado(self):
        esperado = 0
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
    
    def test_porcentagem_atual_retornando_1_caso_calcular_seja_chamado_com_2(
        self
    ):
        self.porcentagem.calcular(2)
        esperado = 1
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)
    
    def test_porcentagem_retornando_100_caso_calcular_seja_chamado_com_200(
        self
    ):
        self.porcentagem.calcular(200)
        esperado = 100
        resultado = self.porcentagem.porcentagem_atual
        self.assertEqual(esperado, resultado)


class TestColorir(TestCase):
    def test_colorir_retornando_uma_string_no_padrão_do_rich(self):
        esperado = '[bold red on black]texto[/bold red on black]'
        resultado = colorir('texto', 'bold red on black')
        self.assertEqual(esperado, resultado)


class TestTemporizador(TestCase):
    def setUp(self):
        self.temporizador = Temporizador()
    
    def test_ativar_gerando_erro_caso_valor_seja_menor_que_zero(self):
        with self.assertRaises(ValueError):
            self.temporizador.ativar(-1)
    
    def test_ativar_definindo_os_segundos(self):
        self.temporizador.ativar(3)
        esperado = 3
        resultado = self.temporizador._segundos
        self.assertEqual(esperado, resultado)
    
    @patch('src.utils.sleep')
    def test_esperar_esperando_3_segundos(self, sleep):
        self.temporizador.ativar(3)
        self.temporizador.esperar()
        for chamada in sleep.call_args_list:
            self.assertEqual(chamada.args[0], 1)
        self.assertEqual(sleep.call_count, 3)


class TestPáginasInválidas(TestCase):
    # ---------// não passando //---------

    def test_não_passando_caso_tenha_um_caracter_inválido_no_início(self):
        self.assertTrue(páginas_invalidas('-1, 2-3'))

    def test_não_passando_caso_tenha_um_caracter_inválido_em_um_número_sozinho(
        self
    ):
        self.assertTrue(páginas_invalidas('1-, 2-3'))
    
    def test_não_passando_caso_tenha_um_caracter_inválido_no_meio_de_dois_números(
        self
    ):
        self.assertTrue(páginas_invalidas('1, 2--3'))
    
    def test_não_passando_caso_tenha_dois_números_iguais_junto_com_hífen(self):
        self.assertTrue(páginas_invalidas('1, 2-2'))
    
    def test_não_passando_caso_inicie_com_dois_números_iguais_separados_por_hífen(
        self
    ):
        self.assertTrue(páginas_invalidas('2-2, 1'))
    
    def test_não_passando_caso_não_tenha_virgula_separando_os_números(self):
        self.assertTrue(páginas_invalidas('1 2-3'))
    
    def test_não_passando_caso_tenha_números_isolados_repetidos(self):
        self.assertTrue(páginas_invalidas('1, 1'))
    
    def test_não_passando_caso_tenha_número_isolado_repetido_com_números_em_hífen(
        self
    ):
        self.assertTrue(páginas_invalidas('2, 1-3'))
    
    def test_não_passando_caso_tenha_números_com_hífen_repetidos(self):
        self.assertTrue(páginas_invalidas('1-2, 1-2'))
    
    def test_não_passando_caso_tenha_números_com_dois_hífens(self):
        self.assertTrue(páginas_invalidas('1-2-3'))
    
    def test_não_passando_caso_primeiro_número_hífen_seja_maior_que_o_segundo(
        self
    ):
        self.assertTrue(páginas_invalidas('3-2'))
    
    # ---------// passando //---------

    def test_passando_caso_inicie_com_um_número_sozinho(self):
        self.assertFalse(páginas_invalidas('1, 2-3'))
    
    def test_passando_caso_inicie_com_dois_números_separados_por_hífen(self):
        self.assertFalse(páginas_invalidas('2-3, 1'))
    

class TestTratarPáginasUsuário(TestCase):
    def test_retornando_páginas_ordenadas(self):
        esperado = [1, 2, 3, 4]
        resultado = tratar_páginas_usuario('4, 2-3, 1')
        self.assertEqual(esperado, resultado)


class TestEstáInstalado(TestCase):
    @patch('src.utils.os.listdir')
    def test_programa_na_path(self, listdir):
        listdir().__contains__.return_value = True
        self.assertTrue(está_instalado('pão'))
        # pão está instalado 😃

    @patch('src.utils.os.listdir')
    def test_programa_não_está_na_path(self, listdir):
        listdir().__contains__.return_value = False
        self.assertFalse(está_instalado('pão'))
        # pão não está instalado 😠