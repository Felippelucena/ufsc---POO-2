import json

class BancoDeDados:
          
    def carregar_dados(self, filename):
        try:
            with open(f'./aa1/db/{filename}.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def salvar_dados(self, filename, data):
        with open(f'./aa1/db/{filename}.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            
    def adicionar_usuario(self, usuario):
        if usuario.nome in self.usuarios: return print(f"Usuário {usuario.nome} já existe.")
        
        self.usuarios[usuario.nome] = usuario.__dict__
        self.salvar_dados('usuarios', self.usuarios)
        
        print(f"Usuário {usuario.nome} adicionado com sucesso.")
    
    def adicionar_alimento(self, alimento):
        if alimento.nome in self.alimentos: return print(f"Alimento {alimento.nome} já existe.")
        
        self.alimentos[alimento.nome] = alimento.__dict__
        self.salvar_dados('alimentos', self.alimentos)
        
        print(f"Alimento {alimento.nome} adicionado com sucesso.")
