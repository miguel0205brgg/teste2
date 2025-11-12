from flask import Flask, request, jsonify, redirect, url_for
from supabase_service import criar_usuario_completo, autenticar_usuario

app = Flask(__name__)

@app.route("/api/cadastro", methods=["POST"])
def cadastro():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    telefone = data.get("telefone")
    cep = data.get("cep")
    logradouro = data.get("rua")
    numero = data.get("numero")
    complemento = data.get("complemento")

    usuario = criar_usuario_completo(nome, email, senha, telefone, cep, logradouro, numero, complemento)
    if usuario:
        return jsonify({"success": True, "redirect_url": "/login"})
    return jsonify({"success": False, "message": "Erro ao criar perfil de leitor. Rollback realizado."}), 400

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    usuario = autenticar_usuario(email, senha)
    if usuario:
        return jsonify({"success": True, "redirect_url": "/dashboard_usuario", "usuario": usuario})
    return jsonify({"success": False, "message": "E-mail ou senha incorretos
