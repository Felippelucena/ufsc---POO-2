import random
from src.carta import Carta
from src.avaliadorMao import AvaliadorMao

'''
Classe Jogador (base) e subclasses:
- JogadorHumano: decide via input() no terminal.
- JogadorIA: decide via heurística baseada em força da mão e personalidade.

Propriedades:
nome, fichas, mao, aposta_rodada, estado.

Métodos:
receber_carta(c), resetar_para_nova_rodada(), resetar_para_nova_partida(),
apostar(valor), desistir(), all_in(), decidir_acao(estado_mesa).
json(): Retorna dicionário para persistência.

Função fábrica:
criar_jogador(**kwargs): Retorna a subclasse correta com base no parâmetro 'tipo'.
'''


ESTADOS_VALIDOS = ('ativo', 'desistiu', 'allin', 'quebrado')


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
        raise NotImplementedError("decidir_acao deve ser implementado pela subclasse.")

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
            "tipo": "humano" if isinstance(self, JogadorHumano) else "ia",
        }


class JogadorHumano(Jogador):
    '''Jogador humano: decisão via input() no terminal.'''

    def decidir_acao(self, estado_mesa):
        diff = estado_mesa['aposta_atual'] - estado_mesa['minha_aposta']
        fichas = estado_mesa['minhas_fichas']

        opcoes = []
        if diff == 0:
            opcoes.append(('passar', 'Passar (check)'))
        if 0 < diff <= fichas:
            opcoes.append(('pagar', f'Pagar {diff}'))
        if fichas > diff:
            opcoes.append(('aumentar', 'Aumentar (raise)'))
        if diff > 0:
            opcoes.append(('desistir', 'Desistir (fold)'))
        if fichas > 0:
            opcoes.append(('all_in', f'All-in ({fichas})'))

        cartas_str = ' '.join(str(c) for c in self.mao)
        comunit_str = ' '.join(str(c) for c in estado_mesa['comunitarias']) or '(nenhuma)'
        print(f"\n--- Sua vez, {self.nome} ---")
        print(f"  Sua mão:        {cartas_str}")
        print(f"  Comunitárias:   {comunit_str}")
        print(f"  Pote:           {estado_mesa['pote']}")
        print(f"  Aposta atual:   {estado_mesa['aposta_atual']}")
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
                print("  Índice fora de faixa.")
                continue
            acao = opcoes[idx][0]
            break

        if acao == 'aumentar':
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
                return {"acao": "aumentar", "valor": diff + extra}
        if acao == 'pagar':
            return {"acao": "pagar", "valor": diff}
        if acao == 'all_in':
            return {"acao": "all_in", "valor": fichas}
        if acao == 'passar':
            return {"acao": "passar", "valor": 0}
        return {"acao": "desistir", "valor": 0}


class JogadorIA(Jogador):
    '''Jogador controlado por IA: decisão via heurística + personalidade.'''

    PERSONALIDADES = ('cauteloso', 'equilibrado', 'agressivo')
    _PERFIS = {
        'cauteloso':   {'min_pagar': 0.40, 'min_aumentar': 0.70, 'min_allin': 0.92},
        'equilibrado': {'min_pagar': 0.30, 'min_aumentar': 0.55, 'min_allin': 0.85},
        'agressivo':   {'min_pagar': 0.20, 'min_aumentar': 0.40, 'min_allin': 0.75},
    }

    def __init__(self, nome, fichas=0, mao=None, aposta_rodada=0, estado='ativo', personalidade='equilibrado'):
        super().__init__(nome, fichas, mao, aposta_rodada, estado)
        self.personalidade = personalidade

    @property
    def personalidade(self):
        return self.__personalidade

    @personalidade.setter
    def personalidade(self, value):
        if value not in self.PERSONALIDADES:
            raise ValueError(f"Personalidade inválida. Deve ser uma de: {', '.join(self.PERSONALIDADES)}.")
        self.__personalidade = value

    def _estimar_forca(self, estado_mesa):
        comunit = estado_mesa['comunitarias']
        if len(comunit) == 0:
            return self._forca_pre_flop()
        cartas = self.mao + list(comunit)
        rank, _ = AvaliadorMao.avaliar(cartas)
        forca = rank * 0.10 + 0.05
        forca += random.uniform(-0.05, 0.05)
        return max(0.0, min(1.0, forca))

    def _forca_pre_flop(self):
        if len(self.mao) < 2:
            return 0.0
        c1, c2 = self.mao[0], self.mao[1]
        v1, v2 = c1.valor_numerico, c2.valor_numerico
        maior, menor = max(v1, v2), min(v1, v2)
        suited = c1.naipe == c2.naipe

        if v1 == v2:
            if v1 >= 13:
                return 0.95
            if v1 >= 10:
                return 0.85
            if v1 >= 7:
                return 0.70
            return 0.55
        if maior >= 10 and menor >= 10:
            return 0.70 if suited else 0.55
        if maior - menor <= 2 and suited:
            return 0.45
        forca = (maior + menor) / 28.0
        if suited:
            forca += 0.05
        return max(0.05, min(0.95, forca))

    def decidir_acao(self, estado_mesa):
        forca = self._estimar_forca(estado_mesa)
        thresholds = self._PERFIS[self.__personalidade]
        diff = estado_mesa['aposta_atual'] - estado_mesa['minha_aposta']
        fichas = estado_mesa['minhas_fichas']
        bb = estado_mesa.get('big_blind', 20)

        if fichas <= 0:
            return {"acao": "passar", "valor": 0}

        if forca >= thresholds['min_allin']:
            return {"acao": "all_in", "valor": fichas}

        if forca >= thresholds['min_aumentar']:
            extra = max(bb, int(fichas * 0.30))
            valor_total = diff + extra
            if valor_total >= fichas:
                return {"acao": "all_in", "valor": fichas}
            return {"acao": "aumentar", "valor": valor_total}

        if forca >= thresholds['min_pagar']:
            if diff == 0:
                return {"acao": "passar", "valor": 0}
            if diff < fichas:
                return {"acao": "pagar", "valor": diff}
            return {"acao": "all_in", "valor": fichas}

        if diff == 0:
            return {"acao": "passar", "valor": 0}
        return {"acao": "desistir", "valor": 0}


def criar_jogador(**kwargs):
    '''Função fábrica: devolve JogadorHumano ou JogadorIA conforme tipo.'''
    tipo = kwargs.pop('tipo', 'humano')
    if tipo == 'humano':
        kwargs.pop('personalidade', None)
        return JogadorHumano(**kwargs)
    if tipo == 'ia':
        if 'personalidade' not in kwargs:
            kwargs['personalidade'] = random.choice(JogadorIA.PERSONALIDADES)
        return JogadorIA(**kwargs)
    raise ValueError(f"Tipo de jogador inválido: {tipo}.")
