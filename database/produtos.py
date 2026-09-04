import sqlite3
from database.connection import conectar

def cadastrar_produto(nome, categoria, preco, quantidade):
    if preco <= 0 or quantidade < 0:
        print("Erro: O preco deve ser maior que zero e a quantidade nao pode ser negativa.")
        return False

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("""
            INSERT INTO produtos (nome, categoria, preco, quantidade)
            VALUES (?, ?, ?, ?)
        """, (nome, categoria, preco, quantidade))
        
        conexao.commit()
        conexao.close()
        print(f"Produto '{nome}' cadastrado com sucesso!")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar produto no banco: {e}")
        return False

def listar_produtos():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT id, nome, categoria, preco, quantidade FROM produtos")
        produtos = cursor.fetchall()
        conexao.close()

        if not produtos:
            print("\nNenhum produto cadastrado no momento.")
            return []

        print("\n--- LISTA DE PRODUTOS ---")
        for prod in produtos:
            print(f"ID: {prod[0]} | Nome: {prod[1]} | Categoria: {prod[2]} | Preço: R$ {prod[3]:.2f} | Estoque: {prod[4]}")
        
        return produtos
    except sqlite3.Error as e:
        print(f"Erro ao listar produtos: {e}")
        return []