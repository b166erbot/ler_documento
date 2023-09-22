from unittest import TestCase
from unittest.mock import patch

from src.falar import falar, parar_fala


class TestsFalar(TestCase):
    @patch('src.falar.subprocess')
    def test_chamando_run_com_um_comando_específico(self, subprocess):
        falar('', '', '')
        esperado = "espeak -v  -s ''".split()
        resultado = subprocess.run.call_args[0][0]
        self.assertEqual(esperado, resultado)
    

class TestPararFalar(TestCase):
    @patch('src.falar.subprocess')
    def test_chamando_run_com_um_comando_específico(self, subprocess):
        comando = 'pkill espeak'.split()
        parar_fala()
        subprocess.run.assert_called_with(comando)
