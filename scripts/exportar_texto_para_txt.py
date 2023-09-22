import sys
from argparse import ArgumentParser
from pathlib import Path
from time import sleep

aqui = Path(__file__).parent
sys.path.append(str(aqui.parent))


from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.extrair_texto import extrair
from src.salvar import obter_texto

console = Console()


def tela_erro(mensagem: str) -> None:
    with console.screen(style = 'bold white on red') as tela:
        texto = Align.center(
            Text.from_markup(f'{mensagem}', justify = 'center'),
            vertical = 'middle'
        )
        tela.update(Panel(texto))
        sleep(5)
        exit(1)


def verificar_arquivo(arquivo: Path) -> bool:
    mensagem = ''
    if not arquivo.exists():
        mensagem = 'Arquivo não existe.'
    elif not arquivo.is_file():
        mensagem = 'O caminho passado não é um arquivo.'
    if bool(mensagem):
        tela_erro(mensagem)


def main() -> None:
    """Função principal."""
    uso = '[poetry run] python3 exportar_texto.py'
    descrição = 'Extrai o texto do banco de dados ou de um arquivo.'
    parser = ArgumentParser(usage = uso, description = descrição)
    parser.add_argument(
        '-a', '--arquivo', required = True,
        help = 'Nome do arquivo pelo qual terá o texto extraído.'
    )
    parser.add_argument(
        '-ls', '--lingua-spacy', default = 'pt_core_news_sm',
        help = (
            'Língua pela qual o programa deve tratar o texto com '
            'spacy. Padrão: pt_core_news_sm.'
        )
    )
    parser.add_argument(
        '-s', '--sobrescrever', action = 'store',
        help = 'Sobrescreve o arquivo se ele já existe.'
    )
    argumentos = parser.parse_args()
    arquivo_usuario = Path(argumentos.arquivo.strip())
    verificar_arquivo(arquivo_usuario)
    texto = obter_texto(arquivo_usuario)
    if not bool(texto):
        texto = extrair(arquivo_usuario, argumentos.lingua_spacy)
    if not bool(texto):
        mensagem = 'arquivo vazio.'
        tela_erro(mensagem)
    texto = '\n'.join(map(
        lambda lista: ' '.join(lista[1]),
        texto
    ))
    local_textos = aqui.parent / 'textos_exportados'
    if not local_textos.exists():
        local_textos.mkdir()
    local_arquivo_texto = local_textos / f"{arquivo_usuario.stem}.txt"
    condições = [
        not local_arquivo_texto.exists(), argumentos.sobrescrever
    ]
    if any(condições):
        with local_arquivo_texto.open('w') as arquivo:
            arquivo.write(texto)
    else:
        mensagem = f'arquivo já existe. Abra o arquivo: {local_arquivo_texto}'
        tela_erro(mensagem)


main()



# TODO: arrumar a descrição e uso acima.