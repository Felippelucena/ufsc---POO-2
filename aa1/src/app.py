from src.bancoDeDados import BancoDeDados
from src.usuario import Usuario, criar_usuario
from src.alimento import Alimento

class App:
    def __init__(self):
        self.alimentos = [Alimento(**alimento) for alimento in BancoDeDados.carregar_dados('alimentos_global')]
        self.usuario_logado = None
    
    @property
    def usuario_logado(self):
        return self.__usuario_logado
    
    @usuario_logado.setter
    def usuario_logado(self, value : Usuario | None):
        if value is not None and not isinstance(value, Usuario):
            raise ValueError("O usuário logado deve ser do tipo Usuario ou None.")
        self.__usuario_logado = value
    
    def adicionar_usuario(self, usuario: dict):
        usuario = criar_usuario(**usuario)
        BancoDeDados.adicionar_usuario(usuario)
        self.usuario_logado = usuario
    
    def atualizar_usuario(self, usuario: dict):
        for k, v in usuario.items():
            setattr(self.usuario_logado, k, v)
        BancoDeDados.atualizar_usuario(self.usuario_logado)
        
    def logout(self):
        BancoDeDados.atualizar_usuario(self.usuario_logado)
        self.usuario_logado = None
    
    def entrar_usuario(self, nome: str):
        usuario = BancoDeDados.buscar_usuario(nome)
        if usuario:
            self.usuario_logado = usuario
            return True
        return False

    def alterar_alimentos_usuario(self, alimento: dict, acao: str):
        if not self.usuario_logado: raise ValueError("Nenhum usuário logado para alterar alimentos.")
        
        if acao == "adicionar": alimento['acao'] = "adicionar"
        elif acao == "atualizar": alimento['acao'] = "atualizar"
        elif acao == "remover": alimento['acao'] = "remover"
        else: raise ValueError("A ação deve ser 'adicionar', 'atualizar' ou 'remover'.")
        
        self.usuario_logado.alimentos = alimento
        BancoDeDados.atualizar_usuario(self.usuario_logado)
    
    def registrar_consumo_diario(self, data: str, consumo: list):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado para registrar consumo.")
        consumo.append(data)
        self.usuario_logado.consumo_diario = consumo
        BancoDeDados.atualizar_usuario(self.usuario_logado)
    