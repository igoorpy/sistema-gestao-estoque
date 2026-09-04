import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.connection import criar_tabelas
from database.produtos import cadastrar_produto, listar_produtos

criar_tabelas()

print("--- TESTANDO CADASTRO ---")
cadastrar_produto("Teclado Mecanico", "Perifericos", 250.00, 10)
cadastrar_produto("Mouse Sem Fio", "Perifericos", 80.00, 15)

listar_produtos()