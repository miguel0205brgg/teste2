from flask import Blueprint, jsonify, request
from src.services.supabase_service import supabase_client
biblioteca_bp = Blueprint("biblioteca", __name__, url_prefix="/api")

@biblioteca_bp.route("/set_token", methods=["POST"])
def set_token():
    data = request.get_json()
    access_token = data.get("access_token")
    # refresh_token = data.get("refresh_token") # Não é mais usado aqui

    if not access_token:
        return jsonify({"error": "Token de acesso não recebido."}), 400

    try:
        user_data = supabase_client.get_user_email_from_token(access_token)
        if not user_data or "email" not in user_data:
            return jsonify({"error": "Não foi possível obter informações do usuário (email)."}), 400

        email = user_data["email"]
        nome = user_data.get("name", "Usuário Google")

        # Chama o novo método de sincronização centralizado no serviço
        sync_result = supabase_client.sync_social_user(email, nome)

        if not sync_result["success"]:
            return jsonify({"error": sync_result["error"]}), 500

        return jsonify({
            "message": "Login com Google realizado com sucesso!",
            "redirect_url": "/dashboard_usuario.html"
            "usuario_id": sync_result["usuario_id"],
            "email": sync_result["email"]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Erro interno ao processar token: {str(e)}"}), 500
