import psycopg2
from database.connection import conectar

def registrar_venda(produto_id, quantidade_vendida, forma_pagamento="Dinheiro"):
    """Registra uma venda com forma de pagamento e realiza a baixa automatica no estoque."""
    if quantidade_vendida <= 0:
        return False

    try:
        conexao = conectar()
        if not conexao:
            return False
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, preco, quantidade FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            conexao.close()
            return False

        nome_produto, preco_unitario, estoque_atual = produto

        if estoque_atual < quantidade_vendida:
            conexao.close()
            return False

        total_venda = float(preco_unitario) * quantidade_vendida
        novo_estoque = estoque_atual - quantidade_vendida

        # Baixa no estoque e insercao da venda
        cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (novo_estoque, produto_id))
        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade, preco_unitario, total_venda, forma_pagamento)
            VALUES (%s, %s, %s, %s, %s)
        """, (produto_id, quantidade_vendida, preco_unitario, total_venda, forma_pagamento))

        conexao.commit()
        cursor.close()
        conexao.close()
        return True

    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
        return False

def buscar_vendas_web():
    """Retorna o histórico de vendas incluindo a forma de pagamento e o faturamento total."""
    try:
        conexao = conectar()
        if not conexao:
            return [], 0.0
        cursor = conexao.cursor()

        query = """
            SELECT 
                vendas.id,
                produtos.nome,
                vendas.quantidade,
                vendas.preco_unitario,
                vendas.total_venda,
                vendas.forma_pagamento,
                TO_CHAR(vendas.data_venda, 'DD/MM/YYYY HH24:MI')
            FROM vendas
            INNER JOIN produtos ON vendas.produto_id = produtos.id
            ORDER BY vendas.id DESC
        """
        cursor.execute(query)
        vendas = cursor.fetchall()

        faturamento_total = sum(float(v[4]) for v in vendas) if vendas else 0.0

        cursor.close()
        conexao.close()
        return vendas, faturamento_total
    except Exception as e:
        print(f"Erro ao buscar vendas para web: {e}")
        return [], 0.0