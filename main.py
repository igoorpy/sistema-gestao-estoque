import os
import sys

# Garante que o diretório atual do projeto esteja no caminho do Python
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_ATUAL not in sys.path:
    sys.path.insert(0, DIRETORIO_ATUAL)

from database.connection import criar_tabelas
from database.produtos import cadastrar_produto, listar_produtos
from database.vendas import registrar_venda, relatorio_vendas

def exibir_menu():
    print("\n=============================================")
    print("      SISTEMA DE GESTÃO DE ESTOQUE E VENDAS  ")
    print("=============================================")
    print("1. Cadastrar Novo Produto")
    print("2. Listar Produtos em Estoque")
    print("3. Registrar Nova Venda")
    print("4. Exibir Relatório de Vendas")
    print("0. Sair")
    print("=============================================")

def main():
    # Inicializa as tabelas no SQLite
    criar_tabelas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- CADASTRO DE PRODUTO ---")
            nome = input("Nome do produto: ").strip()
            categoria = input("Categoria: ").strip()
            
            try:
                preco = float(input("Preço (R$): ").replace(",", "."))
                quantidade = int(input("Quantidade inicial em estoque: "))
                cadastrar_produto(nome, categoria, preco, quantidade)
            except ValueError:
                print("Erro: Digite valores numéricos válidos para preço e quantidade.")

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            print("\n--- REGISTRAR VENDA ---")
            try:
                produto_id = int(input("ID do Produto a ser vendido: "))
                quantidade = int(input("Quantidade vendida: "))
                registrar_venda(produto_id, quantidade)
            except ValueError:
                print("Erro: Digite apenas números inteiros para o ID e a Quantidade.")

        elif opcao == "4":
            relatorio_vendas()

        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()