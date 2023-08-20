import subprocess


def parar_fala() -> None:
    """Para um processo do espeak e interrompe a fala."""
    comando = 'pkill espeak'.split()
    subprocess.run(comando)


def falar(linha: str, lingua: str, velocidade: int) -> None:
    """Fala texto em português com o programa espeak."""
    comando = f"espeak -v {lingua} -s {velocidade}".split() + [f"'{linha}'"]
    subprocess.run(comando, stderr=subprocess.DEVNULL)