from flask import Flask, request, jsonify
from meuscript import saudacao

app = Flask(__name__)

@app.route("/")
def home():
    return "API funcionando!"

@app.route("/saudar", methods=["POST"])
def saudar():
    data = request.json
    nome = data.get("nome", "usuário")
    resposta = saudacao(nome)
    return jsonify({"mensagem": resposta})
