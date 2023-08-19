# Esse módulo precisa ser refatorado pois tem coisas desnecessárias


from argparse import Namespace
from functools import partial
from pathlib import Path
from time import sleep
from typing import Any, Callable

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import (Button, Label, LoadingIndicator, ProgressBar,
                             Static, Input)
from textual.validation import Number

from src.falar import parar_fala
from src.threads import (avancar, avancar_pagina, gerenciar_falas, sair,
                         voltar, voltar_pagina)
from src.utils import (ContagensFinitas, Porcento, colorir, esta_instalado,
                       paginas_invalidas)

local_programa = Path(__file__).parent.parent
contagens: ContagensFinitas
porcentagem: Porcento
injetar_argumentos: Callable
retornar_contagens_porcento: Callable
retornar_textos_argumentos: Callable
# bug no label, se tirar o \n do final, ele não exibe a última linha.
with open(str(local_programa / 'texto_bem_vindo.txt')) as arquivo:
    forma_texto_inicio = arquivo.read()


class TelaPrincipal(Screen):
    CSS_PATH = str(local_programa / 'css/interface.css')

    def __init__(
        self, variaveis_compartilhadas: dict[str: Any], *args, **kwargs
    ) -> None:
        self._variaveis_compartilhadas = variaveis_compartilhadas
        super().__init__(*args, **kwargs)
        self.forma = "Página = {}, sentença = {}"
        self.label_status = Label('', id = 'label_status')
        self.barra_progresso = ProgressBar(
            id = 'barra_de_progresso', total = 100, show_eta = False
        )

    def compose(self) -> ComposeResult:
        """Compoẽ os widgets na tela."""
        with VerticalScroll(id = 'leitor_tela_principal') as container:
            container.border_title = 'Principal'
            # numero_paginas e numero_sentenças corrigidos para o usuário.
            numero_paginas, numero_sentenças = (
                retornar_numero_paginas_sentenças()
            )
            botões_desabilitados = numero_paginas == 1
            with Vertical(id = 'container_progresso'):
                yield self.label_status
                yield self.barra_progresso
                yield Label(id = 'label_sentencas')
            with Vertical():
                with Horizontal(id = 'botoes_tela_principal1'):
                    yield Button(
                        'rodar', id = 'rodar', disabled = True,
                        variant = 'warning'
                    )
                    yield Button(
                        'pausar', id = 'pausar', variant = 'warning'
                    )
                    yield Input(
                        id = 'input_pagina',
                        validators = [Number(1, numero_paginas)],
                        placeholder = 'página'
                    )
                    yield Input(
                        id = 'input_sentenca',
                        validators = [Number(1, numero_sentenças)],
                        placeholder = 'sentença',
                        disabled = True
                    )
                with Horizontal(id = 'botoes_tela_principal2'):
                    yield Button(
                        'avançar', id = 'avancar', variant = 'warning'
                    )
                    yield Button(
                        'voltar', id = 'voltar', variant = 'warning'
                    )
                    yield Button(
                        'avançar página', id = 'avancar_pagina',
                        variant = 'warning', disabled = botões_desabilitados
                    )
                    yield Button(
                        'voltar página', id = 'voltar_pagina',
                        variant = 'warning', disabled = botões_desabilitados
                    )

    def _atualizar_label_status(self) -> None:
        """Atualiza o texto do label principal."""
        pagina = contagens.numero_atual + 1
        sentença = contagens.contagem_atual.numero_atual + 1
        pagina = colorir(pagina, 'dodger_blue2')
        sentença = colorir(sentença, 'dodger_blue2')
        texto = self.forma.format(pagina, sentença)
        texto += '\n' + paginas_sentencas_para_o_usuario()
        self.label_status.update(texto)
    
    def _atualizar_label_sentenças(self, texto) -> None:
        label_sentenças = self.query_one('#label_sentencas', Label)
        if len(texto) > 234:
            texto = f"{texto[:234]}..."
        label_sentenças.update(texto)

    @on(Button.Pressed, '#voltar')
    def voltar_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        voltar(contagens)
        # não precisa colocar número negativo abaixo pois o porcentagem
        # já retorna um número negativo
        self.barra_progresso.advance(
            porcentagem.calcular(contagens.numero_atual_)
        )
        self._atualizar_label_status()

    @on(Button.Pressed, '#avancar')
    def avançar_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        avancar(contagens)
        self.barra_progresso.advance(
            porcentagem.calcular(contagens.numero_atual_)
        )
        self._atualizar_label_status()
    
    @on(Button.Pressed, '#avancar_pagina')
    def avançar_pagina_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        avancar_pagina(contagens)
        self.barra_progresso.advance(
            porcentagem.calcular(contagens.numero_atual_)
        )
        self._atualizar_label_status()
    
    @on(Button.Pressed, '#voltar_pagina')
    def voltar_pagina_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        voltar_pagina(contagens)
        # não precisa colocar número negativo abaixo pois o porcentagem
        # já retorna um número negativo
        self.barra_progresso.advance(
            porcentagem.calcular(contagens.numero_atual_)
        )
        self._atualizar_label_status()

    @on(Button.Pressed, '#pausar')
    def pausar_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        pausar = self.query_one('#pausar', Button)
        rodar = self.query_one('#rodar', Button)
        if not self._variaveis_compartilhadas['pausar']:
            pausar.disabled = True
            rodar.disabled = False
            self._variaveis_compartilhadas['pausar'] = True
            contagens.contagem_atual.repetir_ao_passar_pagina = True
            self._atualizar_label_status()
            parar_fala()

    @on(Button.Pressed, '#rodar')
    def rodar_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        pausar = self.query_one('#pausar', Button)
        rodar = self.query_one('#rodar', Button)
        if self._variaveis_compartilhadas['pausar']:
            rodar.disabled = True
            pausar.disabled = False
            self._variaveis_compartilhadas['pausar'] = False
            self._atualizar_label_status()
            parar_fala()
        
    @on(Input.Changed, '#input_pagina')
    def input_pagina_modificada(self, evento: Input.Changed) -> None:
        """Troca de página conforme o usuário deseja."""
        self.pausar_pressionado(None)
        input_sentença = self.query_one('#input_sentenca', Input)
        if evento.validation_result.is_valid:
            # evento.value corrigido para o programa.
            contagens._definir_progresso_paginas(int(evento.value) - 1)
            # Number corrigido para o usuário.
            input_sentença.validators = [
                Number(1, contagens.contagem_atual._numero_final + 1)
            ]
            self._atualizar_label_status()
            self.barra_progresso.advance(
                porcentagem.calcular(contagens.numero_atual_)
            )
            input_sentença.disabled = False
        else:
            input_sentença.disabled = True

    @on(Input.Changed, '#input_sentenca')
    def input_sentença_modificada(self, evento: Input.Changed) -> None:
        """Troca de sentença conforme o usuário deseja."""
        self.pausar_pressionado(None)
        if evento.validation_result.is_valid:
            contagens._definir_progresso_sentença(int(evento.value) - 1)
            self.barra_progresso.advance(
                porcentagem.calcular(contagens.numero_atual_)
            )
            self._atualizar_label_status()


def retornar_numero_paginas_sentenças() -> list[int]:
    paginas = contagens._numero_final + 1
    sentenças = contagens.contagem_atual.retornar_numero_final + 1
    return [paginas, sentenças]


def paginas_sentencas_para_o_usuario() -> str:
    # paginas e sentenças corrigidas para o usuário.
    paginas, sentenças = retornar_numero_paginas_sentenças()
    paginas = colorir(paginas, 'dodger_blue2')
    sentenças = colorir(sentenças, 'dodger_blue2')
    texto = (
        f"Total: paginas - {paginas}, sentenças da página atual - {sentenças}"
    )
    return texto


class TelaBoasVindas(Screen):
    CSS_PATH = str(local_programa / 'css/interface.css')

    def __init__(
        self, variaveis_compartilhadas: dict[str], *args, **kwargs
    ) -> None:
        self._variaveis_compartilhadas = variaveis_compartilhadas
        self.forma = "Página = {}, sentença = {}"
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """Compoẽ os widgets na tela."""
        self.barra_progresso.advance(
            porcentagem.porcentagem_atual
        )
        # pagina e sentença corrigidos para o usuário.
        pagina = contagens.numero_atual + 1
        sentença = contagens.contagem_atual.numero_atual + 1
        pagina = colorir(pagina, 'dodger_blue2')
        sentença = colorir(sentença, 'dodger_blue2')
        nome_arquivo = contagens.nome_arquivo.stem
        extensão = contagens.nome_arquivo.suffix
        if len(nome_arquivo) > 6:
            nome_arquivo = f"{nome_arquivo[:6]}... {extensão}"
        else:
            nome_arquivo = contagens.nome_arquivo.name
        nome_arquivo = colorir(nome_arquivo, 'dodger_blue2')
        texto_inicio = forma_texto_inicio.format(
            nome_arquivo, pagina, sentença
        )
        with Grid(id = 'grid_comeco') as container:
            container.border_title = 'Inicio'
            yield Label(texto_inicio, id = 'label_inicio')
            yield Button('começar', id = 'botao_comecar', variant = 'success')

    @on(Button.Pressed, '#botao_comecar')
    async def começar_pressionado(self, evento: Button.Pressed) -> None:
        """Executa uma tarefa quando o esse botão for pressionado."""
        self.executar_fala()
    
    @work(exclusive = True, thread = True)
    def executar_fala(self) -> None:
        """Thread separada para executar o gerenciar_falas."""
        gerenciar_falas(
            *retornar_textos_argumentos(), contagens,
            tela_boas_vindas = self
        )
    
    def _atualizar_progresso(self) -> None:
        """Atualiza o progresso da barra de progresso."""
        self.barra_progresso.advance(
            porcentagem.calcular(contagens.numero_atual_)
        )

    def _esperar_retomar(self) -> None:
        """Espera um tempo até que o usuário despause."""
        while self._variaveis_compartilhadas['pausar']:
            sleep(0.1)


class TelaErro(Screen):
    CSS_PATH = str(local_programa / 'css/interface.css')

    def __init__(self, *args, **kwargs) -> None:
        self._label_erro = Label(id = 'label_erro')
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """Compoẽ os widgets na tela."""
        yield self._label_erro


class TelaCarregando(Screen):
    CSS_PATH = str(local_programa / 'css/interface.css')
    
    def compose(self) -> ComposeResult:
        """Compoẽ os widgets na tela."""
        with Vertical(id = 'vertical_carregamento') as container:
            container.border_title = 'Carregando'
            yield Label('Carregando...', id = 'label_carregamento')
            yield LoadingIndicator(id = 'loading_carregamento')


class LeitorApp(App):
    """Classe da interface por linha de comando."""

    CSS_PATH = str(local_programa / 'css/interface.css')
    variaveis_compartilhadas = {'pausar': False}
    tela_principal = TelaPrincipal(variaveis_compartilhadas)
    tela_boas_vindas = TelaBoasVindas(variaveis_compartilhadas)
    SCREENS = {
        'tela boas vindas': tela_boas_vindas,
        'tela principal': tela_principal,
        'tela erro': TelaErro(),
        'tela carregando': TelaCarregando()
    }
    tela_boas_vindas.label_status = tela_principal.label_status
    tela_boas_vindas.barra_progresso = tela_principal.barra_progresso
    tela_boas_vindas._atualizar_label_status = (
        tela_principal._atualizar_label_status
    )
    tela_principal.executar_fala = tela_boas_vindas.executar_fala
    tela_boas_vindas._atualizar_label_sentenças = (
        tela_principal._atualizar_label_sentenças
    )

    def __init__(self, argumentos: Namespace, *args, **kwargs) -> None:
        self._argumentos = argumentos
        self._label_erro = self.SCREENS['tela erro']._label_erro
        super().__init__(*args, **kwargs)
        
    def on_mount(self) -> None:
        """Executa tarefas na montagem das telas."""
        self.push_screen('tela carregando')
        # não use mais de uma tread aqui, pois senão a segunda em diante
        # não irá funcionar.
        self.processamento_tela_loading()
        # colocar o switch_screen aqui fará com que a tela carregamento
        # não carregue

    @on(Button.Pressed, '#botao_comecar')
    def começar_pressionado(self, evento: Button.Pressed) -> None:
        """Troca de telas caso o botão começar for pressionado."""
        self.switch_screen('tela principal')

    @work(exclusive = True, thread = True)
    def processamento_tela_loading(self) -> None:
        """Processar algumas coisas na tela de loading."""
        self.verificando_argumentos()
        self.fazer_importações_e_carregar_texto()
        label_carregamento = self.query_one('#label_carregamento', Label)
        label_carregamento.update(colorir('Fim.', 'green'))
        sleep(0.5)
        # colocar para trocar de tela aqui sem o lambda, gera um erro.
        self.call_later(lambda: self.switch_screen('tela boas vindas'))
    
    def verificando_argumentos(self) -> None:
        """Verifica se o usuário enviou argumentos corretamente."""
        label_carregamento = self.query_one('#label_carregamento', Label)
        label_carregamento.update('Verificando programas instalados')
        # verificar se os programas espeak e mbrola estão instalados
        if not all(map(esta_instalado, ['espeak', 'mbrola'])):
            mensagem = (
                'O programa espeak não está instalado.\n'
                'Para instalar ele com as dependências, digite: sudo apt install '
                'espeak mbrola mbrola-br1\n'
            )
            self._label_erro.update(mensagem)
            self.erro_sair()
            return
        label_carregamento.update(colorir(
            'Verificando programas instalados', 'green'
        ))
        
        sleep(0.3)
        label_carregamento.update('Verificando argumentos')
        if bool(self._argumentos.paginas):
            if paginas_invalidas(self._argumentos.paginas):
                mensagem = (
                    'O padrão de números de páginas não correspode ao padrão'
                    ' adequado.\n'
                    "padrão: '1, 3, 5-7, 9, 18-60'\n"
                )
                self._label_erro.update(mensagem)
                self.erro_sair()
                return
        label_carregamento.update(colorir('Verificando argumentos', 'green'))
        sleep(0.3)

        arquivo = self._argumentos.arquivo.strip()
        arquivo = Path(arquivo).expanduser()
        label_carregamento.update('Verificando arquivo')
        if not arquivo.exists():
            mensagem = 'Arquivo não existe.'
            self._label_erro.update(mensagem)
            self.erro_sair()
            return
        elif not arquivo.is_file():
            mensagem = 'O caminho passado não é um arquivo.'
            self._label_erro.update(mensagem)
            self.erro_sair()
            return
        label_carregamento.update(colorir('Verificando arquivo', 'green'))
        sleep(0.3)
    
    def fazer_importações_e_carregar_texto(self) -> None:
        """Fazer as importações demoradas e extrair/carregar o texto."""
        label_carregamento = self.query_one('#label_carregamento', Label)
        global injetar_argumentos, retornar_contagens_porcento
        global retornar_textos_argumentos
        label_carregamento.update('Importando bibliotecas')
        from src.carregar_texto import (injetar_argumentos,
                                        retornar_contagens_porcento,
                                        retornar_textos_argumentos)
        label_carregamento.update(colorir('Importando bibliotecas', 'green'))
        sleep(0.3)
        global contagens, porcentagem
        label_carregamento.update('Carregando ou extraindo o texto')
        injetar_argumentos(self._argumentos)
        contagens, porcentagem = retornar_contagens_porcento()
        label_carregamento.update(colorir(
            'Carregando ou extraindo o texto', 'green'
        ))
        sleep(0.3)
    
    def erro_sair(self) -> None:
        """Exibe uma mensagem de erro na tela e sai."""
        # colocar para trocar de tela aqui sem o lambda, gera um erro.
        self.call_later(lambda: self.switch_screen('tela erro'))
        sleep(4)
        # coloquei o super aqui pois não quero salvar o progresso.
        super().exit()

    def exit(self) -> None:
        """Função de sair do programa."""
        self.variaveis_compartilhadas['pausar'] = False
        sair(contagens)
        super().exit()