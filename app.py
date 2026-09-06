import os
import sys

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_ATUAL not in sys.path:
    sys.path.insert(0, DIRETORIO_ATUAL)

from flask import Flask, render_template, request, redirect, url_for
from database.connection import criar_tabelas
from database.produtos import cadastrar_produto, listar_produtos

app = Flask(__name__)

# Garante a criação das tabelas no SQLite
criar_tabelas()

@app.route("/")
@app.route("/produtos")
def pagina_produtos():
    produtos = listar_produtos()
    return render_template("produtos.html", produtos=produtos)

@app.route("/produtos/cadastrar", methods=["POST"])
def rota_cadastrar_produto():
    nome = request.form.get("nome", "").strip()
    categoria = request.form.get("categoria", "").strip()
    preco_texto = request.form.get("preco", "").strip().replace(",", ".")
    qtd_texto = request.form.get("quantidade", "").strip()

    try:
        preco = float(preco_texto)
        quantidade = int(qtd_texto)
        cadastrar_produto(nome, categoria, preco, quantidade)
    except ValueError:
        pass

    return redirect("/produtos")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)