import os
import sys

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_ATUAL not in sys.path:
    sys.path.insert(0, DIRETORIO_ATUAL)

from database.connection import criar_tabelas
from database.produtos import listar_produtos
from database.vendas import registrar_venda, relatorio_vendas

# Garante que as tabelas existem no banco
criar_tabelas()

print("--- TESTANDO MÓDULO DE VENDAS ---")

# 1. Venda válida: 3 unidades do Produto ID 1 (Teclado Mecanico)
registrar_venda(1, 3)

# 2. Venda inválida: tentando vender mais do que o estoque disponível (deve dar erro)
registrar_venda(2, 50)

# 3. Lista os produtos atualizados para conferir a baixa no estoque
listar_produtos()

# 4. Exibe o relatório com o faturamento gerado
relatorio_vendas()