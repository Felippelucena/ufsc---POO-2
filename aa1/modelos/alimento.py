'''
Classe Alimento
Porção: Quantidade em gramas do alimento.
Calorias: Calorias por porção (kcal).
Proteína: Quantidade de proteína por porção (g).
Carboidrato: Quantidade de carboidratos por porção (g).
Gordura: Quantidade de gordura por porção (g).
''' 

class Alimento:
    def __init__(self, nome, porcao, calorias, proteina, carboidrato, gordura):
        self.nome = nome
        self.porcao = porcao
        self.calorias = calorias
        self.proteina = proteina
        self.carboidrato = carboidrato
        self.gordura = gordura
    
    # metodo para print
    def __str__(self):
        return f"{self.nome} - Porção: {self.porcao}g, Calorias: {self.calorias} kcal, Proteína: {self.proteina}g, Carboidrato: {self.carboidrato}g, Gordura: {self.gordura}g"
