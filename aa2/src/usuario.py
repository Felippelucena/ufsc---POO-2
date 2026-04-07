from src.controleFinanceiro import ControleFinanceiro
from src.categoria import criar_categoria

'''
Classe Usuario
Propriedades:
Nome: Nome do usuário (min 3 caracteres).
Email: Email do usuário (deve conter @ e .).
Controle Financeiro: Instância de ControleFinanceiro.

Métodos:
json(): Retorna dicionário para persistência em JSON.
'''


class Usuario:
    def __init__(self, nome, email, controle_financeiro={}):
        self.nome = nome
        self.email = email
        self.controle_financeiro = controle_financeiro

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        if not value or len(value) < 3:
            raise ValueError("O nome não pode ser vazio e deve ter pelo menos 3 caracteres.")
        self.__nome = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not value or '@' not in value or '.' not in value:
            raise ValueError("O email deve conter '@' e '.'.")
        self.__email = value

    @property
    def controle_financeiro(self):
        return self.__controle_financeiro

    @controle_financeiro.setter
    def controle_financeiro(self, value):
        if isinstance(value, ControleFinanceiro):
            self.__controle_financeiro = value
        elif isinstance(value, dict):
            categorias_dict = value.get("categorias", {})
            categorias = {}
            for nome, cat_data in categorias_dict.items():
                categorias[nome] = criar_categoria(**cat_data)
            self.__controle_financeiro = ControleFinanceiro(categorias)
        else:
            raise ValueError("O controle financeiro deve ser um dicionário ou instância de ControleFinanceiro.")

    def __str__(self):
        return f"{self.nome} - {self.email}"

    def json(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "controle_financeiro": self.__controle_financeiro.json()
        }
