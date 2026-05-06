'''
Classe Carta
Propriedades:
Valor: Valor da carta ('2'..'10', 'J', 'Q', 'K', 'A').
Naipe: Naipe da carta ('♥️', '♦️', '♠️', '♣️').

Propriedade calculada:
valor_numerico: Inteiro 2..14 usado para comparação na avaliação de mãos.

Métodos:
json(): Retorna dicionário para persistência em JSON.
'''


class Carta:
    VALORES_VALIDOS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    NAIPES_VALIDOS = ['♥️', '♦️', '♠️', '♣️']
    _MAPA_VALOR = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, value):
        value = str(value)
        if value not in self.VALORES_VALIDOS:
            raise ValueError(f"Valor inválido. Deve ser um de: {', '.join(self.VALORES_VALIDOS)}.")
        self.__valor = value

    @property
    def naipe(self):
        return self.__naipe

    @naipe.setter
    def naipe(self, value):
        if value not in self.NAIPES_VALIDOS:
            raise ValueError(f"Naipe inválido. Deve ser um de: {', '.join(self.NAIPES_VALIDOS)}.")
        self.__naipe = value

    @property
    def valor_numerico(self):
        return self._MAPA_VALOR[self.__valor]

    def __str__(self):
        return f"{self.__valor}{self.__naipe}"

    def __repr__(self):
        return f"Carta({self.__valor!r}, {self.__naipe!r})"

    def json(self):
        return {"valor": self.valor, "naipe": self.naipe}
