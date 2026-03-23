'''
Classe Alimento
Porção: Quantidade em gramas do alimento.
Calorias: Calorias por porção (kcal).
Proteína: Quantidade de proteína por porção (g).
Carboidrato: Quantidade de carboidratos por porção (g).
Gordura: Quantidade de gordura por porção (g).
''' 

class Alimento:
    def __init__(self, nome, porcao, proteina, carboidrato, gordura):
        self.nome = nome
        self.porcao = porcao
        self.proteina = proteina
        self.carboidrato = carboidrato
        self.gordura = gordura
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, value):
        if not value or len(value) < 3:
            raise ValueError("O nome do alimento não pode ser vazio ou ter menos que 3 caracteres.")
        self.__nome = value
        
    @property
    def porcao(self):
        return self.__porcao
    
    @porcao.setter
    def porcao(self, value):
        if value <= 0 or value > 1000:
            raise ValueError("A porção deve ser um valor positivo até 1000g.")
        self.__porcao = value
        
    @property
    def proteina(self):
        return self.__proteina
    
    @proteina.setter
    def proteina(self, value):
        if value < 0 or value > 500:
            raise ValueError("A quantidade de proteína deve ser um valor positivo até 500g.")
        self.__proteina = value
        
    @property
    def carboidrato(self):
        return self.__carboidrato

    @carboidrato.setter
    def carboidrato(self, value):
        if value < 0 or value > 1000:
            raise ValueError("A quantidade de carboidratos deve ser um valor positivo até 1000g.")
        self.__carboidrato = value

    @property
    def gordura(self):
        return self.__gordura

    @gordura.setter
    def gordura(self, value):
        if value < 0 or value > 1000:
            raise ValueError("A quantidade de gordura deve ser um valor positivo até 1000g.")
        self.__gordura = value

    @property
    def calorias(self):
        return int((self.proteina * 4) + (self.carboidrato * 4) + (self.gordura * 9))

    # metodo para print
    def __str__(self):
        return f"{self.nome} - Porção: {self.porcao}g, Calorias: {self.calorias} kcal, Proteína: {self.proteina}g, Carboidrato: {self.carboidrato}g, Gordura: {self.gordura}g"
    
    def calorias_consumidas(self, porcao_consumida):
        if porcao_consumida <= 0:
            raise ValueError("A porção consumida deve ser um valor positivo em gramas.")
        return int(porcao_consumida * (self.calorias / self.porcao))

    def json(self):
        return {
            "nome": self.nome,
            "porcao": self.porcao,
            "proteina": self.proteina,
            "carboidrato": self.carboidrato,
            "gordura": self.gordura
        }