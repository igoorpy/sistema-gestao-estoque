import sqlite3
from database.connection import conectar

def cadastrar_produto(nome, categoria, preco, quantidade):
    """Insere um novo produto no banco de dados."""
    if preco <= 0 or quantidade < 0:
        print("Erro: O preço deve ser maior que zero e a quantidade não pode ser negativa.")
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
    """Retorna e exibe a lista de todos os produtos cadastrados."""
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


def atualizar_produto(produto_id, novo_nome, nova_categoria, novo_preco, nova_quantidade):
    """Atualiza as informações de um produto existente pelo seu ID."""
    if novo_preco <= 0 or nova_quantidade < 0:
        print("Erro: O preço deve ser maior que zero e a quantidade não pode ser negativa.")
        return False

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM produtos WHERE id = ?", (produto_id,))
        if not cursor.fetchone():
            print(f"Erro: Produto com ID {produto_id} não encontrado.")
            conexao.close()
            return False

        cursor.execute("""
            UPDATE produtos
            SET nome = ?, categoria = ?, preco = ?, quantidade = ?
            WHERE id = ?
        """, (novo_nome, nova_categoria, novo_preco, nova_quantidade, produto_id))

        conexao.commit()
        conexao.close()
        print(f"Produto ID {produto_id} atualizado com sucesso!")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")
        return False


def deletar_produto(produto_id):
    """Remove um produto do banco de dados pelo seu ID."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print(f"Erro: Produto com ID {produto_id} não encontrado.")
            conexao.close()
            return False

        nome_produto = produto[0]

        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))

        conexao.commit()
        conexao.close()
        print(f"Produto '{nome_produto}' (ID {produto_id}) removido com sucesso!")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao deletar produto: {e}")
        return False
    
def obter_metricas_estoque():
    """Retorna estatísticas do estoque: total de produtos, valor investido e itens críticos."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT quantidade, preco FROM produtos")
        produtos = cursor.fetchall()
        conexao.close()

        total_itens = len(produtos)
        valor_total_estoque = sum(p[0] * p[1] for p in produtos) if produtos else 0.0
        itens_criticos = sum(1 for p in produtos if p[0] <= 3)

        return {
            "total_itens": total_itens,
            "valor_total": valor_total_estoque,
            "itens_criticos": itens_criticos
        }
    except sqlite3.Error as e:
        print(f"Erro ao calcular métricas: {e}")
        return {"total_itens": 0, "valor_total": 0.0, "itens_criticos": 0}