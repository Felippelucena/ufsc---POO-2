import json
from .usuario import Usuario
from .alimento import Alimento

class BancoDeDados:
    @classmethod      
    def carregar_dados(cls, filename):
        try:
            with open(f'./aa1/db/{filename}.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    @classmethod    
    def salvar_dados(cls, filename, data):
        with open(f'./aa1/db/{filename}.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    @classmethod        
    def adicionar_usuario(cls, usuario):
        #verificar se o usuario é do tipo Usuario
        if not isinstance(usuario, Usuario):
            raise ValueError("O objeto deve ser do tipo Usuario.")
        
        usuarios = cls.carregar_dados('usuarios')
        # Verificar se o usuário já existe
        for u in usuarios:
            if u['nome'] == usuario.nome:
                return print(f"Usuário {usuario.nome} já existe.")

        usuarios.append(usuario.json())
        cls.salvar_dados('usuarios', usuarios)

        print(f"Usuário {usuario.nome} adicionado com sucesso.")
    
    @classmethod
    def atualizar_usuario(cls, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("O objeto deve ser do tipo Usuario.")
        
        usuarios = cls.carregar_dados('usuarios')
        for i, u in enumerate(usuarios):
            if u['nome'] == usuario.nome:
                usuarios[i] = usuario.json()
                cls.salvar_dados('usuarios', usuarios)
                print(f"Usuário {usuario.nome} atualizado com sucesso.")
                return
        print(f"Usuário {usuario.nome} não encontrado para atualização.")
    
    @classmethod
    def adicionar_alimento(cls, alimento):
        #verificar se o alimento é do tipo Alimento
        if not isinstance(alimento, Alimento):
            raise ValueError("O objeto deve ser do tipo Alimento.")
        
        alimentos = cls.carregar_dados('alimentos_global')
        for a in alimentos:
            if a['nome'] == alimento.nome:
                return print(f"Alimento {alimento.nome} já existe.")

        alimentos.append(alimento.json())
        cls.salvar_dados('alimentos_global', alimentos)

        print(f"Alimento {alimento.nome} adicionado com sucesso.")
        
    @classmethod
    def buscar_usuario(cls, nome):
        usuarios = cls.carregar_dados('usuarios')
        for u in usuarios:
            if u['nome'] == nome:
                return Usuario(**u)
        return None

