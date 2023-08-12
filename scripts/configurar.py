import sys
from configparser import ConfigParser
from json import dump, load
from pathlib import Path

from pynput.keyboard import Key


def main():
    """Função principal."""
    local_projeto = Path(__file__).parent.parent
    local_arquivo = local_projeto / 'config.json'
    print(
        'Esse programa tem o intúito de criar/editar um arquivo'
        f" de configuração.\n O local desse arquivo é {local_arquivo}\n"
    )
    resposta = input(
        'Gostaria de imprimir todas as teclas de atalhos? [sim/não]: '
    )
    if resposta.strip().lower() in ['sim', 's', 'yes', 'y']:
        print(', '.join(map(lambda chave: chave.name, Key)) + '\n')
        print(
            'As teclas de a-z, números e pontuações também podem'
            ' ser usadas como atalho.\n'
        )
    print(
        'Todas as questões abaixo são opcionais, e se não respondidas, '
        'não irá alterar o arquivo de configuração.\n'
    )
    print('Digite as respostas dessa forma: ctrl shift ,')
    voltar = input(
        'Suas teclas de atalho para voltar: '
    ).strip().lower().split(' ')
    avançar = input(
        'Suas teclas de atalho para avançar: '
    ).strip().lower().split(' ')
    voltar_pagina = input(
        'Suas teclas de atalho para voltar página: '
    ).strip().lower().split(' ')
    avançar_pagina = input(
        'Suas teclas de atalho para avançar página: '
    ).strip().lower().split(' ')
    sair = input('Suas teclas de atalho para sair: ').strip().lower().split(' ')
    config = dict()
    if all([local_arquivo.exists(), local_arquivo.is_file()]):
        with open(local_arquivo) as arquivo:
            config_antiga = load(arquivo)
        valores = list(zip(
            [voltar, avançar, voltar_pagina, avançar_pagina, sair],
            config_antiga['teclas_atalho'].values()
        ))
        chaves_valores = list(zip(
            ['voltar', 'avancar', 'voltar_pagina', 'avancar_pagina', 'sair'],
            valores
        ))
    else:
        valores = list(zip(
            [voltar, avançar, voltar_pagina, avançar_pagina, sair],
            [
                ['ctrl', ','],
                ['ctrl', '.'],
                ['alt', ','],
                ['alt', '.'],
                ['ctrl', ';'],
            ]
        ))
        chaves_valores = list(zip(
            ['voltar', 'avancar', 'voltar_pagina', 'avancar_pagina', 'sair'],
            valores
        ))
    config['teclas_atalho'] = {
        chave: (
            valor_usuario
            if any(valor_usuario)
            else valor_padrao
        )
        for chave, (valor_usuario, valor_padrao)
        in chaves_valores
    }
    with open(local_arquivo, 'w') as arquivo:
        dump(config, arquivo, indent = 4)
    print('Finalizado!')


try:
    main()
except (EOFError, KeyboardInterrupt):
    print('\nConfiguração abortada.')