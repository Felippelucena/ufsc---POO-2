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

from src.uiTerminal import UiTerminal
    
if __name__ == "__main__":
    ui = UiTerminal()
    ui.iniciar()