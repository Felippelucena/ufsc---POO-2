import json
from src.usuario import Usuario
from src.categoria import criar_categoria

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
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Erro ao salvar dados no arquivo {filename}.json: {e}")

    @classmethod
    def adicionar_usuario(cls, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("O objeto deve ser do tipo Usuario.")

        usuarios = cls.carregar_dados('usuarios')
        for u in usuarios:
            if u['nome'] == usuario.nome:
                raise ValueError(f"Usuário {usuario.nome} já existe.")

        usuarios.append(usuario.json())
        cls.salvar_dados('usuarios', usuarios)

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
    def buscar_usuario(cls, nome):
        usuarios = cls.carregar_dados('usuarios')
        for u in usuarios:
            if u['nome'] == nome:
                return Usuario(**u)
        return None
