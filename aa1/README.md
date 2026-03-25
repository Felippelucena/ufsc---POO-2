# Sistema de Controle de Dieta e Nutrição

## 📋 Descrição

Sistema orientado a objetos para controle de dieta que permite que usuários registrem alimentos consumidos, calculem calorias diárias e acompanhem seu progresso nutricional. O projeto foi desenvolvido como atividade avaliativa para disciplina de Programação Orientada a Objetos (POO).

## 🎯 Objetivo

Desenvolver um software com aplicação prática dos princípios de POO (classes, encapsulamento, herança, polimorfismo) para gerenciar registros nutricionais de usuários, incluindo cálculo de metabolismo basal, gasto energético total e acompanhamento de objetivos dietéticos.

## 📋 Requisitos do Sistema

O sistema implementa as seguintes funcionalidades:

### Usuários
- ✅ Cadastro com dados pessoais (nome, sexo, idade, peso, altura)
- ✅ Definição de objetivo de saúde (perda de peso, manutenção, ganho de massa)
- ✅ Nível de atividade física (sedentário, leve, moderado, intenso, muito intenso)

### Alimentos
- ✅ Cadastro com nome, quantidade em gramas e macronutrientes
- ✅ Cálculo automático de calorias por porção
- ✅ Banco global de alimentos disponíveis
- ✅ Alimentos personalizados por usuário

### Acompanhamento Nutricional
- ✅ Registro de consumo diário por data
- ✅ Cálculo de **TMB** (Taxa Metabólica Basal) - Fórmula Harris-Benedict
- ✅ Cálculo de **GET** (Gasto Energético Total) com ajuste por nível de atividade
- ✅ Recomendação de calorias diárias conforme objetivo (+500 kcal para ganho, -500 para perda)

### Interface
- ✅ Interface de terminal interativa com menus
- ✅ Estrutura de interface gráfica com Tkinter (pronta para expansão)

### Persistência
- ✅ Armazenamento em arquivos JSON
- ✅ Carregamento e salvamento de dados de usuários e alimentos

## 🏗️ Estrutura do Projeto

```

```

## 🔧 Tecnologias Utilizadas

- **Linguagem**: Python 3.x
- **Interface**: 
  - Terminal (ativa)
  - Tkinter para GUI (estrutura implementada)
- **Persistência**: JSON
- **Princípios**: POO com encapsulamento, validação e separação de responsabilidades

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Tkinter (geralmente incluído com Python)

### Passos de Instalação

1. **Clone ou baixe o projeto**
```bash
cd aa1
```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

## 🚀 Como Usar

### Executar a Aplicação

```bash
python main.py
```

A aplicação iniciará com a interface de terminal. Menu principal oferecerá opções como:

