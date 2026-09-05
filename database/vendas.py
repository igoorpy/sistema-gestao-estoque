import sqlite3
from database.connection import conectar

def registrar_venda(produto_id, quantidade):
    """
    Registra uma venda e atualiza o estoque do produto.
    Valida se o produto existe e se ha estoque suficiente.
    """
    if quantidade <= 0:
        print("Erro: A quantidade vendida deve ser maior que zero.")
        return False

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        #Verifica se o produto existe e qual o estoque atual
        cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print(f"Erro: Produto com ID {produto_id} não encontrado.")
            conexao.close()
            return False

        nome_produto, estoque_atual = produto

        if estoque_atual < quantidade:
            print(f"Erro: Estoque insuficiente para '{nome_produto}'. Disponível: {estoque_atual}, Solicitado: {quantidade}.")
            conexao.close()
            return False

        #Registra a venda na tabela 'vendas'
        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade)
            VALUES (?, ?)
        """, (produto_id, quantidade))

        # Atualiza (dá baixa) na quantidade do produto
        novo_estoque = estoque_atual - quantidade
        cursor.execute("""
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
        """, (novo_estoque, produto_id))

        # Confirma as duas alterações (Transação)
        conexao.commit()
        conexao.close()

        print(f"Venda realizada com sucesso! {quantidade}x '{nome_produto}' vendido(s). Novo estoque: {novo_estoque}")
        return True

    except sqlite3.Error as e:
        print(f"Erro ao registrar venda no banco: {e}")
        return False


def relatorio_vendas():
    """Exibe o relatorio geral de vendas com JOIN na tabela de produtos."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Consulta com INNER JOIN para pegar o nome do produto vendido
        cursor.execute("""
            SELECT v.id, p.nome, v.quantidade, p.preco, (v.quantidade * p.preco) AS total, v.data_venda
            FROM vendas v
            INNER JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
        """)
        vendas = cursor.fetchall()
        conexao.close()

        if not vendas:
            print("\nNenhuma venda registrada até o momento.")
            return []

        print("\n--- RELATÓRIO DE VENDAS ---")
        faturamento_total = 0
        for venda in vendas:
            v_id, p_nome, qtd, preco_unit, total, data = venda
            faturamento_total += total
            print(f"Venda #{v_id} | Produto: {p_nome} | Qtd: {qtd} | Total: R$ {total:.2f} | Data: {data}")

        print(f"-----------------------------------")
        print(f"FATURAMENTO TOTAL: R$ {faturamento_total:.2f}")

        return vendas

    except sqlite3.Error as e:
        print(f"Erro ao gerar relatório de vendas: {e}")
        return []