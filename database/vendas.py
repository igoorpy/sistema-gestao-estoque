import sqlite3
from database.connection import conectar

def registrar_venda(produto_id, quantidade_vendida):
    """Registra uma venda e realiza a baixa automatica no estoque do produto."""
    if quantidade_vendida <= 0:
        print("Erro: A quantidade vendida deve ser maior que zero.")
        return False

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Busca o produto e verifica o estoque atual
        cursor.execute("SELECT nome, preco, quantidade FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print(f"Erro: Produto com ID {produto_id} não encontrado.")
            conexao.close()
            return False

        nome_produto, preco_unitario, estoque_atual = produto

        # Validação de estoque
        if estoque_atual < quantidade_vendida:
            print(f"Erro: Estoque insuficiente para '{nome_produto}'. Disponível: {estoque_atual}.")
            conexao.close()
            return False

        total_venda = preco_unitario * quantidade_vendida
        novo_estoque = estoque_atual - quantidade_vendida

        # Inicia a transação: atualiza o estoque e insere o registro da venda
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, produto_id))
        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade, preco_unitario, total_venda)
            VALUES (?, ?, ?, ?)
        """, (produto_id, quantidade_vendida, preco_unitario, total_venda))

        conexao.commit()
        conexao.close()
        print(f"Venda realizada com sucesso! Total: R$ {total_venda:.2f}")
        return True

    except sqlite3.Error as e:
        print(f"Erro ao registrar venda: {e}")
        return False


def relatorio_vendas():
    """Exibe o relatório simples de vendas no terminal (CLI)."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = """
            SELECT 
                vendas.id,
                produtos.nome,
                vendas.quantidade,
                vendas.preco_unitario,
                vendas.total_venda,
                vendas.data_venda
            FROM vendas
            INNER JOIN produtos ON vendas.produto_id = produtos.id
            ORDER BY vendas.id DESC
        """
        cursor.execute(query)
        vendas = cursor.fetchall()
        conexao.close()

        if not vendas:
            print("\nNenhuma venda registrada.")
            return

        print("\n--- RELATÓRIO DE VENDAS ---")
        faturamento_total = 0
        for v in vendas:
            faturamento_total += v[4]
            print(f"ID Venda: {v[0]} | Produto: {v[1]} | Qtd: {v[2]} | Total: R$ {v[4]:.2f} | Data: {v[5]}")

        print(f"\nFaturamento Total Acumulado: R$ {faturamento_total:.2f}")

    except sqlite3.Error as e:
        print(f"Erro ao gerar relatório: {e}")


def buscar_vendas_web():
    """Retorna o histórico de vendas e o faturamento total acumulado para a interface Web."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = """
            SELECT 
                vendas.id,
                produtos.nome,
                vendas.quantidade,
                vendas.preco_unitario,
                vendas.total_venda,
                vendas.data_venda
            FROM vendas
            INNER JOIN produtos ON vendas.produto_id = produtos.id
            ORDER BY vendas.id DESC
        """
        cursor.execute(query)
        vendas = cursor.fetchall()

        faturamento_total = sum(v[4] for v in vendas) if vendas else 0.0

        conexao.close()
        return vendas, faturamento_total
    except sqlite3.Error as e:
        print(f"Erro ao buscar vendas para a web: {e}")
        return [], 0.0