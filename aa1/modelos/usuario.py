class Usuario:
    def __init__(self, nome, idade, peso, altura, objetivo):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.objetivo = objetivo
        self.consumo_diario = 0
        
    # metodo para print
    def __str__(self):
        return f"{self.nome} - Idade: {self.idade}, Peso: {self.peso}kg, Altura: {self.altura}cm, Objetivo: {self.objetivo}, Consumo Diário: {self.consumo_diario} kcal"