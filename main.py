from argparse import ArgumentParser, Namespace
from pathlib import Path
from threading import Thread
from time import sleep

from src.extrair_texto import extrair
from src.salvar import (criar_config, existe_arquivo, obter_texto, salvar,
                        verificar_arquivo_shelve)
from src.threads import (bloquear_entradas_usuario, gerenciar_falas,
                         gerenciar_teclado)
from src.utils import esta_instalado, validar_paginas
from src.interface import LeitorApp


def pre_main() -> list[list[list[str]], Namespace]:
    """Função pré principal."""
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

    print('Aviso: não use o espeak enquanto estiver usando esse programa.')

    # verificar se o programa espeak está instalado
    if not esta_instalado('espeak'):
        print('O programa espeak não está instalado.')
        print(
            'Para instalar ele com as dependências, digite: sudo apt install '
            'espeak mbrola mbrola-br1'
        )
        exit()

    if bool(argumentos.paginas):
        if not validar_paginas(argumentos.paginas):
            print(
                'O padrão de números de páginas não correspode ao padrão'
                ' adequado.'
            )
            print("padrão: '1, 3, 5-7, 9, 18-60'")
            exit()
    
    if not existe_arquivo(Path('config.json')):
        criar_config()

    arquivo = argumentos.arquivo.strip()
    arquivo = Path(arquivo).expanduser()
    if not arquivo.exists():
        print('Arquivo não existe.')
        exit()
    elif not arquivo.is_file():
        print('O caminho passado não é um arquivo.')
        exit()

    arquivo_processado = verificar_arquivo_shelve(arquivo)

    # marcar para salvar e definir a mensagem para o usuário.
    if all([arquivo_processado, argumentos.forcar_salvamento]):
        marcar_salvar, mensagem = (True, 'Arquivo salvo!')
    elif all([arquivo_processado, not argumentos.forcar_salvamento]):
        marcar_salvar, mensagem = (
            False,
            (
                'Arquivo.pkl não alterado/salvo pois opção --forcar-salvamento '
                'foi omitida.'
            )
        )
    elif not arquivo_processado:
        marcar_salvar, mensagem = (True, 'Arquivo salvo!')
    
    # decicir entre extrair e salvar no banco de dados.
    if marcar_salvar:
        textos = extrair(arquivo, argumentos.lingua_spacy, argumentos.paginas)
        salvar(textos, arquivo)
        print(mensagem)
    else:
        textos = obter_texto(arquivo)
        print(mensagem)
    # esperar um tempo após exibir mensagens na tela.
    sleep(2)
    return [textos, argumentos]


def main(textos: list[list[str]], argumentos) -> None:
    """Função principal."""
    # todas as treads com daemon serão interrompidas caso só existam threads
    # que tem o daemon ativo. As que tem '.join()' só finalizam quando terminam
    args = (textos, argumentos)
    thread_falas = Thread(
        target = gerenciar_falas, args = args, daemon = True
    )
    thread_bloquear_entradas = Thread(
        target = bloquear_entradas_usuario, daemon = True
    )
    thread_interface = Thread(target = lambda: app.run())
    # bloquear entradas é temporário até eu achar um substituto.
    # thread_bloquear_entradas.start()
    
    # esperar um pouco para rodar a thread acima primeiro.
    pausar_ate_carregar_interface.ativar(0.5)
    thread_falas.start()
    app = LeitorApp()
    # o pynput já usa o threading e já tem o join nessa função abaixo.
    gerenciar_teclado().start()
    thread_interface.join()


main(*pre_main())


# TODO: colocar mais tipos de arquivos.
# TODO: armazenar folha por folha no shelve para não lotar a memória.
# TODO: salvar o arquivo inteiro, porém, carregar somente partes dele
# na memória.
# TODO: fazer com que ele armazene a folha/"numero da linha" para
# eu ler com cautela depois.
# TODO: concertar o bug de exibir texto na tela quando o usuário digita.
# TODO: criar pausa.
# TODO: documentar as funções e métodos.
# TODO: corrigir o race condition no threads.
# TODO: colocar para segurar uma tecla e ele avançar/retroceder conforme segura.
# TODO: usar textual para bloquear entradas do usuário?