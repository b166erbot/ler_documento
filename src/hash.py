from hashlib import sha256
from pathlib import Path


def hashear_arquivo(local_arquivo: Path) -> str:
    """Retorna o hash de um arquivo."""
    sha = sha256()
    if not all([local_arquivo.exists(), local_arquivo.is_file()]):
        raise FileNotFoundError('Arquivo não encontrado.')
    with open(local_arquivo, 'rb') as arquivo:
        pedaço = arquivo.read(50_000)
        while bool(pedaço):
            sha.update(pedaço)
            pedaço = arquivo.read(50_000)
    return sha.hexdigest()
