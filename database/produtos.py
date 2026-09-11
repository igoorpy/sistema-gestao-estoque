import psycopg2
from database.connection import conectar

def cadastrar_produto(nome, categoria, preco, quantidade):
    try:
        conexao = conectar()
        if not conexao:
            return False
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (%s, %s, %s, %s)",
            (nome, categoria, preco, quantidade)
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
        return False

def listar_produtos():
    try:
        conexao = conectar()
        if not conexao:
            return []
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, categoria, preco, quantidade FROM produtos ORDER BY id ASC")
        produtos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return produtos
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []

def obter_metricas_estoque():
    try:
        conexao = conectar()
        if not conexao:
            return {"total_itens": 0, "valor_total": 0.0, "itens_criticos": 0}
        cursor = conexao.cursor()
        cursor.execute("SELECT quantidade, preco FROM produtos")
        produtos = cursor.fetchall()
        cursor.close()
        conexao.close()

        total_itens = len(produtos)
        valor_total_estoque = sum(float(p[0]) * float(p[1]) for p in produtos) if produtos else 0.0
        itens_criticos = sum(1 for p in produtos if p[0] <= 3)

        return {
            "total_itens": total_itens,
            "valor_total": valor_total_estoque,
            "itens_criticos": itens_criticos
        }
    except Exception as e:
        print(f"Erro ao calcular metricas: {e}")
        return {"total_itens": 0, "valor_total": 0.0, "itens_criticos": 0}