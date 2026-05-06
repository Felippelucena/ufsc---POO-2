import os
from src.carta import Carta
from src.acao import Passar, Pagar, Aumentar, Desistir, AllIn

'''
Classe Jogador
Propriedades: nome, fichas, mao, aposta_rodada, estado.

Estados: 'ativo', 'desistiu', 'allin', 'quebrado'.

Métodos:
receber_carta(c), resetar_para_nova_rodada(), resetar_para_nova_partida(),
apostar(valor), desistir(), all_in(), receber_premio(valor),
decidir_acao(estado_mesa) -> retorna instância de Acao via input no terminal.
json(): Retorna dicionário para persistência.
'''


ESTADOS_VALIDOS = ('ativo', 'desistiu', 'allin', 'quebrado')


def _limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


class Jogador:
    def __init__(self, nome, fichas=0, mao=None, aposta_rodada=0, estado='ativo'):
        self.nome = nome
        self.fichas = fichas
        self.__mao = []
        if mao:
            for c in mao:
                if isinstance(c, Carta):
                    self.__mao.append(c)
                elif isinstance(c, dict):
                    self.__mao.append(Carta(**c))
        self.aposta_rodada = aposta_rodada
        self.estado = estado

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        if not isinstance(value, str) or len(value.strip()) < 2:
            raise ValueError("Nome deve ter ao menos 2 caracteres.")
        self.__nome = value.strip()

    @property
    def fichas(self):
        return self.__fichas

    @fichas.setter
    def fichas(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Fichas não podem ser negativas.")
        self.__fichas = value

    @property
    def mao(self):
        return list(self.__mao)

    @property
    def aposta_rodada(self):
        return self.__aposta_rodada

    @aposta_rodada.setter
    def aposta_rodada(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Aposta da rodada não pode ser negativa.")
        self.__aposta_rodada = value

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        if value not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Deve ser um de: {', '.join(ESTADOS_VALIDOS)}.")
        self.__estado = value

    def receber_carta(self, c):
        if not isinstance(c, Carta):
            raise ValueError("Carta inválida.")
        if len(self.__mao) >= 2:
            raise ValueError("Mão já tem 2 cartas.")
        self.__mao.append(c)

    def resetar_para_nova_rodada(self):
        self.aposta_rodada = 0

    def resetar_para_nova_partida(self):
        self.__mao = []
        self.aposta_rodada = 0
        if self.fichas > 0:
            self.estado = 'ativo'
        else:
            self.estado = 'quebrado'

    def apostar(self, valor):
        valor = int(valor)
        if valor <= 0 or self.__fichas == 0:
            return 0
        real = min(valor, self.__fichas)
        self.__fichas -= real
        self.__aposta_rodada += real
        if self.__fichas == 0:
            self.__estado = 'allin'
        return real

    def desistir(self):
        self.estado = 'desistiu'

    def all_in(self):
        return self.apostar(self.fichas)

    def receber_premio(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("Prêmio não pode ser negativo.")
        self.__fichas += valor

    def decidir_acao(self, estado_mesa):
        '''
        Apresenta o estado da mesa, lista as opções válidas e lê a escolha
        do jogador atual via input(). Retorna uma instância de Acao.
        '''
        _limpar_tela()
        input(f"=== Passe o teclado para {self.nome} e pressione Enter ===")
        _limpar_tela()

        diff = estado_mesa['aposta_atual'] - estado_mesa['minha_aposta']
        fichas = estado_mesa['minhas_fichas']

        opcoes = []
        if diff == 0:
            opcoes.append(('passar', 'Passar (check)'))
        if 0 < diff <= fichas:
            opcoes.append(('pagar', f'Pagar {diff}'))
        if fichas > diff and fichas > 0:
            opcoes.append(('aumentar', 'Aumentar (raise)'))
        if diff > 0:
            opcoes.append(('desistir', 'Desistir (fold)'))
        if fichas > 0:
            opcoes.append(('all_in', f'All-in ({fichas})'))

        cartas_str = ' '.join(str(c) for c in self.mao)
        comunit_str = ' '.join(str(c) for c in estado_mesa['comunitarias']) or '(nenhuma)'

        print(f"--- Vez de {self.nome} ---")
        print(f"  Comunitárias:   {comunit_str}")
        print(f"  Pote:           {estado_mesa['pote']}")
        print(f"  Aposta atual:   {estado_mesa['aposta_atual']}")
        print(f"  Jogadores em jogo: {estado_mesa['n_ativos']}")
        print(f"  Sua mão:        {cartas_str}")
        print(f"  Sua aposta:     {estado_mesa['minha_aposta']}")
        print(f"  Suas fichas:    {fichas}")
        print(f"  Para pagar:     {diff}")
        print("  Opções:")
        for i, (codigo, label) in enumerate(opcoes, start=1):
            print(f"    {i}. {label}")

        while True:
            escolha = input("  Escolha: ").strip()
            if not escolha.isdigit():
                print("  Inválido — digite o número da opção.")
                continue
            idx = int(escolha) - 1
            if not (0 <= idx < len(opcoes)):
                print("  Fora de faixa.")
                continue
            codigo = opcoes[idx][0]
            break

        if codigo == 'aumentar':
            min_extra = max(estado_mesa.get('big_blind', 1), 1)
            max_extra = fichas - diff
            while True:
                entrada = input(f"  Valor extra a aumentar (min {min_extra}, max {max_extra}): ").strip()
                if not entrada.isdigit():
                    print("  Valor inválido.")
                    continue
                extra = int(entrada)
                if extra < min_extra or extra > max_extra:
                    print(f"  Fora de faixa ({min_extra}..{max_extra}).")
                    continue
                acao = Aumentar(diff + extra)
                break
        elif codigo == 'pagar':
            acao = Pagar()
        elif codigo == 'all_in':
            acao = AllIn()
        elif codigo == 'passar':
            acao = Passar()
        else:
            acao = Desistir()

        input(f"  → Você escolheu: {acao}. Pressione Enter para passar a vez.")
        _limpar_tela()
        return acao

    def __str__(self):
        cartas_str = ' '.join(str(c) for c in self.__mao) if self.__mao else '(sem cartas)'
        return f"{self.__nome} | Fichas: {self.__fichas} | Estado: {self.__estado} | Mão: {cartas_str}"

    def json(self):
        return {
            "nome": self.nome,
            "fichas": self.fichas,
            "mao": [c.json() for c in self.__mao],
            "aposta_rodada": self.aposta_rodada,
            "estado": self.estado,
        }
