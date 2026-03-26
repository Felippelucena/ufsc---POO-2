# Sistema de Controle de Dieta e Nutrição

## Descrição

Sistema orientado a objetos para controle de dieta desenvolvido como atividade avaliativa de POO (UFSC). Permite cadastro de usuários, registro de alimentos, cálculo de TMB/GET e acompanhamento nutricional.

## Como Executar

```bash
python main.py
```

Sem dependências externas — utiliza apenas Python 3.8+ (json, tkinter).

## Funcionalidades

- **Cadastro de usuários** com dados pessoais, objetivo e nível de atividade
- **Cadastro de alimentos** (globais e por usuário) com cálculo automático de calorias (4/4/9 kcal)
- **Registro de consumo diário** por data com resumo comparativo à meta (GET)
- **Cálculo de TMB** (Harris-Benedict) e **GET** (com ajuste por atividade e objetivo)
- **Histórico de consumo** com comparação diária à meta calórica
- **Relatório nutricional** com média, dias acima/abaixo da meta e detalhamento por dia
- **Atualização de perfil** com suporte a troca de objetivo (recria subclasse)
- **CRUD de alimentos** do usuário (adicionar, atualizar, remover)
- **Interface gráfica completa** com Tkinter e interface de terminal alternativa

## Princípios de POO

- **Encapsulamento**: propriedades com `@property`, atributos privados com name mangling (`__`) e validação nos setters
- **Herança**: subclasses `UsuarioPerdaPeso`, `UsuarioManutencao` e `UsuarioGanhoMassa` estendem `Usuario`
- **Polimorfismo**: cada subclasse sobrescreve a propriedade `get` com o ajuste calórico específico do objetivo (-500, 0, +500 kcal)
- **Função fábrica**: `criar_usuario()` instancia a subclasse correta com base no objetivo

## Estrutura

```
aa1/
├── main.py                  # Ponto de entrada
├── src/
│   ├── ui.py                # Interface gráfica (Tkinter) -- Feito com IA com base na uiTerminal.py
│   ├── uiTerminal.py        # Interface de terminal
│   ├── app.py               # Lógica de negócio
│   ├── usuario.py           # Classe base + subclasses por objetivo
│   ├── alimento.py          # Classe Alimento
│   └── bancoDeDados.py      # Persistência JSON
└── db/
    ├── usuarios.json         # Dados dos usuários
    └── alimentos_global.json # Banco global de alimentos
```

## Fluxo de Dados

UI (dicts) → App (constrói objetos de domínio) → BancoDeDados (serializa via `.json()` para `db/*.json`)
