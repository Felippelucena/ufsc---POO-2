from src.baralho import Baralho
from src.pote import Pote
from src.jogador import Jogador

'''
Classe Mesa
Compõe Baralho e Pote. Agrega Jogadores e cartas comunitárias.

Propriedades:
jogadores: Lista de Jogador (2..4).
baralho: Instância Baralho.
pote: Instância Pote.
cartas_comunitarias: Lista de Carta (0..5).
small_blind, big_blind, aposta_atual, indice_dealer.

Métodos:
adicionar_jogador(j), remover_jogador(nome), jogadores_ativos(),
avancar_dealer(), resetar_para_nova_partida(), receber_aposta(j, valor),
colocar_comunitarias(n), estado_publico(jogador_visao=None).
'''


class Mesa:
    def __init__(self, small_blind=10, big_blind=20):
        self.__jogadores = []
        self.__baralho = Baralho()
        self.__pote = Pote()
        self.__cartas_comunitarias = []
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.__aposta_atual = 0
        self.__indice_dealer = 0

    @property
    def jogadores(self):
        return list(self.__jogadores)

    @property
    def baralho(self):
        return self.__baralho

    @property
    def pote(self):
        return self.__pote

    @property
    def cartas_comunitarias(self):
        return list(self.__cartas_comunitarias)

    @property
    def small_blind(self):
        return self.__small_blind

    @small_blind.setter
    def small_blind(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Small blind deve ser positivo.")
        self.__small_blind = value

    @property
    def big_blind(self):
        return self.__big_blind

    @big_blind.setter
    def big_blind(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Big blind deve ser positivo.")
        self.__big_blind = value

    @property
    def aposta_atual(self):
        return self.__aposta_atual

    @aposta_atual.setter
    def aposta_atual(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Aposta atual não pode ser negativa.")
        self.__aposta_atual = value

    @property
    def indice_dealer(self):
        return self.__indice_dealer

    def adicionar_jogador(self, j):
        if not isinstance(j, Jogador):
            raise ValueError("Apenas instâncias de Jogador podem ser adicionadas.")
        if len(self.__jogadores) >= 4:
            raise ValueError("Mesa cheia (máx 4 jogadores).")
        if any(jg.nome == j.nome for jg in self.__jogadores):
            raise ValueError(f"Já existe jogador com nome {j.nome}.")
        self.__jogadores.append(j)

    def remover_jogador(self, nome):
        self.__jogadores = [j for j in self.__jogadores if j.nome != nome]

    def jogadores_com_fichas(self):
        return [j for j in self.__jogadores if j.fichas > 0]

    def jogadores_ativos(self):
        return [j for j in self.__jogadores if j.estado in ('ativo', 'allin')]

    def jogadores_em_disputa(self):
        return [j for j in self.__jogadores if j.estado == 'ativo']

    def avancar_dealer(self):
        if not self.__jogadores:
            return
        n = len(self.__jogadores)
        for _ in range(n):
            self.__indice_dealer = (self.__indice_dealer + 1) % n
            if self.__jogadores[self.__indice_dealer].fichas > 0:
                return

    def resetar_para_nova_partida(self):
        self.__baralho.resetar()
        self.__pote.resetar()
        self.__cartas_comunitarias = []
        self.__aposta_atual = 0
        for j in self.__jogadores:
            j.resetar_para_nova_partida()

    def receber_aposta(self, jogador, valor):
        if jogador not in self.__jogadores:
            raise ValueError("Jogador não pertence a esta mesa.")
        real = jogador.apostar(valor)
        if real > 0:
            self.__pote.adicionar(jogador.nome, real)
            if jogador.aposta_rodada > self.__aposta_atual:
                self.__aposta_atual = jogador.aposta_rodada
        return real

    def colocar_comunitarias(self, n):
        n = int(n)
        if n <= 0:
            return
        self.__baralho.queimar()
        for _ in range(n):
            self.__cartas_comunitarias.append(self.__baralho.comprar())

    def estado_publico(self, jogador_visao=None):
        minha_aposta = jogador_visao.aposta_rodada if jogador_visao else 0
        minhas_fichas = jogador_visao.fichas if jogador_visao else 0
        return {
            "comunitarias": self.cartas_comunitarias,
            "pote": self.__pote.total,
            "aposta_atual": self.__aposta_atual,
            "minha_aposta": minha_aposta,
            "minhas_fichas": minhas_fichas,
            "n_ativos": len(self.jogadores_em_disputa()),
            "big_blind": self.__big_blind,
            "small_blind": self.__small_blind,
        }

    def __str__(self):
        comunit = ' '.join(str(c) for c in self.__cartas_comunitarias) or '(nenhuma)'
        linhas = [f"Mesa | Pote: {self.__pote.total} | Aposta atual: {self.__aposta_atual}"]
        linhas.append(f"Comunitárias: {comunit}")
        for i, j in enumerate(self.__jogadores):
            marca = '(D) ' if i == self.__indice_dealer else '    '
            linhas.append(f"  {marca}{j}")
        return '\n'.join(linhas)
