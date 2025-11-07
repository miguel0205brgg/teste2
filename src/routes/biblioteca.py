from flask import Blueprint, jsonify, request, session
from src.services.supabase_service import SupabaseService

biblioteca_bp = Blueprint('biblioteca', __name__)
supabase_service = SupabaseService()

@biblioteca_bp.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    """Endpoint para cadastro de novos usuários"""
    try:
        data = request.json
        print(f"[DEBUG BIBLIOTECA] Dados recebidos para cadastro: {data}")
        
        # Validar dados obrigatórios
        required_fields = ['nome', 'email', 'senha', 'telefone', 'cep', 'rua', 'numero']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'field': field,
                    'message': f'O campo "{field}" é obrigatório e não pode estar vazio.'
                }), 400
    
    # Validar força da senha (Correção 2)
    senha = data.get('senha')
    if len(senha) < 8:
        return jsonify({
            'success': False,
            'field': 'senha',
            'message': 'A senha deve ter no mínimo 8 caracteres.'
        }), 400

    import re
    tem_maiuscula = bool(re.search(r'[A-Z]', senha))
    tem_minuscula = bool(re.search(r'[a-z]', senha))
    tem_numero = bool(re.search(r'[0-9]', senha))
    tem_especial = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', senha))

    forcas = sum([tem_maiuscula, tem_minuscula, tem_numero, tem_especial])
    if forcas < 3:
        return jsonify({
            'success': False,
            'field': 'senha',
            'message': 'A senha deve conter pelo menos 3 dos seguintes: maiúsculas, minúsculas, números, caracteres especiais.'
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

        telefone = data.get('telefone')
        if telefone and len(telefone) > 20:
            return jsonify({
                'success': False,
                'field': 'telefone',
                'message': 'O campo "telefone" deve ter no máximo 20 caracteres.'
            }), 400

        # Concatenar endereço para passar para o serviço Supabase
        rua = data.get('rua')
        endereco_completo = f"Rua: {rua}, CEP: {cep}, Número: {numero}"
        if complemento:
            endereco_completo += f", Complemento: {complemento}"

        # Cadastrar usuário
        result = supabase_service.cadastrar_usuario_completo(
            nome=data['nome'],
            email=data['email'],
            senha=data['senha'],
            cep=data['cep'],
            rua=data['rua'],
            numero=data['numero'],
            complemento=data.get('complemento'),
            telefone=data.get('telefone')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            print(f"ERRO NO CADASTRO: {result.get('error')}")
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
            session['usuario_perfil'] = result['data']['perfil']
            session['usuario_nome'] = result['data']['nome']
            
            redirect_url = ''
            redirect_url = "/biblioteca"
            
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
            if session["usuario_perfil"] == "dev":
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
            'user_role': session.get('usuario_perfil', None)
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


@biblioteca_bp.route("/perfil", methods=["GET"])
def perfil():
    """Renderiza a página de perfil do usuário logado"""
    try:
        # Verificar se o usuário está logado (verificar sessão)
        usuario_id = session.get("usuario_id")
        
        if not usuario_id:
            # Se não estiver logado, redirecionar para login
            return redirect("/login")
        
        # Buscar dados do usuário no banco de dados
        usuario = supabase_service.buscar_usuario_por_id(usuario_id)
        
        if not usuario or not usuario.get("success"):
            return redirect("/login")
        
        usuario_data = usuario.get("data")
        
        # Renderizar template com os dados do usuário
        return render_template("perfil.html", usuario=usuario_data)
    
    except Exception as e:
        print(f"[ERROR] Erro ao acessar perfil: {str(e)}")
        return redirect("/login")
