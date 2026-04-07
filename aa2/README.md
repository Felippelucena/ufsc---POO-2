# Sistema de Controle Financeiro Residencial

Atividade Avaliativa 2 — Programação Orientada a Objetos (UFSC)

## Objetivo

Sistema de controle financeiro orientado a objetos em Python que permite a uma residência gerenciar suas despesas mensais em categorias específicas e exportar relatórios em formato PDF.

## Funcionalidades

1. **Cadastro de Despesas** — em 8 categorias: Educação, Energia, Água, Internet, Alimentação, Transporte, Residência, Entretenimento
2. **Visualização de Gastos** — relatórios mensais com despesas categorizadas
3. **Análise de Dados** — comparação de gastos entre meses, identificação de aumentos significativos
4. **Notificações** — alertas quando gastos ultrapassam limites pré-definidos (com limiares por tipo de categoria)
5. **Exportação PDF** — relatório de despesas em formato PDF

## Como Executar

```bash
cd aa2
python main.py
```

Para exportação PDF, instale a dependência:
```bash
pip install fpdf2
```

## Arquitetura

```
aa2/
├── main.py                     # Ponto de entrada
├── db/                         # Persistência JSON
│   ├── usuarios.json
│   └── categorias_padrao.json
└── src/
    ├── despesa.py              # Domínio: Despesa
    ├── categoria.py            # Domínio: Categoria + 3 subclasses + fábrica
    ├── controleFinanceiro.py   # Domínio: ControleFinanceiro
    ├── usuario.py              # Domínio: Usuario
    ├── app.py                  # Lógica de negócio
    ├── bancoDeDados.py         # Persistência
    └── uiTerminal.py           # Interface terminal
```

## Conceitos OOP Demonstrados

- **Encapsulamento**: atributos privados com `@property` e validação
- **Herança**: `CategoriaEssencial`, `CategoriaVariavel`, `CategoriaDiscricionaria` estendem `Categoria`
- **Polimorfismo**: cada subclasse sobrescreve a propriedade `alerta` com limiar diferente
- **Função Fábrica**: `criar_categoria()` retorna a subclasse correta
- **Arquitetura em Camadas**: UI → App → Domínio → Persistência
