from flask import Blueprint, jsonify, request, render_template
from src.services.supabase_service import supabase_client
from src.routes.auth import get_user_id_from_request

pagamento_bp = Blueprint("pagamento", __name__)

# Rota para servir a página HTML
@pagamento_bp.route("/pagamento-divida", methods=["GET"])
def pagamento_divida_page():
    return render_template("pagamento_divida.html")

# Rota de API para buscar o valor da dívida do usuário
@pagamento_bp.route("/api/divida", methods=["GET"])
def get_divida():
    # Simulação: Em um sistema real, você buscaria o ID do usuário
    # e consultaria o banco de dados para calcular a dívida.
    # Por enquanto, vamos simular um valor fixo.
    
    # user_id = get_user_id_from_request(request) # Implementar esta função
    # if not user_id:
    #     return jsonify({"error": "Não autorizado"}), 401

    # Simulação de busca de dívida
    divida_simulada = {
        "valor": 45.50,
        "detalhes": "Atraso na devolução do livro 'O Senhor dos Anéis'."
    }
    
    return jsonify({"success": True, "divida": divida_simulada}), 200

# Rota de API para simular o pagamento
@pagamento_bp.route("/api/pagar-divida", methods=["POST"])
def pagar_divida():
    data = request.get_json()
    valor_pago = data.get("valor")
    
    # user_id = get_user_id_from_request(request) # Implementar esta função
    # if not user_id:
    #     return jsonify({"error": "Não autorizado"}), 401

    # Simulação de processamento de pagamento
    if valor_pago and valor_pago >= 45.50: # Valor simulado
        # Em um sistema real, aqui você integraria com um gateway de pagamento
        # e, em caso de sucesso, registraria o pagamento no banco de dados.
        return jsonify({"success": True, "message": "Pagamento de dívida realizado com sucesso!"}), 200
    else:
        return jsonify({"success": False, "message": "Valor de pagamento insuficiente ou inválido."}), 400
