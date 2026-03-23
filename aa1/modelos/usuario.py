from .alimento import Alimento

class Usuario:
    def __init__(self, nome, sexo, idade, peso, altura, objetivo, nivel_atividade, consumo_diario=[], alimentos=[]):
        self.nome = nome
        self.sexo = sexo
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.objetivo = objetivo
        self.nivel_atividade = nivel_atividade
        self.consumo_diario = consumo_diario
        self.alimentos = alimentos
        
        self.__naf = {'sedentario': 1.2, 'leve': 1.375, 'moderado': 1.55, 'intenso': 1.725, 'muito intenso': 1.9}
    
    @property    
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, value):
        if not value or len(value) < 3:
            raise ValueError("O nome não pode ser vazio e deve ter pelo menos 3 caracteres.")
        self.__nome = value
        
    @property
    def sexo(self):
        return self.__sexo
    
    @sexo.setter
    def sexo(self, value):
        if value not in ['m', 'f']:
            raise ValueError("O sexo deve ser  masculino 'm' ou feminino 'f'.")
        self.__sexo = value
        
    @property
    def idade(self):
        return self.__idade
    
    @idade.setter
    def idade(self, value):
        if value < 5 or value > 100:
            raise ValueError("A idade deve ser entre 5 e 100 anos.")
        self.__idade = value
    
    @property
    def peso(self):
        return self.__peso

    @peso.setter
    def peso(self, value):
        if value <= 0 or value > 400:
            raise ValueError("O peso deve ser um valor positivo menor que 400kg.")
        self.__peso = value
        
    @property
    def altura(self):
        return self.__altura
    
    @altura.setter
    def altura(self, value):
        if value <= 0 or value > 250:
            raise ValueError("A altura deve ser um valor positivo menor que 250cm.")
        self.__altura = value
    
    @property
    def objetivo(self):
        return self.__objetivo
    
    @objetivo.setter
    def objetivo(self, value):
        objetivos_validos = ['perda de peso', 'manutenção', 'ganho de massa']
        if value not in objetivos_validos:
            raise ValueError(f"O objetivo deve ser um dos seguintes: {', '.join(objetivos_validos)}.")
        self.__objetivo = value
        
    @property
    def nivel_atividade(self):
        return self.__nivel_atividade
    
    @nivel_atividade.setter
    def nivel_atividade(self, value):
        niveis_validos = ['sedentario', 'leve', 'moderado', 'intenso', 'muito intenso']
        if value not in niveis_validos:
            raise ValueError(f"O nível de atividade deve ser um dos seguintes: {', '.join(niveis_validos)}.")
        self.__nivel_atividade = value
        
    @property
    def consumo_diario(self):
        return self.__consumo_diario
    
    @consumo_diario.setter
    def consumo_diario(self, value):
        if isinstance(value, dict):
            self.__consumo_diario = value
        elif isinstance(value, list):
            key = value.pop()
            self.__consumo_diario[key] = value
        else:
            raise ValueError("O consumo diário deve ser uma lista de alimentos consumidos.")

        
    @property
    def alimentos(self):
        return [Alimento(**a) for a in self.__alimentos]

    @alimentos.setter
    def alimentos(self, value):
        if isinstance(value, list):
            self.__alimentos = value
        elif isinstance(value, dict):
            acao = value.pop("acao", None)
            if acao == "adicionar":
                self.__alimentos.append(value)
            if acao == "atualizar":
                for i, a in enumerate(self.__alimentos):
                    if a['nome'] == value['nome']:
                        self.__alimentos[i] = value
                        break
            if acao == "remover":
                self.__alimentos = [a for a in self.__alimentos if a['nome'] != value['nome']]                
        else:
            raise ValueError("A entrada deve ser uma lista ou dicionário.")
        
    
    @property
    def tmb(self):
        if self.sexo == 'm':
            tmb = (10 * self.peso) + (6.65 * self.altura) - (5 * self.idade) + 5
        else:
            tmb = (10 * self.peso) + (6.65 * self.altura) - (5 * self.idade) - 161
        return tmb
    
    @property
    def get(self):
        tmb = self.tmb
        naf = self.__naf.get(self.nivel_atividade, 1.2)
        return tmb * naf

    def calcular_calorias_diarias(self):
        tmb = self.calcular_tmb()
        naf = self.__naf.get(self.nivel_atividade, 1.2)
        calorias_diarias = tmb * naf
        
        # Ajustar calorias com base no objetivo
        if self.objetivo == 'perda de peso':
            calorias_diarias -= 500
        elif self.objetivo == 'ganho de massa':
            calorias_diarias += 500
        
        return calorias_diarias

    # metodo para print
    def __str__(self):
        return f"{self.nome} - Idade: {self.idade}, Peso: {self.peso}kg, Altura: {self.altura}cm, Objetivo: {self.objetivo}, Nível de Atividade: {self.nivel_atividade}"
    
    def json(self):
        return {
            "nome": self.nome,
            "sexo": self.sexo,
            "idade": self.idade,
            "peso": self.peso,
            "altura": self.altura,
            "objetivo": self.objetivo,
            "nivel_atividade": self.nivel_atividade,
            "consumo_diario": self.consumo_diario,
            "alimentos": self.__alimentos
        }