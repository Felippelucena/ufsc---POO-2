"Jogo de Poker Texas Hold'em"

import random as r

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.fichas = 0
        self.mao = []
        
    def passar():
        pass
    def apostar():
        pass
    def desistir():
        pass
    def pagar():
        pass
    def aumentar():
        pass
    def allin():
        pass
        
class Mesa:
    def __init__(self):
        self.jogadores = []
        self.rodada = []
        self.cartas_na_mesa = []
        self.fichas_na_mesa = 0
        self.baralho = Baralho()


class Dealer:
    def __init__(self):
        self.jogador_dealer = ''
        self.estado_mesa = 'aberto'
    
    def avancar_estado():
        estados = ['aberto','pré-flop']
    
class Baralho:
    def __init__(self):
        self.cartas = []
        self.peso = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
        self.construir_baralho()
        
    def construir_baralho(self):
        nipes = ['♥️','♦️','♠️','♣️']
        for x in nipes:
            for y in self.peso:
                self.cartas.append([y,x])

    def embaralhar(self):
        pilhas = [[],[],[],[],[]]
        for x in self.cartas:
            pilhas[r.randint(0,4)].append(x)
        self.cartas = pilhas[4]+pilhas[0]+pilhas[3]+pilhas[2]+pilhas[1]
        
b = Baralho()
b.embaralhar()
b.embaralhar()
print(b.cartas)