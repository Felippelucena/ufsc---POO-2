# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

Sistema de Controle Financeiro Residencial — atividade avaliativa de POO (UFSC). Permite cadastro de usuários, registro de despesas por categoria, relatórios mensais, comparação entre meses, alertas de limite e exportação em PDF. Escrito em português brasileiro.

## Running

```bash
cd aa2
python main.py
```

Dependência externa: `fpdf2` (apenas para exportação PDF). Instalar com `pip install fpdf2`.

## Architecture

**Entry point:** `main.py` → instancia `UiTerminal` e chama `iniciar()`.

**Layers:**
- **UI layer** (`src/uiTerminal.py`): Interface terminal com menus recursivos. Instancia `App`.
- **App layer** (`src/app.py`): Coordenador de lógica. Gerencia `usuario_logado`, delega persistência para `BancoDeDados`. Recebe dicts da UI e constrói objetos de domínio.
- **Domain models** (`src/despesa.py`, `src/categoria.py`, `src/controleFinanceiro.py`, `src/usuario.py`): Classes com validação via `@property`. `Categoria` tem 3 subclasses (herança + polimorfismo) que sobrescrevem `alerta`. `Despesa` calcula `mes_ano`. `ControleFinanceiro` agrega categorias e gera relatórios.
- **Persistence** (`src/bancoDeDados.py`): `BancoDeDados` com `@classmethod`. Lê/escreve JSON em `db/`.

**Data flow:** UI coleta input como dicts → `App` constrói objetos de domínio → `BancoDeDados` serializa via `.json()` para `db/*.json`.

**Data files** (`db/`):
- `usuarios.json` — lista de usuários (inclui controle_financeiro com categorias e despesas)
- `categorias_padrao.json` — limites padrão por categoria

## Conventions

- Todo código, nomes de variáveis, strings de UI e comentários em **português**.
- Properties usam `@property` com atributos privados `__` (name mangling) e validação nos setters.
- `Categoria.despesas` setter aceita list (replace) ou dict com chave `acao` (`adicionar`, `remover`).
- Herança: `CategoriaEssencial` (alerta 90%), `CategoriaVariavel` (alerta 100%), `CategoriaDiscricionaria` (alerta 80%).
- Função fábrica `criar_categoria()` seleciona subclasse correta pelo nome.
