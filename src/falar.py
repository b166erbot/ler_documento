import subprocess

# Não use o parar_fala pois há um bug onde, depois de executado, ele inicia
# a próxima fala logo em seguida, impedindo que o usuário avance ou retroceda
# corretamente.


def parar_fala() -> None:
    """Para um processo do espeak e interrompe a fala."""
    comando = 'pkill espeak'.split()
    subprocess.run(comando)


def falar(linha: str, lingua: str, velocidade: int) -> None:
    """Fala texto em português com o programa espeak."""
    comando = f"espeak -v {lingua} -s {velocidade}".split() + [f"'{linha}'"]
    subprocess.run(comando, stderr=subprocess.DEVNULL)