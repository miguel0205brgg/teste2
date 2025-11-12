from flask import Blueprint, jsonify, request
from src.services.supabase_service import supabase_client

biblioteca_bp = Blueprint("biblioteca", __name__, url_prefix="/api")

@biblioteca_bp.route("/set_token", methods=["POST"])
def set_token():
    data = request.get_json()
    access_token = data.get("access_token")
    if not access_token:
        return jsonify({"error": "Token de acesso não recebido."}), 400
    try:
        user_data = supabase_client.get_user_email_from_token(access_token)
        if not user_data or "email" not in user_data:
            return jsonify({"error": "Não foi possível obter informações do usuário (email)."}), 400

        email = user_data["email"]
        nome = user_data.get("name", "Usuário Google")
        sync_result = supabase_client.sync_social_user(email, nome)
        if not sync_result["success"]:
            return jsonify({"error": sync_result["error"]}), 500

        return jsonify({
            "message": "Login com Google realizado com sucesso!",
            "usuario_id": sync_result["usuario_id"],
            "email": sync_result["email"],
            "redirect_url": "/dashboard_usuario"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro interno ao processar token: {str(e)}"}), 500

@biblioteca_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    if not email or not senha:
        return jsonify({"success": False, "message": "Email e senha são obrigatórios."}), 400
    auth_result = supabase_client.autenticar_usuario(email, senha)
    if auth_result["success"]:
        return jsonify({"success": True, "redirect_url": "/dashboard-usuario"})
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

    if not nome or not email or not senha or not cep or not rua or not numero or not telefone:
        return jsonify({"success": False, "message": "Todos os campos obrigatórios devem ser preenchidos."}), 400

    try:
        # 1) Criar usuário na tabela usuario
        usuario_res = supabase_client.criar_usuario(nome, email, senha)
        if not usuario_res["success"]:
            return jsonify({"success": False, "message": usuario_res["message"]}), 400
        usuario_id = usuario_res["usuario_id"]

        # 2) Criar endereço
        endereco_res = supabase_client.criar_endereco(cep, rua, numero, complemento)
        if not endereco_res["success"]:
            return jsonify({"success": False, "message": endereco_res["message"]}), 400
        endereco_id = endereco_res["endereco_id"]

        # 3) Criar leitor vinculando usuario e endereco
        leitor_res = supabase_client.criar_leitor(nome, email, telefone, usuario_id, endereco_id)
        if not leitor_res["success"]:
            return jsonify({"success": False, "message": leitor_res["message"]}), 400

        return jsonify({"success": True, "redirect_url": "/login"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500
