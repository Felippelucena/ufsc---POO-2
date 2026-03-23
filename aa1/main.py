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
        print("")
        print("Bem-vindo ao Dieta em Dia!")
        print("1. Cadastrar Usuário | 2. Entrar | 0. Sair")
        
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.cadastrar_usuario()
            self.perfil() 
        elif escolha == '2':
            if self.entrar_usuario():
                self.perfil()    
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
        print("")
        if not self.app.usuario_logado: return print("Usuário não logado. Retornando ao menu inicial.")
        
        print(f'----- Dashboard Dieta em Dia -----')
        print(f"Bem-vindo, {self.app.usuario_logado.nome} | Idade: {self.app.usuario_logado.idade}, Peso: {self.app.usuario_logado.peso}kg, Altura: {self.app.usuario_logado.altura}cm")
        print(f'Objetivo: {self.app.usuario_logado.objetivo} | Nível de Atividade: {self.app.usuario_logado.nivel_atividade} | TMB: {self.app.usuario_logado.tmb:.2f} kcal | GET: {self.app.usuario_logado.get:.2f} kcal')
        print('1. Registrar Consumo do Dia | 2. Ver Alimentos Cadastrados | 3. Cadastrar Novo Alimento')
        print('4. Atualizar Perfil | 5. Ver Histórico de Consumo | 0. Sair')
        
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            self.registrar_consumo_do_dia()
        elif escolha == '2':
            self.alimentos_disponiveis()

        elif escolha == '3':
            self.cadastrar_alimento()
        elif escolha == '0':
            print("Saindo...")
            self.app.logout()
            return
        else:
            print("Opção inválida!")
        
        self.perfil()
        
    def alimentos_disponiveis(self):
        print("Alimentos Globais:")
        for alimento in self.app.alimentos:
            print(f"{alimento.nome} - {alimento.porcao}g - {alimento.calorias:.2f} kcal")
        print("Seus Alimentos:")
        for i, alimento in enumerate(self.app.usuario_logado.alimentos):
            print(f"{i + 1}. {alimento.nome} - {alimento.porcao}g - {alimento.calorias:.2f} kcal")
            

    def entrar_usuario(self):
        nome = input("Digite seu nome para entrar: ")
        if self.app.entrar_usuario(nome):
            return True
        else:
            print("Usuário não encontrado. Retornando ao menu inicial.")
            return False
        
    
    def registrar_consumo_do_dia(self):
        if not self.app.usuario_logado: return print("Usuário não logado. Retornando ao menu inicial.")
        print("Alimentos disponíveis:")
        todos_alimentos = self.app.alimentos + self.app.usuario_logado.alimentos
        consumo_do_dia = []
        
        for i, alimento in enumerate(todos_alimentos):
            print(f"{i + 1}. {alimento.nome} - {alimento.porcao}g - {alimento.calorias:.2f} kcal")
        
        data = input("Digite a data do consumo (YYYY-MM-DD): ")
        
        #verificar se a data é valida
        try:
            from datetime import datetime
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            print("Data inválida. Por favor, digite no formato YYYY-MM-DD.")
            return

        escolha = input("Digite o número do alimento consumido (ou 0 para finalizar): ")
        while escolha != '0':
            try:
                index = int(escolha) - 1
                if 0 <= index < len(todos_alimentos):
                    alimento = todos_alimentos[index]
                    quantia = float(input(f"Quantia consumida de {alimento.nome} (g): "))
                    consumo_do_dia.append([alimento.nome, quantia, alimento.calorias_consumidas(quantia)])
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
            
            escolha = input("Digite o número do alimento consumido (ou 0 para finalizar): ")
        
        print("Consumo do dia registrado:")
        for item in consumo_do_dia:
            print(f"{item[0]} - {item[1]}g - {item[2]:.2f} kcal")
            
        self.app.registrar_consumo_diario(data, consumo_do_dia)
        
    
    
    def cadastrar_alimento(self):
        try:
            alimento = {
                "nome": input("Nome do alimento: "),
                "porcao": float(input("Porção (g): ")),
                "proteina": float(input("Proteína (g): ")),
                "carboidrato": float(input("Carboidrato (g): ")),
                "gordura": float(input("Gordura (g): ")),
            }
            self.app.alterar_alimentos_usuario(alimento, "adicionar")
            
        except ValueError as e:
            print(f"Entrada inválida: {e}")
            self.cadastrar_alimento()


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
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado para alterar alimentos.")
        if acao == "adicionar":
            alimento['acao'] = "adicionar"
            self.usuario_logado.alimentos = alimento
        elif acao == "atualizar":
            alimento['acao'] = "atualizar"
            self.usuario_logado.alimentos = alimento
        elif acao == "remover":
            alimento['acao'] = "remover"
            self.usuario_logado.alimentos = alimento
        else:
            raise ValueError("A ação deve ser 'adicionar', 'atualizar' ou 'remover'.")
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