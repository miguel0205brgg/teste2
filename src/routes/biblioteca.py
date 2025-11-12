from flask import Blueprint, request, jsonify, session
from src.services.supabase_service import supabase_client

biblioteca_bp = Blueprint("biblioteca", __name__, url_prefix="/api")

@biblioteca_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"success": False, "message": "Email e senha são obrigatórios."}), 400

    auth_result = supabase_client.autenticar_usuario(email, senha)
    if auth_result["success"]:
        session["usuario_email"] = email  # salva o email na sessão
        return jsonify({"success": True, "redirect_url": "/dashboard_usuario"})
    else:
        return jsonify({"success": False, "message": auth_result["message"]}), 401

@biblioteca_bp.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    cep = data.get("cep")
    rua = data.get("rua")
    numero = data.get("numero")
    complemento = data.get("complemento")
    telefone = data.get("telefone")

    if not all([nome, email, senha, cep, rua, numero, telefone]):
        return jsonify({"success": False, "message": "Todos os campos obrigatórios devem ser preenchidos."}), 400

    try:
        res = supabase_client.cadastrar_usuario_completo(
            nome, email, senha, cep, rua, numero, complemento, telefone
        )
        if res["success"]:
            return jsonify({"success": True, "redirect_url": "/login"})
        else:
            return jsonify({"success": False, "message": res.get("error", "Erro ao cadastrar usuário")}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500
