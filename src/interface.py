from pathlib import Path

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import (
    Container, Horizontal, Vertical, ScrollableContainer
)
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button, ProgressBar, Label

from src.threads import contagens
from src.utils import Porcento


# isso serve quando eu quero rodar só esse módulo isolado.
local_programa = Path(__file__).parent.parent

class LeitorApp(App):
    """Classe da interface por linha de comando."""
    CSS_PATH = str(local_programa / 'css/interface.css')

    def __init__(self, *args, **kwargs) -> None:
        super(*args, **kwargs)
        self.porcentagem = Porcento(
            contagens.numero_maximo, contagens.numero_atual_
        )

    def compose(self) -> ComposeResult:
        """Compoẽ os widgets na tela."""
        texto = (
            'Aqui aparecerá todo o texto do programa, como a sentença sendo '
            'lida, número da página com o número da linha, mostrar avançando'
            ' e voltando, mensagens de aviso, etc. digite ctrl+c para sair.'
        )
        with Vertical(id = 'leitor'):
            with Horizontal():
                yield Label(texto, id = 'label_principal')
            with Horizontal():
                yield ProgressBar(id = 'barra_de_progresso', total = 100)
            with Horizontal(id = 'container2'):
                yield Button('rodar', id = 'rodar')
                yield Button('pausar', id = 'pausar')
                yield Button('avançar', id = 'avancar')
                yield Button('voltar', id = 'voltar')

    @on(Button.Pressed, '#voltar')
    def voltar_pressionado(self, botao: Button.Pressed) -> None:
        barra_progresso = self.query_one('#barra_de_progresso', ProgressBar)
        barra_progresso.advance(
            - self.porcentagem.calcular(contagens.numero_atual_)
        )
        # self.query_one('#label_principal', Label).update()

    @on(Button.Pressed, '#avancar')
    def avançar_pressionado(self, botao: Button.Pressed) -> None:
        barra_progresso = self.query_one('#barra_de_progresso', ProgressBar)
        barra_progresso.advance(
            self.porcentagem.calcular(contagens.numero_atual_)
        )

    @on(Button.Pressed, '#pausar')
    def pausar_pressionado(self, botao: Button.Pressed) -> None:
        ...
        # self.query_one('#barra_de_progresso', ProgressBar).advance(5)

    @on(Button.Pressed, '#rodar')
    def rodar_pressionado(self, botao: Button.Pressed) -> None:
        ...
        # self.query_one('#barra_de_progresso', ProgressBar).advance(5)


if __name__ == '__main__':
    LeitorApp().run()