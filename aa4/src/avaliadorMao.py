from itertools import combinations

'''
Classe AvaliadorMao (utilitária)
Avalia a melhor combinação de 5 cartas a partir de 5..7 cartas (Texas Hold'em usa 7).
Categorias (rank, do menor ao maior):
0 - Carta Alta
1 - Par
2 - Dois Pares
3 - Trinca
4 - Sequência (Straight)
5 - Flush
6 - Full House
7 - Quadra
8 - Straight Flush
9 - Royal Flush

Métodos de classe:
avaliar(cartas): Retorna (rank, kickers) da melhor mão de 5.
descrever(rank, kickers): Retorna string humano-legível do resultado.
'''


class AvaliadorMao:
    CATEGORIAS = {
        0: 'Carta Alta',
        1: 'Par',
        2: 'Dois Pares',
        3: 'Trinca',
        4: 'Sequência',
        5: 'Flush',
        6: 'Full House',
        7: 'Quadra',
        8: 'Straight Flush',
        9: 'Royal Flush',
    }

    _NOMES_VALOR = {
        2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
        8: '8', 9: '9', 10: '10', 11: 'Valete', 12: 'Dama',
        13: 'Rei', 14: 'Ás'
    }

    _PLURAL_VALOR = {
        2: '2s', 3: '3s', 4: '4s', 5: '5s', 6: '6s', 7: '7s',
        8: '8s', 9: '9s', 10: '10s', 11: 'Valetes', 12: 'Damas',
        13: 'Reis', 14: 'Ases'
    }

    @classmethod
    def avaliar(cls, cartas):
        if len(cartas) < 5:
            raise ValueError("São necessárias pelo menos 5 cartas para avaliar.")
        melhor = None
        for cinco in combinations(cartas, 5):
            resultado = cls._avaliar_cinco(list(cinco))
            if melhor is None or resultado > melhor:
                melhor = resultado
        return melhor

    @classmethod
    def _avaliar_cinco(cls, cinco):
        valores = sorted([c.valor_numerico for c in cinco], reverse=True)
        contagens = cls._contagens(cinco)
        eh_flush = cls._eh_flush(cinco)
        seq_alta = cls._eh_sequencia(cinco)

        # Royal Flush: Straight Flush com carta alta = 14
        if eh_flush and seq_alta == 14:
            return (9, (14,))

        # Straight Flush
        if eh_flush and seq_alta is not None:
            return (8, (seq_alta,))

        # Quadra
        for valor, qtd in contagens.items():
            if qtd == 4:
                kicker = max(v for v in valores if v != valor)
                return (7, (valor, kicker))

        # Full House (trinca + par)
        trinca = None
        par = None
        for valor, qtd in sorted(contagens.items(), key=lambda x: (-x[1], -x[0])):
            if qtd == 3 and trinca is None:
                trinca = valor
            elif qtd >= 2 and par is None and valor != trinca:
                par = valor
        if trinca is not None and par is not None:
            return (6, (trinca, par))

        # Flush
        if eh_flush:
            return (5, tuple(valores))

        # Sequência
        if seq_alta is not None:
            return (4, (seq_alta,))

        # Trinca
        if trinca is not None:
            kickers = tuple(v for v in valores if v != trinca)[:2]
            return (3, (trinca,) + kickers)

        # Dois Pares / Par
        pares = sorted([v for v, q in contagens.items() if q == 2], reverse=True)
        if len(pares) >= 2:
            kicker = max(v for v in valores if v not in pares[:2])
            return (2, (pares[0], pares[1], kicker))
        if len(pares) == 1:
            kickers = tuple(v for v in valores if v != pares[0])[:3]
            return (1, (pares[0],) + kickers)

        # Carta Alta
        return (0, tuple(valores))

    @classmethod
    def _contagens(cls, cinco):
        contagens = {}
        for c in cinco:
            v = c.valor_numerico
            contagens[v] = contagens.get(v, 0) + 1
        return contagens

    @classmethod
    def _eh_flush(cls, cinco):
        naipes = {c.naipe for c in cinco}
        return len(naipes) == 1

    @classmethod
    def _eh_sequencia(cls, cinco):
        valores = sorted({c.valor_numerico for c in cinco})
        if len(valores) != 5:
            return None
        # Wheel: A-2-3-4-5 (Ás como 1)
        if valores == [2, 3, 4, 5, 14]:
            return 5
        if valores[-1] - valores[0] == 4:
            return valores[-1]
        return None

    @classmethod
    def descrever(cls, rank, kickers):
        nome = cls.CATEGORIAS[rank]
        if rank == 9:
            return "Royal Flush"
        if rank == 8:
            return f"Straight Flush até {cls._NOMES_VALOR[kickers[0]]}"
        if rank == 7:
            return f"Quadra de {cls._PLURAL_VALOR[kickers[0]]}"
        if rank == 6:
            return f"Full House de {cls._PLURAL_VALOR[kickers[0]]} com {cls._PLURAL_VALOR[kickers[1]]}"
        if rank == 5:
            return f"Flush, carta alta {cls._NOMES_VALOR[kickers[0]]}"
        if rank == 4:
            return f"Sequência até {cls._NOMES_VALOR[kickers[0]]}"
        if rank == 3:
            return f"Trinca de {cls._PLURAL_VALOR[kickers[0]]}"
        if rank == 2:
            return f"Dois Pares: {cls._PLURAL_VALOR[kickers[0]]} e {cls._PLURAL_VALOR[kickers[1]]}"
        if rank == 1:
            return f"Par de {cls._PLURAL_VALOR[kickers[0]]}"
        return f"Carta Alta {cls._NOMES_VALOR[kickers[0]]}"
