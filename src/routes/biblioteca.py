from flask import Blueprint, jsonify, request, session, redirect
from src.services.supabase_service import SupabaseService

biblioteca_bp = Blueprint('biblioteca', __name__)
supabase_service = SupabaseService()

@biblioteca_bp.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    """Endpoint para cadastro de novos usuários"""
    try:
        data = request.json
        
        # Validar dados obrigatórios
        required_fields = ['nome', 'email', 'senha', 'telefone', 'cep', 'numero']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'field': field,
                    'message': f'O campo "{field}" é obrigatório e não pode estar vazio.'
                }), 400
        
        # Validar comprimento dos campos de endereço
        cep = data.get('cep')
        numero = data.get('numero')
        complemento = data.get('complemento')  # Complemento é opcional

        if len(cep) != 9:
            return jsonify({
                'success': False,
                'field': 'cep',
                'message': 'O campo "cep" deve ter 9 caracteres (ex: 12345-678).'
            }), 400
        
        if len(numero) > 10:
            return jsonify({
                'success': False,
                'field': 'numero',
                'message': 'O campo "numero" deve ter no máximo 10 caracteres.'
            }), 400

        if complemento and len(complemento) > 30:
            return jsonify({
                'success': False,
                'field': 'complemento',
                'message': 'O campo "complemento" deve ter no máximo 30 caracteres.'
            }), 400

        # Concatenar endereço para passar para o serviço Supabase
        endereco_completo = f"CEP: {cep}, Número: {numero}"
        if complemento:
            endereco_completo += f", Complemento: {complemento}"

        # Cadastrar usuário
        result = supabase_service.cadastrar_usuario_completo(
            nome=data["nome"],
            email=data["email"],
            senha=data["senha"],
            endereco=endereco_completo,
            telefone=data.get("telefone")
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro interno do servidor'
        }), 500

@biblioteca_bp.route('/login', methods=['POST'])
def login_usuario():
    """Endpoint para login de usuários"""
    try:
        data = request.json
        
        # Validar dados obrigatórios
        if not data.get('email'):
            return jsonify({
                'success': False,
                'field': 'email',
                'message': 'O campo "email" é obrigatório e não pode estar vazio.'
            }), 400
        if not data.get('senha'):
            return jsonify({
                'success': False,
                'field': 'senha',
                'message': 'O campo "senha" é obrigatório e não pode estar vazio.'
            }), 400       
        # Autenticar usuário
        result = supabase_service.autenticar_usuario(
            email=data['email'],
            senha=data['senha']
        )
        
        if result['success']:
            # Salvar dados do usuário na sessão
            session['usuario_id'] = result['data']['id']
            session['usuario_role'] = result['data']['role']
            session['usuario_nome'] = result['data']['nome']
            
            redirect_url = ''
            if session["usuario_role"] == "dev":
                redirect_url = "/dashboard-dev"  # Exemplo de página para desenvolvedores
            else:
                redirect_url = "/dashboard-usuario"  # Exemplo de página para usuários comuns
            
            result["redirect_url"] = redirect_url
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro interno do servidor'
        }), 500

@biblioteca_bp.route('/logout', methods=['POST'])
def logout_usuario():
    """Endpoint para logout de usuários"""
    try:
        session.clear()
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro interno do servidor'
        }), 500

@biblioteca_bp.route('/perfil', methods=['GET'])
def obter_perfil():
    """Endpoint para obter dados do perfil do usuário logado"""
    try:
        if 'usuario_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Usuário não autenticado'
            }), 401
        
        # Buscar dados do usuário
        result = supabase_service.buscar_usuario_por_id(session['usuario_id'])
        
        if result['success']:
            redirect_url = ''
            if session["usuario_role"] == "dev":
                redirect_url = "/dashboard-dev"
            else:
                redirect_url = "/dashboard-usuario"
            
            result["redirect_url"] = redirect_url
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro interno do servidor'
        }), 500

@biblioteca_bp.route('/status', methods=['GET'])
def status_sistema():
    """Endpoint para verificar o status do sistema"""
    try:
        return jsonify({
            'success': True,
            'message': 'Sistema de Biblioteca Online funcionando',
            'version': '1.0.0',
            'authenticated': 'usuario_id' in session,
            'user_role': session.get('usuario_role', None)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro interno do servidor'
        }), 500

@biblioteca_bp.route("/solicitar_reset_senha", methods=["POST"])
def solicitar_reset_senha():
    """Endpoint para solicitar o reset de senha"""
    try:
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"success": False, "message": "E-mail é obrigatório."}), 400

        result = supabase_service.gerar_token_reset_senha(email)
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "Token de reset de senha gerado. Verifique seu e-mail.",
                "token": result["token"]
            }), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Erro interno do servidor."}), 500

@biblioteca_bp.route("/resetar_senha", methods=["POST"])
def resetar_senha():
    """Endpoint para resetar a senha usando um token"""
    try:
        data = request.json
        token = data.get("token")
        nova_senha = data.get("nova_senha")

        if not token or not nova_senha:
            return jsonify({"success": False, "message": "Token e nova senha são obrigatórios."}), 400

        result = supabase_service.resetar_senha(token, nova_senha)
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Erro interno do servidor."}), 500

@biblioteca_bp.route("/login/google")
def login_google():
    """Redireciona para a página de autenticação do Google."""
    result = supabase_service.autenticar_com_oauth(provider="google")
    if result['success']:
        return redirect(result['redirect_url'])
    else:
        return jsonify(result), 500

@biblioteca_bp.route("/auth/callback")
def auth_callback():
    """Lida com o callback do provedor OAuth."""
    # Esta rota é um placeholder para o frontend lidar com a extração dos tokens.
    return render_template("callback.html")

@biblioteca_bp.route("/set_token", methods=["POST"])
def set_token():
    """Recebe os tokens OAuth do frontend e estabelece a sessão do usuário."""
    try:
        data = request.json
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")

        if not access_token or not refresh_token:
            return jsonify({"success": False, "message": "Tokens de autenticação não recebidos."}), 400

        # Tenta obter informações do usuário do Supabase usando o access_token
        user_response = supabase_service.supabase.auth.get_user(access_token)

        if user_response.user:
            user_email = user_response.user.email
            user_name = user_response.user.user_metadata.get("full_name", user_response.user.email)
            supabase_auth_id = user_response.user.id

            # Usa o método do serviço para obter ou criar o usuário na nossa tabela local
            user_processing_result = supabase_service.get_or_create_oauth_user(user_email, user_name, supabase_auth_id)

            if user_processing_result["success"]:
                usuario_id = user_processing_result["data"]["id"]
                # Salva os dados do usuário na sessão do Flask
                session["usuario_id"] = usuario_id
                session["usuario_role"] = "usuario"
                session["usuario_nome"] = user_name
                session["access_token"] = access_token
                session["refresh_token"] = refresh_token

                # Retorna a URL de redirecionamento para o frontend
                return jsonify({"success": True, "redirect_url": "/dashboard-usuario"}), 200
            else:
                return jsonify(user_processing_result), 400
        else:
            return jsonify({"success": False, "message": "Não foi possível obter informações do usuário do Supabase com o token fornecido."}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "message": "Erro interno do servidor ao processar tokens OAuth."}), 500

