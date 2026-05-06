import random
from src.carta import Carta

'''
Classe Baralho
Propriedades:
cartas: Lista de cartas restantes no baralho (lista de Carta).
tamanho: Quantidade de cartas restantes.

Métodos:
construir_baralho(): Popula 52 cartas (13 valores x 4 naipes).
embaralhar(): Embaralha as cartas usando random.shuffle.
comprar(): Saca a carta do topo (retorna e remove).
queimar(): Descarta a carta do topo (sem retornar).
resetar(): Reconstrói o baralho do zero e embaralha.
'''


class Baralho:
    _VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    _NAIPES = ['♥️', '♦️', '♠️', '♣️']

    def __init__(self):
        self.__cartas = []
        self.construir_baralho()
        self.embaralhar()

    @property
    def cartas(self):
        return list(self.__cartas)

    @property
    def tamanho(self):
        return len(self.__cartas)

    def construir_baralho(self):
        self.__cartas = []
        for naipe in self._NAIPES:
            for valor in self._VALORES:
                self.__cartas.append(Carta(valor, naipe))

    def embaralhar(self):
        random.shuffle(self.__cartas)

    def comprar(self):
        if not self.__cartas:
            raise ValueError("Baralho vazio.")
        return self.__cartas.pop()

    def queimar(self):
        if not self.__cartas:
            raise ValueError("Baralho vazio.")
        self.__cartas.pop()

    def resetar(self):
        self.construir_baralho()
        self.embaralhar()
