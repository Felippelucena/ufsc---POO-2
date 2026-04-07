from datetime import datetime

'''
Classe Despesa
Propriedades:
Valor: Valor da despesa (float > 0).
Categoria: Categoria da despesa (str em lista válida).
Data: Data da despesa (formato DD/MM/AAAA).
Descrição: Descrição breve da despesa (min 3 caracteres).

Propriedade calculada:
mes_ano: Extrai "MM/AAAA" da data para agrupamento mensal.

Métodos:
json(): Retorna dicionário para persistência em JSON.
'''


class Despesa:
    CATEGORIAS_VALIDAS = [
        'Educação', 'Energia', 'Água', 'Internet',
        'Alimentação', 'Transporte', 'Residência', 'Entretenimento'
    ]

    def __init__(self, valor, categoria, data, descricao):
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, value):
        value = float(value)
        if value <= 0 or value > 1000000:
            raise ValueError("O valor deve ser positivo e menor que R$ 1.000.000,00.")
        self.__valor = value

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, value):
        if value not in self.CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria inválida. Deve ser uma das seguintes: {', '.join(self.CATEGORIAS_VALIDAS)}.")
        self.__categoria = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        try:
            datetime.strptime(value, '%d/%m/%Y')
        except ValueError:
            raise ValueError("A data deve estar no formato DD/MM/AAAA.")
        self.__data = value

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        if not value or len(value) < 3:
            raise ValueError("A descrição não pode ser vazia e deve ter pelo menos 3 caracteres.")
        self.__descricao = value

    @property
    def mes_ano(self):
        partes = self.__data.split('/')
        return f"{partes[1]}/{partes[2]}"

    def __str__(self):
        return f"{self.data} - {self.categoria}: R$ {self.valor:.2f} - {self.descricao}"

    def json(self):
        return {
            "valor": self.valor,
            "categoria": self.categoria,
            "data": self.data,
            "descricao": self.descricao
        }
