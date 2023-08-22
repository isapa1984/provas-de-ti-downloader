class Modulo:
    def __init__(self):
        self.nome: str  = ''
        self.url: str = ''
        self.arquivo: str = ''
        self.diretorio: str = ''

class Trilha:
    def __init__(self):
        self.nome: str = ''
        self.modulos: list[Modulo] = []

class Disciplina:
    def __init__(self):
        self.nome: str = ''
        self.trilhas: list[Trilha] = []

    def __eq__(self, other: object) -> bool:
        return self.nome == other.nome