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
from modelos.usuario import Usuario
from modelos.alimento import Alimento

class UiTerminal:
    def __init__(self, app : App):
        self.app = app
    
    def iniciar(self):
        self.menu_inicial()
    
    def menu_inicial(self):
        print("Bem-vindo ao Controle de Dieta!")
        print("1. Cadastrar Usuário")
        print("2. Entrar com Usuário")

        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.cadastrar_usuario()
        elif escolha == '2':
            self.entrar_usuario()
        elif escolha == '0':
            print("Saindo...")
            return
        else:
            print("Opção inválida!")
            self.menu_inicial()
    
    def cadastrar_usuario(self):
        try:
            user = {
                "nome": input("Nome: "),
                "sexo": input("Sexo (m/f): "),
                "idade": int(input("Idade: ")),
                "peso": float(input("Peso (kg): ")),
                "altura": float(input("Altura (cm): ")),
                "objetivo": input("Objetivo (perda de peso, manutenção, ganho de massa): "),
                "nivel_atividade": input("Nível de Atividade (sedentario, leve, moderado, intenso, muito intenso): ")
            }
            self.app.adicionar_usuario(user)
            
        except ValueError as e:
            print(f"Entrada inválida: {e}")
            self.cadastrar_usuario()
            
    def perfil(self):
        if not self.app.usuario_logado: return print("Usuário não logado. Retornando ao menu inicial.")
        
        print(f'--- Dashboard Dieta em Dia ---')
        print(f'Idade: {self.app.usuario_logado.idade}, Peso: {self.app.usuario_logado.peso}kg, Altura: {self.app.usuario_logado.altura}cm')
        print(f'Objetivo: {self.app.usuario_logado.objetivo}, Nível de Atividade: {self.app.usuario_logado.nivel_atividade}')
        print(f'TMB: {self.app.usuario_logado.tmb:.2f} kcal, GET: {self.app.usuario_logado.get:.2f} kcal')
        print('1. Registrar Consumo do Dia')
        print('0. Sair')
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.registrar_consumo()
            self.perfil()
        elif escolha == '0':
            print("Saindo...")
            self.menu_inicial()
        else:
            print("Opção inválida!")
            self.perfil()

    def entrar_usuario(self):
        nome = input("Digite seu nome para entrar: ")
        self.app.entrar_usuario(nome)
    
    def registrar_consumo(self):
        if not self.app.usuario_logado: return print("Usuário não logado. Retornando ao menu inicial.")


class App:
    def __init__(self):
        self.alimentos = [Alimento(**alimento) for alimento in BancoDeDados.carregar_dados('alimentos')]
        self.usuario_logado = None
        self.ui = UiTerminal(self)
    
    @property
    def usuario_logado(self):
        return self.__usuario_logado
    
    @usuario_logado.setter
    def usuario_logado(self, value):
        if value is not None and not isinstance(value, Usuario):
            raise ValueError("O usuário logado deve ser do tipo Usuario ou None.")
        self.__usuario_logado = value
    
    def adicionar_usuario(self, usuario):
        usuario = Usuario(**usuario)
        BancoDeDados.adicionar_usuario(usuario)
        self.ui.menu_inicial()
    
    def entrar_usuario(self, nome):
        usuario = BancoDeDados.buscar_usuario(nome)
        if usuario:
            self.usuario_logado = usuario
            print(f"Bem-vindo, {usuario.nome}!")
            self.ui.perfil()
            return
        print("Usuário não encontrado. Retornando ao menu inicial.")
        self.ui.menu_inicial()

if __name__ == "__main__":
    app = App()
    app.ui.iniciar()