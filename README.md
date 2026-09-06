# Sistema de Gestão de Estoque e Vendas

Sistema de gerenciamento de estoque, cadastro de produtos e controle de vendas desenvolvido em Python com interface Web em HTML5/CSS3 e persistência de dados em banco relacional SQLite.

O objetivo deste projeto é consolidar conceitos de desenvolvimento de software, arquitetura modular, manipulação de bancos de dados relacionais, desenvolvimento web backend e controle de versão.

## Estrutura do Projeto

```text
sistema-gestao-estoque/
│
├── database/
│   ├── __init__.py         # Pacote Python
│   ├── connection.py       # Conexão e criação das tabelas SQLite
│   ├── produtos.py         # Módulo de cadastro, listagem, edição e remoção
│   └── vendas.py           # Módulo de vendas e relatórios
│
├── static/
│   └── style.css           # Estilização visual em CSS
│
├── templates/
│   └── produtos.html       # Interface Web com formulário e tabela de estoque
│
├── .gitignore              # Arquivos ignorados pelo Git (.venv, .db, cache)
├── app.py                  # Servidor Web Flask (Backend)
├── main.py                 # Interface legada via CLI (Terminal)
└── README.md               # Documentação técnica do projeto