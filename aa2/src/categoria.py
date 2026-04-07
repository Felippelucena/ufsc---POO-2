from src.despesa import Despesa

'''
Classe Categoria (base) e subclasses por tipo:
- CategoriaEssencial: Água, Energia, Alimentação, Residência — alerta em 90% do limite.
- CategoriaVariavel: Transporte, Internet, Educação — alerta em 100% do limite.
- CategoriaDiscricionaria: Entretenimento — alerta em 80% do limite.

Propriedades:
Nome, Limite, Despesas, Total, Alerta.

Métodos:
total_mes(mes_ano): Retorna total de despesas para um mês específico.
json(): Retorna dicionário para persistência em JSON.

Função fábrica:
criar_categoria(**kwargs): Retorna a subclasse correta com base no nome da categoria.
'''


class Categoria:
    def __init__(self, nome, limite=None, despesas=None):
        self.nome = nome
        self.limite = limite
        self.despesas = despesas if despesas is not None else []

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        categorias_validas = [
            'Educação', 'Energia', 'Água', 'Internet',
            'Alimentação', 'Transporte', 'Residência', 'Entretenimento'
        ]
        if value not in categorias_validas:
            raise ValueError(f"Categoria inválida. Deve ser uma das seguintes: {', '.join(categorias_validas)}.")
        self.__nome = value

    @property
    def limite(self):
        return self.__limite

    @limite.setter
    def limite(self, value):
        if value is not None:
            value = float(value)
            if value <= 0:
                raise ValueError("O limite deve ser um valor positivo.")
        self.__limite = value

    @property
    def despesas(self):
        return [Despesa(**d) for d in self.__despesas]

    @despesas.setter
    def despesas(self, value):
        if isinstance(value, list):
            self.__despesas = value
        elif isinstance(value, dict):
            acao = value.pop("acao", None)
            if acao == "adicionar":
                self.__despesas.append(value)
            if acao == "remover":
                indice = value.get("indice", None)
                if indice is not None and 0 <= indice < len(self.__despesas):
                    self.__despesas.pop(indice)
        else:
            raise ValueError("A entrada deve ser uma lista ou dicionário.")

    @property
    def total(self):
        return sum(d['valor'] for d in self.__despesas)

    def total_mes(self, mes_ano):
        total = 0
        for d in self.__despesas:
            despesa = Despesa(**d)
            if despesa.mes_ano == mes_ano:
                total += d['valor']
        return total

    @property
    def mes_atual(self):
        '''Retorna o mês/ano mais recente (maior ano, maior mês) entre as despesas.'''
        if not self.__despesas:
            return None
        mais_recente = None
        for d in self.__despesas:
            despesa = Despesa(**d)
            ma = despesa.mes_ano  # "MM/AAAA"
            partes = ma.split('/')
            chave = (int(partes[1]), int(partes[0]))  # (ano, mes)
            if mais_recente is None or chave > mais_recente:
                mais_recente = chave
        return f"{mais_recente[1]:02d}/{mais_recente[0]}"

    @property
    def total_mes_atual(self):
        '''Total de despesas do mês mais recente.'''
        if self.mes_atual is None:
            return 0
        return self.total_mes(self.mes_atual)

    @property
    def alerta(self):
        '''Alerta base: dispara quando total do mês atual atinge 100% do limite. Subclasses sobrescrevem.'''
        if self.__limite is None or self.mes_atual is None:
            return None
        total = self.total_mes_atual
        if total >= self.__limite:
            return f"ALERTA {self.__nome}: R$ {total:.2f} atingiu o limite de R$ {self.__limite:.2f} em {self.mes_atual}!"
        return None

    def __str__(self):
        limite_str = f"R$ {self.__limite:.2f}" if self.__limite else "Sem limite"
        return f"{self.__nome} - Total: R$ {self.total:.2f} | Limite: {limite_str}"

    def json(self):
        return {
            "nome": self.nome,
            "limite": self.limite,
            "despesas": self.__despesas
        }


class CategoriaEssencial(Categoria):
    '''Categoria essencial (Água, Energia, Alimentação, Residência). Alerta em 90% do limite.'''
    def __init__(self, nome, limite=None, despesas=None):
        super().__init__(nome, limite, despesas)

    @property
    def alerta(self):
        if self.limite is None or self.mes_atual is None:
            return None
        total = self.total_mes_atual
        limiar = self.limite * 0.9
        if total >= self.limite:
            return f"ALERTA {self.nome}: R$ {total:.2f} ULTRAPASSOU o limite de R$ {self.limite:.2f} em {self.mes_atual}!"
        elif total >= limiar:
            return f"ALERTA {self.nome}: R$ {total:.2f} atingiu 90% do limite de R$ {self.limite:.2f} em {self.mes_atual}."
        return None


class CategoriaVariavel(Categoria):
    '''Categoria variável (Transporte, Internet, Educação). Alerta em 100% do limite.'''
    def __init__(self, nome, limite=None, despesas=None):
        super().__init__(nome, limite, despesas)

    @property
    def alerta(self):
        if self.limite is None or self.mes_atual is None:
            return None
        total = self.total_mes_atual
        if total >= self.limite:
            return f"ALERTA {self.nome}: R$ {total:.2f} atingiu o limite de R$ {self.limite:.2f} em {self.mes_atual}!"
        return None


class CategoriaDiscricionaria(Categoria):
    '''Categoria discricionária (Entretenimento). Alerta em 80% do limite.'''
    def __init__(self, nome, limite=None, despesas=None):
        super().__init__(nome, limite, despesas)

    @property
    def alerta(self):
        if self.limite is None or self.mes_atual is None:
            return None
        total = self.total_mes_atual
        limiar = self.limite * 0.8
        if total >= self.limite:
            return f"ALERTA {self.nome}: R$ {total:.2f} ULTRAPASSOU o limite de R$ {self.limite:.2f} em {self.mes_atual}!"
        elif total >= limiar:
            return f"ALERTA {self.nome}: R$ {total:.2f} atingiu 80% do limite de R$ {self.limite:.2f} em {self.mes_atual}."
        return None


def criar_categoria(**kwargs):
    '''Função fábrica: retorna a subclasse correta com base no nome da categoria.'''
    nome = kwargs.get('nome')

    essenciais = ['Água', 'Energia', 'Alimentação', 'Residência']
    discricionarias = ['Entretenimento']

    if nome in essenciais:
        return CategoriaEssencial(**kwargs)
    elif nome in discricionarias:
        return CategoriaDiscricionaria(**kwargs)
    else:
        return CategoriaVariavel(**kwargs)
