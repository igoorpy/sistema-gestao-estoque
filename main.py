import os
import sys

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_ATUAL not in sys.path:
    sys.path.insert(0, DIRETORIO_ATUAL)

from database.connection import criar_tabelas
from database.produtos import (
    cadastrar_produto,
    listar_produtos,
    atualizar_produto,
    deletar_produto
)
from database.vendas import registrar_venda, relatorio_vendas

def exibir_menu():
    print("\n=============================================")
    print("      SISTEMA DE GESTÃO DE ESTOQUE E VENDAS  ")
    print("=============================================")
    print("1. Cadastrar Novo Produto")
    print("2. Listar Produtos em Estoque")
    print("3. Editar Produto")
    print("4. Deletar Produto")
    print("5. Registrar Nova Venda")
    print("6. Exibir Relatório de Vendas")
    print("0. Sair")
    print("=============================================")

def main():
    criar_tabelas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- CADASTRO DE PRODUTO ---")
            nome = input("Nome do produto: ").strip()
            categoria = input("Categoria: ").strip()
            
            preco_texto = input("Preço (R$): ").strip().replace(",", ".")
            qtd_texto = input("Quantidade inicial em estoque: ").strip()

            try:
                preco_convertido = float(preco_texto)
                qtd_convertida = int(qtd_texto)
                cadastrar_produto(nome, categoria, preco_convertido, qtd_convertida)
            except ValueError:
                print("Erro: Digite valores numéricos válidos para preço e quantidade.")

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            print("\n--- EDITAR PRODUTO ---")
            id_texto = input("ID do produto a ser editado: ").strip()
            nome = input("Novo nome: ").strip()
            categoria = input("Nova categoria: ").strip()
            preco_texto = input("Novo preço (R$): ").strip().replace(",", ".")
            qtd_texto = input("Nova quantidade em estoque: ").strip()

            try:
                id_convertido = int(id_texto)
                preco_convertido = float(preco_texto)
                qtd_convertida = int(qtd_texto)
                atualizar_produto(id_convertido, nome, categoria, preco_convertido, qtd_convertida)
            except ValueError:
                print("Erro: Entrada de dados inválida. Certifique-se de digitar números.")

        elif opcao == "4":
            print("\n--- DELETAR PRODUTO ---")
            id_texto = input("ID do produto a ser deletado: ").strip()

            try:
                id_convertido = int(id_texto)
                confirmacao = input(f"Tem certeza que deseja deletar o produto ID {id_convertido}? (S/N): ").strip().upper()
                if confirmacao == "S":
                    deletar_produto(id_convertido)
                else:
                    print("Operação cancelada.")
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == "5":
            print("\n--- REGISTRAR VENDA ---")
            id_texto = input("ID do produto a ser vendido: ").strip()
            qtd_texto = input("Quantidade vendida: ").strip()

            try:
                id_convertido = int(id_texto)
                qtd_convertida = int(qtd_texto)
                registrar_venda(id_convertido, qtd_convertida)
            except ValueError:
                print("Erro: Digite apenas números inteiros para o ID e a Quantidade.")

        elif opcao == "6":
            relatorio_vendas()

        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()