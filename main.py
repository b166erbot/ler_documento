from argparse import ArgumentParser
from pathlib import Path

from src.interface import LeitorApp


def main() -> None:
    """Função principal."""
    descricao = 'Programa que lê um texto de um arquivo sem usar a internet.'
    usagem = (
        '[poetry run] python3 main.py -a arquivo -f -l língua -v velocidade '
        '-p paginas -z'
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
    # from src.carregar_texto import injetar_argumentos, retornar_contagens_porcento
    # injetar_argumentos(argumentos)
    # contagens, _ = retornar_contagens_porcento()
    # import pdb; pdb.set_trace()
    app = LeitorApp(argumentos)
    app.run()


main()


# TODO: colocar mais tipos de arquivos.
# TODO: armazenar folha por folha no shelve para não lotar a memória.
# TODO: salvar o arquivo inteiro, porém, carregar somente partes dele
# na memória.
# TODO: fazer com que ele armazene a folha/"numero da linha" para
# eu ler com cautela depois.
# TODO: colocar um lábel para mostrar a sentença atual? não vai ocupar muito
# espaço?
# TODO: colocar input para o usuário percorer as folhas de maneira mais fácil.
# TODO: colocar um botão só para o play e pause.