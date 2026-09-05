# Sistema de Gestão de Estoque e Vendas (Python + SQLite)

Sistema de gerenciamento de estoque, cadastro de produtos e controle de vendas desenvolvido em Python com persistência de dados em banco relacional SQLite.

O objetivo deste projeto é consolidar conceitos de desenvolvimento de software, arquitetura modular, manipulação de bancos de dados relacionais e controle de versão.

Projetado para evolução progressiva, com futuras atualizações previstas para incluir interface web (HTML/CSS), novos relatórios e expansão das regras de negócio.

## Estrutura Atual do Projeto

```text
sistema-gestao-estoque/
│
├── database/
│   ├── __init__.py         #Pacote Python
│   ├── connection.py       #Conexão e criação das tabelas sqlite
│   ├── produtos.py         #Módulo de cad e listagem de produtos
│   └── vendas.py           #Módulo de vendas e relatórios
│
├── main.py                 #Ponto de entrada da aplicação (CLI)
├── .gitignore              #Arquivos ignorados pelo Git
└── README.md               #Documentação do projeto