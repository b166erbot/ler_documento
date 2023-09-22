from argparse import ArgumentParser

from src.interface import LeitorApp


def main() -> None:
    """Função principal."""
    descricao = 'Programa que lê um texto de um arquivo sem usar a internet.'
    usagem = (
        '[poetry run] python3 main.py -a arquivo -f -l língua -v velocidade '
        '-p páginas -z'
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
        help = (
            'Língua pela qual o programa deve falar com espeak e mbrola. '
            'Padrão: mb-br1'
        )
    )
    parser.add_argument(
        '-ls', '--lingua-spacy', required = False, default = 'pt_core_news_sm',
        help = (
            'Língua pela qual o programa deve tratar o texto com '
            'spacy. Padrão: pt_core_news_sm.'
        )
    )
    parser.add_argument(
        '-v', '--velocidade', type = int, default = 130,
        help = 'Velocidade em que a voz deve falar. Padrão: 130.'
    )
    parser.add_argument(
        '-p', '--páginas',
        help = (
            'páginas a serem recortadas. Ex: "0, 2-5, 7, 8-9, 1". '
            'Caso use essa opção, o usuário precisa saber as páginas'
            'que irá avançar pois o programa não irá informar.'
        )
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
# TODO: fazer com que ele armazene a folha/"número da linha" para
# eu ler com cautela depois.
# TODO: colocar um botão só para o play e pause. por causa de bugs, eu resolvi
# não colocar.