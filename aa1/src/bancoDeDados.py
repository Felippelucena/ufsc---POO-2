import json
from src.usuario import Usuario
from src.alimento import Alimento

class BancoDeDados:
    @classmethod      
    def carregar_dados(cls, filename):
        try:
            with open(f'./db/{filename}.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"O arquivo {filename}.json não foi encontrado.")
        except json.JSONDecodeError:
            raise ValueError(f"O arquivo {filename}.json contém dados inválidos.")
    
    @classmethod    
    def salvar_dados(cls, filename, data):
        try:
            with open(f'./db/{filename}.json', 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            raise ValueError(f"Erro ao salvar dados no arquivo {filename}.json: {e}")

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
                return
    
    @classmethod
    def adicionar_alimento_global(cls, alimento):
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

