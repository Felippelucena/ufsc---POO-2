'''Objetivo

Desenvolver um software orientado a objetos para controle de dieta, permitindo que o usuário registre alimentos consumidos, calcule calorias diárias e acompanhe o progresso nutricional. O projeto deve seguir os princípios da Programação Orientada a Objetos (POO), utilizando classes, encapsulamento, herança e polimorfismo.

Requisitos do Sistema
O sistema deve permitir:

Cadastro de Usuários: Nome, idade, peso, altura, objetivo (perda de peso, manutenção, ganho de massa).
Cadastro de Alimentos: Nome, quantidade em gramas, calorias por porção, macronutrientes (proteína, carboidrato, gordura).
Registro de Consumo Diário: Usuário pode adicionar alimentos consumidos e visualizar um resumo diário.
Cálculo de Metabolismo Basal (TMB) e Gasto Energético Total (GET): Com base nas informações do usuário.
Relatórios: Exibir histórico de consumo e comparação com objetivos diários.
Critérios de Avaliação
O projeto será avaliado com base nos seguintes critérios:

Uso correto de POO: Aplicação de classes, métodos, atributos e boas práticas.
Encapsulamento: Proteção de dados e uso adequado de getters e setters.
Herança e Polimorfismo: Implementação de subclasses para diferentes categorias de usuários e alimentos.
Persistência de Dados: Utilização de arquivos JSON ou SQLite para armazenar registros.
Interface Simples: Pode ser via terminal ou uma interface gráfica opcional com Tkinter ou PyQt.
Código bem estruturado e comentado.'''


from modelos.bancoDeDados import BancoDeDados
from modelos.ui import Ui
from modelos.uiTerminal import UiTerminal
from modelos.usuario import Usuario
from modelos.alimento import Alimento



class App:
    def __init__(self):
        self.alimentos = [Alimento(**alimento) for alimento in BancoDeDados.carregar_dados('alimentos_global')]
        self.usuario_logado = None
        self.ui = UiTerminal(self)
    
    @property
    def usuario_logado(self):
        return self.__usuario_logado
    
    @usuario_logado.setter
    def usuario_logado(self, value : Usuario | None):
        if value is not None and not isinstance(value, Usuario):
            raise ValueError("O usuário logado deve ser do tipo Usuario ou None.")
        self.__usuario_logado = value
    
    def adicionar_usuario(self, usuario: dict):
        usuario = Usuario(**usuario)
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
    
    
if __name__ == "__main__":
    app = App()
    app.ui.iniciar()