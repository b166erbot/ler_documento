from unittest import TestCase, skip
from unittest.mock import MagicMock, patch

patch('spacy.load').start()
patch('spacy.cli.download').start()
patch('PyPDF4.PdfFileReader').start()


from src.carregar_texto import (
    injetar_argumentos, retornar_contagens_porcento, retornar_textos_argumentos)
from src.utils import ContagensFinitas


class TestInjetarArgumentos(TestCase):
    def setUp(self):
        self.argumentos = MagicMock(
            forcar_salvamento = False, páginas = None
        )

    # ---------// extraindo texto //---------

    @patch('src.carregar_texto.tratar_páginas_usuario')
    @patch('src.carregar_texto.salvar')
    @patch('src.carregar_texto.extrair', return_value = ['oi', 'ola'])
    @patch('src.carregar_texto.ContagensFinitas')
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi']), (1, ['ola'])]
    )
    def test_não_extraindo_texto_caso_forçar_salvamento_false_e_textos_lista(
        self, obter_texto, ContagensFinitas, extrair, salvar,
        tratar_páginas_usuario
    ):
        injetar_argumentos(self.argumentos)
        extrair.assert_not_called()
        salvar.assert_not_called()
    
    @patch('src.carregar_texto.tratar_páginas_usuario')
    @patch('src.carregar_texto.salvar')
    @patch('src.carregar_texto.extrair', return_value = ['oi', 'ola'])
    @patch('src.carregar_texto.ContagensFinitas')
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi']), (1, ['ola'])]
    )
    def test_extraindo_texto_caso_forçar_salvamento_true_e_textos_lista(
        self, obter_texto, ContagensFinitas, extrair, salvar,
        tratar_páginas_usuario
    ):
        self.argumentos.forcar_salvamento = True
        injetar_argumentos(self.argumentos)
        extrair.assert_called_once()
        salvar.assert_called_once()
    
    @patch('src.carregar_texto.tratar_páginas_usuario')
    @patch('src.carregar_texto.salvar')
    @patch('src.carregar_texto.extrair', return_value = ['oi', 'ola'])
    @patch('src.carregar_texto.ContagensFinitas')
    @patch('src.carregar_texto.obter_texto', return_value = None)
    def test_extraindo_texto_caso_forçar_salvamento_false_e_textos_none(
        self, obter_texto, ContagensFinitas, extrair, salvar,
        tratar_páginas_usuario
    ):
        injetar_argumentos(self.argumentos)
        extrair.assert_called_once()
        salvar.assert_called_once()
    
    # decidi colocar um retorno na função pois os testes estão difíceis

    # ---------// filtrando páginas //---------

    @patch('src.carregar_texto.tratar_páginas_usuario')
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi']), (1, ['ola'])]
    )
    def test_filtrando_páginas_caso_existam_páginas_nos_argumentos(
        self, obter_texto, tratar_páginas_usuario
    ):
        self.argumentos.páginas = '1, 2'
        tratar_páginas_usuario.return_value = [1, 2]
        retorno = injetar_argumentos(self.argumentos)
        número_de_contagens = len(retorno[3]._contagens.values())
        self.assertEqual(número_de_contagens, 2)
    
    @patch('src.carregar_texto.tratar_páginas_usuario')
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi']), (1, ['ola']), (2, ['alo'])]
    )
    def test_não_filtrando_páginas_caso_não_existam_páginas_nos_argumentos(
        self, obter_texto,
        tratar_páginas_usuario
    ):
        retorno = injetar_argumentos(self.argumentos)
        número_de_contagens = len(retorno[3]._contagens.values())
        self.assertEqual(número_de_contagens, 3)
    
    # ---------// reiniciando progresso //---------

    @patch('src.carregar_texto.salvar')
    @patch(
        'src.carregar_texto.extrair',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    @patch('src.carregar_texto.carregar_progresso', return_value = [0, 1])
    @patch('src.carregar_texto.existe_arquivo', return_value = True)
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    def test_não_reiniciando_o_progresso_caso_forcar_salvamento_true(
        self, obter_texto, existe_arquivo, carregar_progresso, extrair, salvar
    ):
        self.argumentos.zerar_progresso = False
        self.argumentos.forcar_salvamento = False
        retorno = injetar_argumentos(self.argumentos)
        esperado = [0, 1]
        resultado = [
            retorno[3].número_atual,
            retorno[3].contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)

    @patch('src.carregar_texto.carregar_progresso', return_value = [0, 1])
    @patch('src.carregar_texto.existe_arquivo', return_value = False)
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    def test_reiniciando_o_progresso_caso_arquivo_não_exista(
        self, obter_texto, existe_arquivo, carregar_progresso
    ):
        self.argumentos.zerar_progresso = False
        retorno = injetar_argumentos(self.argumentos)
        esperado = [0, 0]
        resultado = [
            retorno[3].número_atual,
            retorno[3].contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
    
    @patch('src.carregar_texto.carregar_progresso', return_value = [0, 1])
    @patch('src.carregar_texto.existe_arquivo', return_value = True)
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    def test_reiniciando_o_progresso_caso_zerar_progresso_true(
        self, obter_texto, existe_arquivo, carregar_progresso
    ):
        self.argumentos.zerar_progresso = True
        retorno = injetar_argumentos(self.argumentos)
        esperado = [0, 0]
        resultado = [
            retorno[3].número_atual,
            retorno[3].contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
    
    @patch('src.carregar_texto.carregar_progresso', return_value = [0, 1])
    @patch('src.carregar_texto.existe_arquivo', return_value = True)
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    def test_reiniciando_o_progresso_caso_tenha_páginas_selecionadas_pelo_usuário(
        self, obter_texto, existe_arquivo, carregar_progresso
    ):
        self.argumentos.zerar_progresso = False
        self.argumentos.páginas = '1'
        retorno = injetar_argumentos(self.argumentos)
        esperado = [0, 0]
        resultado = [
            retorno[3].número_atual,
            retorno[3].contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
    
    # ---------// porcentagem.finalizou //---------

    @patch('src.carregar_texto.Porcento.finalizou', True)
    @patch('src.carregar_texto.ContagensFinitas')
    @patch('src.carregar_texto.salvar')
    @patch(
        'src.carregar_texto.extrair',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    @patch('src.carregar_texto.carregar_progresso', return_value = None)
    @patch('src.carregar_texto.existe_arquivo', return_value = True)
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    def test_reiniciando_o_progresso_caso_porcentagem_finalizou_true(
        self, obter_texto, existe_arquivo, carregar_progresso, extrair, salvar,
        Contagens
    ):
        self.argumentos.zerar_progresso = False
        self.argumentos.forcar_salvamento = True
        textos = [(0, ['oi', 'ola']), (1, ['ola', 'oi'])]
        contagens = ContagensFinitas(
            ((número, 0, len(sentenças) - 1) for número, sentenças in textos),
            MagicMock()
        )
        contagens.definir_progresso([0, 1])
        Contagens.return_value = contagens
        retorno = injetar_argumentos(self.argumentos)
        esperado = [0, 0]
        resultado = [
            retorno[3].número_atual,
            retorno[3].contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)
    
    @patch('src.carregar_texto.Porcento.finalizou', False)
    @patch('src.carregar_texto.ContagensFinitas')
    @patch('src.carregar_texto.salvar')
    @patch(
        'src.carregar_texto.extrair',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    @patch('src.carregar_texto.carregar_progresso', return_value = None)
    @patch('src.carregar_texto.existe_arquivo', return_value = True)
    @patch(
        'src.carregar_texto.obter_texto',
        return_value = [(0, ['oi', 'ola', 'alo'])]
    )
    def test_não_reiniciando_o_progresso_caso_porcentagem_finalizou_false(
        self, obter_texto, existe_arquivo, carregar_progresso, extrair, salvar,
        Contagens
    ):
        self.argumentos.zerar_progresso = False
        self.argumentos.forcar_salvamento = True
        textos = [(0, ['oi', 'ola']), (1, ['ola', 'oi'])]
        contagens = ContagensFinitas(
            ((número, 0, len(sentenças) - 1) for número, sentenças in textos),
            MagicMock()
        )
        contagens.definir_progresso([0, 1])
        Contagens.return_value = contagens
        retorno = injetar_argumentos(self.argumentos)
        esperado = [0, 1]
        resultado = [
            retorno[3].número_atual,
            retorno[3].contagem_atual.número_atual
        ]
        self.assertEqual(esperado, resultado)


class TestRetornarContagensPorcento(TestCase):
    def test_retornando_lista_caso_existam_as_variáveis_globais(self):
        lista = retornar_contagens_porcento()
        self.assertIsInstance(lista, list)
    

class TestRetornarTextosArgumentos(TestCase):
    def test_retornando_lista_caso_existam_as_variáveis_globais(self):
        lista = retornar_textos_argumentos()
        self.assertIsInstance(lista, list)