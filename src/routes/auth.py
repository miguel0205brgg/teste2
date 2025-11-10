from flask import Blueprint, jsonify, request
from src.services.supabase_service import supabase_client

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Usuário deslogado com sucesso."})

@auth_bp.route("/user", methods=["GET"])
def get_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token não fornecido."}), 401

    user_data = supabase_client.get_user_email_from_token(token)
    if not user_data:
        return jsonify({"error": "Token inválido ou expirado."}), 400

    return jsonify(user_data)
