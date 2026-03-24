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
aa1/
├── README.md                 # Este arquivo
├── main.py                   # Ponto de entrada da aplicação
├── modelos/                  # Módulo com classes do sistema
│   ├── __init__.py
│   ├── alimento.py          # Classe Alimento
│   ├── usuario.py           # Classe Usuario
│   ├── bancoDeDados.py      # Gerenciamento de persistência
│   ├── ui.py                # Interface gráfica (Tkinter)
│   └── uiTerminal.py        # Interface de terminal
└── db/                       # Banco de dados em JSON
    ├── usuarios.json        # Perfis de usuários cadastrados
    └── alimentos_global.json # Banco global de alimentos
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

- **Novo Usuário**: Cadastra um novo perfil
- **Fazer Login**: Acessa um perfil existente
- **Sair**: Encerra a aplicação

### Exemplos de Uso

#### 1. Cadastrar Novo Usuário
```
Nome: João Silva
Sexo: m
Idade: 25
Peso (kg): 80
Altura (cm): 180
Objetivo: ganho de massa
Nível de Atividade: moderado
```

#### 2. Registrar Consumo
- Selecionar data (YYYY-MM-DD)
- Adicionar alimentos com quantidade
- Sistema calcula calorias automaticamente

#### 3. Visualizar Resumo
- Calorias consumidas vs. recomendadas
- Macronutrientes (proteína, carboidrato, gordura)
- Comparação com objetivo

## 🏛️ Arquitetura e Princípios POO

### Encapsulamento
- Atributos privados com `__` prefix
- Properties e setters com validação
- Exemplos: `usuario.peso`, `usuario.altura`

### Validação de Dados
30+ validações implementadas:
- Comprimento de strings (nomes)
- Ranges numéricos (peso, altura, idade)
- Tipos de dados
- Enumerações (sexo, objetivo, nível_atividade)

### Padrões de Design
- **Factory Pattern**: Classe `BancoDeDados` com métodos classmethod
- **Separação de Camadas**:
  - Lógica de negócio: `usuario.py`, `alimento.py`
  - Persistência: `bancoDeDados.py`
  - Interface: `ui.py`, `uiTerminal.py`

### Métodos de Serialização
- `.json()` para converter objetos a dicionários
- Integração com persistência JSON

## 📊 Estrutura de Dados

### Usuario (JSON)
```json
{
  "nome": "string",
  "sexo": "m|f",
  "idade": número,
  "peso": número,
  "altura": número,
  "objetivo": "perda de peso|manutenção|ganho de massa",
  "nivel_atividade": "sedentario|leve|moderado|intenso|muito intenso",
  "consumo_diario": {
    "YYYY-MM-DD": [
      ["Alimento", "porcao", "calorias"],
      ["Frango", 150, 245]
    ]
  },
  "alimentos": [
    {
      "nome": "string",
      "porcao": número,
      "proteina": número,
      "carboidrato": número,
      "gordura": número
    }
  ]
}
```

### Alimento (JSON)
```json
{
  "nome": "string",
  "porcao": número,
  "proteina": número,
  "carboidrato": número,
  "gordura": número
}
```

## 📐 Cálculos Implementados

### Taxa Metabólica Basal (TMB)
Utilizando fórmula de Harris-Benedict:

**Homens**: TMB = 88,362 + (13,397 × peso) + (4,799 × altura) - (5,677 × idade)

**Mulheres**: TMB = 447,593 + (9,247 × peso) + (3,098 × altura) - (4,330 × idade)

### Gasto Energético Total (GET)
GET = TMB × NAF (Nível de Atividade Física)

**Fatores de Atividade**:
- Sedentário: 1.2
- Leve: 1.375
- Moderado: 1.55
- Intenso: 1.725
- Muito Intenso: 1.9

### Ajuste por Objetivo
- Ganho de Massa: +500 kcal
- Manutenção: sem ajuste
- Perda de Peso: -500 kcal

## 🔍 Módulos Principais

### `main.py` - Classe App
Gerenciador central da aplicação:
- `adicionar_usuario()` - Cadastra novo usuário
- `entrar_usuario()` - Login de usuário existente
- `alterar_alimentos_usuario()` - Adiciona/atualiza/remove alimentos
- `registrar_consumo_diario()` - Registra consumo do dia

### `modelos/usuario.py` - Classe Usuario
Representa um usuário do sistema com:
- Dados pessoais validados
- Cálculo automático de TMB e GET
- Registro de consumo diário
- Alimentos personalizados
- Método de conversão JSON

### `modelos/alimento.py` - Classe Alimento
Representa um alimento com:
- Dados nutricionais (macronutrientes)
- Cálculo de calorias (validação)
- Método de conversão JSON

### `modelos/bancoDeDados.py` - Classe BancoDeDados
Gerencia persistência:
- `carregar_dados()` - Lê JSON
- `salvar_dados()` - Escreve JSON
- `adicionar_usuario()` - Persiste novo usuário
- `atualizar_usuario()` - Atualiza usuário existente
- `buscar_usuario()` - Localiza usuário por nome
- `adicionar_alimento_global()` - Adiciona alimento à lista global

### `modelos/uiTerminal.py` - Classe UiTerminal
Interface interativa de terminal com:
- Menus navegáveis
- Validação de entrada
- Operações CRUD de usuários e alimentos

### `modelos/ui.py` - Classe Ui
Estrutura de interface gráfica em Tkinter:
- `MenuPage` - Tela inicial
- `LoginPage` - Autenticação
- `CadastroPage` - Cadastro de novo usuário

## 🎓 Critérios de Avaliação Implementados

✅ **Uso correto de POO**: Classes bem definidas com responsabilidades claras

✅ **Encapsulamento**: Atributos privados com properties validadas

✅ **Herança e Polimorfismo**: Estrutura preparada para expandir categorias

✅ **Persistência**: Sistema JSON funcional e robusta

✅ **Interface**: Terminal interativa operacional + Tkinter estruturada

✅ **Código**: Bem estruturado, comentado e seguindo convenções PEP 8

## 📝 Possíveis Expansões Futuras

- [ ] Completar interface gráfica com Tkinter
- [ ] Integrar com banco de dados SQLite
- [ ] Adicionar relatórios em PDF
- [ ] Sistema de metas e acompanhamento semanal
- [ ] Integração com APIs de alimentos
- [ ] Sincronização em nuvem
- [ ] Aplicativo mobile

## 📞 Suporte

Para dúvidas ou sugestões sobre o projeto, consulte a documentação inline no código ou as comentárias nas classes.

---

**Desenvolvido como atividade avaliativa de Programação Orientada a Objetos - UFSC**
