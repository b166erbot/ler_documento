from argparse import ArgumentParser
from pathlib import Path

from src.interface import LeitorApp


def main() -> None:
    """Função principal."""
    descricao = 'Programa que lê um texto de um arquivo sem usar a internet.'
    usagem = (
        '[poetry run] python3 main.py -a arquivo -f -l língua -v velocidade '
        '-p paginas'
    )
    parser = ArgumentParser(
        usage = usagem, description = descricao
    )
    # o tipo precisa ser str pois preciso tratar antes de transformar em path.
    parser.add_argument(
        '-a', '--arquivo', required = True,
        help = 'Nome do arquivo pelo qual terá o texto lido.'
    )
    parser.add_argument(
        '-f', '--forcar-salvamento',
        action = 'store_true',
        help = 'Salvar a força.'
    )
    parser.add_argument(
        '-le', '--lingua-espeak', required = False, default = 'mb-br1',
        help = 'Língua pela qual o programa deve falar com espeak e mbrola.'
    )
    parser.add_argument(
        '-ls', '--lingua-spacy', required = False, default = 'pt_core_news_sm',
        help = 'Língua pela qual o programa deve tratar o texto com spacy.'
    )
    parser.add_argument(
        '-v', '--velocidade', type = int, default = 130,
        help = 'Velocidade em que a voz deve falar.'
    )
    parser.add_argument(
        '-p', '--paginas',
        help = 'Paginas a serem recortadas. Ex: "0, 2-5, 7, 8-9, 1".'
    )
    parser.add_argument(
        '-z', '--zerar-progresso', action = 'store_true',
        help = 'Reinicia o progresso do arquivo para o início.'
    )
    argumentos = parser.parse_args()
    app = LeitorApp(argumentos)
    app.run()


main()


# TODO: colocar mais tipos de arquivos.
# TODO: armazenar folha por folha no shelve para não lotar a memória.
# TODO: salvar o arquivo inteiro, porém, carregar somente partes dele
# na memória.
# TODO: fazer com que ele armazene a folha/"numero da linha" para
# eu ler com cautela depois.
# TODO: documentar as funções e métodos.
# TODO: loading widget textual. DESISTI KKKKKKKKKK
# TODO: desativar botões de avançar e retroceder página caso o arquivo seja do
# tipo texto puro.
# TODO: VerticalScroll.
# TODO: remover bibliotecas/códigos/módulos desnecessários.