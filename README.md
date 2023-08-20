# ler_documento
Ler um documento para você enquanto você faz alguma outra coisa.

## Para que serve:
- Extrair o texto de um arquivo e ler ele para você.

## Dependências:
- Instalar o programa espeak
- Instalar o mbrola junto com a voz que deseja. Ex: mbrola-br1 (recomendado para português brasileiro.)

## Como instalar as dependências:
- Linux: sudo apt install espeak mbrola \[mbrola-br1\]
> Por enquanto só funciona em distribuições derivadas de debian, como debian, ubuntu, linux-mint, kali-linux, etc.
- Windows: Por enquanto não tem suporte.

## Como instalar:
- poetry install

## Como rodar:
- primeiro ative o ambiente virtual: poetry shell
- depois: python3 main.py --arquivo arquivo(.pdf, .txt, sem_extensão)
> pretendo adicionar mais extensões futuramente.

## Argumentos:
- -a ou --arquivo: Arquivo a ser passado para o programa ler.
- -f ou --forcar-salvamento: Força o programa a extrair o texto e salvar novamente.
- -le ou --lingua-espeak: Língua pela qual o espeak irá falar. default = mb-br1.
- -ls ou --lingua-spacy: Língua pela qual o spacy irá tratar o arquivo. default = pt_core_news_sm.
- -v ou --velocidade: Velocidade pela qual o programa irá ler o conteúdo. default = 130.
- -p ou --paginas: Páginas pelas quais o programa irá ler.
- -z ou --zerar-progresso: Força o programa a reiniciar o progresso da leitura.

## Recursos:
- avançar sentenças.
- retroceder sentenças.
- avançar páginas.
- retroceder páginas.
- ir para a página e sentença diretamente.
- "pausar" uma fala. (ele não pausa, ele interrompe a fala.)
- "continuar" uma fala. (ele não continua, ele começa a fala da sentença do início.)
- salvar o progresso automaticamente quando o usuário sair do programa com o **ctrl+c**. Nada de sair fechando a janela pois o progresso é perdido.
- extrai o texto uma vez, salva ele em um arquivo *.pkl* com o nome do hash do arquivo do texto obtido, e na próxima vez que o programa abre, só carrega o arquivo.
- indentifica se o arquivo é repetido caso você tenha arquivos com o nome diferente mas com o mesmo conteúdo.
- exibe parte da sentença na tela.
- exibe a página e sentença atual na tela.
- exibe o número máximo de páginas e sentenças da página escolhida na tela.

Algum bug? reporte na aba issues para mim.
