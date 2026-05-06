'''
Classe Pote
Propriedades:
contribuicoes: Dicionário {nome_jogador: total_apostado} (cópia retornada).
total: Soma total das contribuições.

Métodos:
adicionar(nome, valor): Soma valor à contribuição do jogador nomeado.
resetar(): Zera todas as contribuições.
distribuir(vencedores): Divide o total igualmente entre os vencedores; resto vai para o primeiro.
json(): Retorna dicionário para persistência em JSON.
'''


class Pote:
    def __init__(self):
        self.__contribuicoes = {}

    @property
    def contribuicoes(self):
        return dict(self.__contribuicoes)

    @property
    def total(self):
        return sum(self.__contribuicoes.values())

    def adicionar(self, nome, valor):
        if not isinstance(nome, str) or not nome:
            raise ValueError("Nome do jogador deve ser uma string não vazia.")
        valor = int(valor)
        if valor < 0:
            raise ValueError("Valor não pode ser negativo.")
        if valor == 0:
            return
        self.__contribuicoes[nome] = self.__contribuicoes.get(nome, 0) + valor

    def resetar(self):
        self.__contribuicoes = {}

    def distribuir(self, vencedores):
        if not vencedores:
            raise ValueError("Lista de vencedores vazia.")
        total = self.total
        n = len(vencedores)
        cota = total // n
        resto = total - cota * n
        resultado = {nome: cota for nome in vencedores}
        if resto > 0:
            resultado[vencedores[0]] += resto
        self.resetar()
        return resultado

    def json(self):
        return {"contribuicoes": dict(self.__contribuicoes), "total": self.total}
