from src.categoria import Categoria, criar_categoria

'''
Classe ControleFinanceiro
Propriedades:
Categorias: dicionário nome → Categoria.

Métodos:
total_geral(): Soma total de todas as categorias.
total_mes(mes_ano): Total para um mês específico.
relatorio_mensal(mes_ano): Dicionário categoria → total do mês.
comparar_meses(mes1, mes2): Comparação entre dois meses.
alertas(): Lista de alertas de todas as categorias.
json(): Retorna dicionário para persistência em JSON.
'''


class ControleFinanceiro:
    def __init__(self, categorias=None):
        self.categorias = categorias if categorias is not None else {}

    @property
    def categorias(self):
        return self.__categorias

    @categorias.setter
    def categorias(self, value):
        if not isinstance(value, dict):
            raise ValueError("As categorias devem ser um dicionário.")
        self.__categorias = value

    def total_geral(self):
        return sum(cat.total for cat in self.__categorias.values())

    def total_mes(self, mes_ano):
        return sum(cat.total_mes(mes_ano) for cat in self.__categorias.values())

    def relatorio_mensal(self, mes_ano):
        relatorio = {}
        for nome, cat in self.__categorias.items():
            total = cat.total_mes(mes_ano)
            relatorio[nome] = {
                "total": total,
                "limite": cat.limite,
            }
        relatorio["TOTAL"] = self.total_mes(mes_ano)
        return relatorio

    def comparar_meses(self, mes1, mes2):
        comparacao = {}
        for nome, cat in self.__categorias.items():
            total1 = cat.total_mes(mes1)
            total2 = cat.total_mes(mes2)
            diferenca = total2 - total1
            percentual = (diferenca / total1 * 100) if total1 > 0 else 0
            comparacao[nome] = {
                "mes1": total1,
                "mes2": total2,
                "diferenca": diferenca,
                "percentual": percentual,
                "aumento_significativo": percentual > 20
            }
        return comparacao

    def alertas(self):
        lista = []
        for cat in self.__categorias.values():
            alerta = cat.alerta
            if alerta:
                lista.append(alerta)
        return lista

    def json(self):
        categorias_json = {}
        for nome, cat in self.__categorias.items():
            categorias_json[nome] = cat.json()
        return {"categorias": categorias_json}
