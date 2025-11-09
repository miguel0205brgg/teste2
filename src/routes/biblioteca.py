from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from src.services.supabase_service import SupabaseService

from src.config import SUPABASE_URL # Importar SUPABASE_URL

biblioteca_bp = Blueprint('biblioteca', __name__)
supabase_service = SupabaseService()

@biblioteca_bp.route('/dashboard_dev')
def dashboard_dev():
    """Simula a dashboard do desenvolvedor após o login."""
    if 'access_token' not in session:
        return redirect(url_for('biblioteca.login')) # Redirecionar para a página de login se não estiver autenticado
    
    # Aqui você faria a lógica de buscar os dados do usuário no Supabase
    # usando o token de acesso da sessão.
    
    return render_template('dashboard_dev.html')

@biblioteca_bp.route('/dashboard_usuario')
def dashboard_usuario():
    """Simula a dashboard do usuário após o login."""
    if 'access_token' not in session:
        return redirect(url_for('biblioteca.login')) # Redirecionar para a página de login se não estiver autenticado
    
    # Aqui você faria a lógica de buscar os dados do usuário no Supabase
    # usando o token de acesso da sessão.
    
    return render_template('dashboard_usuario.html')

@biblioteca_bp.route('/login')
def login():
    """Renderiza a página de login."""
    return render_template('login.html')

@biblioteca_bp.route('/login/google', methods=['GET'])
def login_google():
    """Redireciona para o fluxo de autenticação Google do Supabase."""
    # O Supabase gerencia o fluxo OAuth. O REDIRECT_URI deve ser o configurado no Google Cloud Console.
    # O Supabase usa o parâmetro 'redirect_to' para o redirecionamento final.
    # O URI de Redirecionamento configurado no Google Cloud Console é o do Supabase:
    # https://naawyjavknbewjgzcnxv.supabase.co/auth/v1/callback
    
    # O endpoint de autorização do Supabase é:
    provider = 'google'
    
    # url_for('biblioteca.callback', _external=True) irá gerar o URI de redirecionamento final
    # para a rota /callback que será implementada no Flask.
    auth_url = f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}&redirect_to={url_for('biblioteca.callback', _external=True)}"
    
    return redirect(auth_url)

@biblioteca_bp.route('/callback', methods=['GET'])
def callback():
    """
    Rota de callback para processar a resposta do Supabase Auth.
    O Supabase retorna a sessão via URL fragment (#access_token=...)
    ou via query parameters (?code=...).
    
    Como o Flask não lida diretamente com URL fragments, o template
    callback.html deve conter JavaScript para extrair o token e
    redirecionar o usuário para a dashboard ou página principal.
    
    Esta rota apenas renderiza o template.
    """
    return render_template('callback.html')

@biblioteca_bp.route('/api/set_token', methods=['POST'])
def set_token():
    """
    Endpoint para receber os tokens de sessão do Supabase via JavaScript
    e criar a sessão do usuário no Flask.
    """
    try:
        data = request.json
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        if not access_token or not refresh_token:
            return jsonify({
                'success': False,
                'message': 'Tokens de acesso ou refresh ausentes.'
            }), 400

        # O SupabaseService deve ter um método para definir a sessão
        # e obter os dados do usuário.
        # Por exemplo, usando o access_token para obter o usuário.
        
        # O SupabaseService deve ser capaz de inicializar o cliente com o token
        # e obter a sessão.
        
        # Como não temos a implementação do SupabaseService, vamos simular
        # a criação da sessão e o redirecionamento.
        
        # *** AQUI DEVE ENTRAR A LÓGICA REAL DE CRIAÇÃO DE SESSÃO COM O SUPABASE ***
        # Exemplo:
        # user_session = supabase_service.set_session(access_token, refresh_token)
        # if user_session:
        #     session['user'] = user_session.user.id
        #     session['access_token'] = access_token
        #     session['refresh_token'] = refresh_token
        #     return jsonify({
        #         'success': True,
        #         'redirect_url': url_for('biblioteca.dashboard_usuario') # Redirecionar para a dashboard
        #     })
        # else:
        #     return jsonify({
        #         'success': False,
        #         'message': 'Falha ao criar a sessão do usuário.'
        #     }), 401
        
                # *** AQUI ENTRA A LÓGICA REAL DE CRIAÇÃO DE SESSÃO COM O SUPABASE ***
        
        # 1. Obter o email do usuário a partir do access_token (JWT)
            user_email = supabase_service.get_user_email_from_token(access_token)
        
        if not user_email:
            return jsonify({
                'success': False,
                'message': 'Falha ao obter o email do usuário a partir do token.'
            }), 401
            
        # 2. Verificar se o usuário existe na tabela 'usuario'
        usuario_result = supabase_service.obter_usuario_por_email(user_email)
        
        if not usuario_result['success']:
            # Se o usuário não existe, precisamos criá-lo.
            # O Supabase Auth já criou o usuário na tabela 'auth.users',
            # mas precisamos criar o registro correspondente na tabela 'usuario'.
            
            # **NOTA:** O login social não fornece a senha, então usaremos um hash
            # vazio ou um valor padrão para a coluna 'senha' na tabela 'usuario'.
            # A autenticação futura será feita via Supabase Auth (tokens).
            
            # O Supabase Auth não fornece o nome do usuário diretamente no token,
            # mas o nome completo geralmente está no campo 'user_metadata' ou 'full_name'.
            # Como estamos decodificando o JWT, vamos assumir que o nome não está disponível
            # e usar o email como nome temporário.
            
            # Para fins de demonstração, vamos usar o email como nome e uma senha
            # hash vazia para satisfazer a restrição NOT NULL da tabela 'usuario'.
            
            # Criar um hash de senha vazio para usuários de login social
            empty_password_hash = supabase_service.hash_password(secrets.token_urlsafe(16))
            
            # Tenta criar o usuário na tabela 'usuario'
            try:
                insert_result = supabase_service.supabase.table('usuario').insert({
                    'nome': user_email.split('@')[0], # Nome temporário
                    'email': user_email,
                    'senha': empty_password_hash, # Senha hash vazia
                    'perfil': 'usuario'
                }).execute()
                
                if not insert_result.data:
                    raise Exception("Falha ao inserir usuário na tabela 'usuario'.")
                
                usuario_id = str(insert_result.data[0]['id'])
                usuario_nome = insert_result.data[0]['nome']
                usuario_perfil = insert_result.data[0]['perfil']
                
                # Tenta criar o registro na tabela 'leitor' (opcional, mas recomendado)
                # Como não temos os dados de endereço/telefone, criamos com valores nulos
                supabase_service.criar_leitor(usuario_id, id_endereco=None, telefone=None, email=user_email)
                
            except Exception as e:
                print(f"[ERRO LOGIN SOCIAL] Falha ao criar usuário/leitor: {e}")
                # Retorna um erro que será capturado pelo callback.html
                return jsonify({
                    'success': False,
                    'message': f'Database error saving new user: {str(e)}'
                }), 500
                
        else:

            # Usuário já existe, apenas atualiza a sessão
            usuario_id = str(usuario_result['data']['id'])
            usuario_nome = usuario_result['data']['nome']
            usuario_perfil = usuario_result['data']['perfil']
            
        # 3. Criar a sessão no Flask
        session['usuario_id'] = usuario_id
        session['usuario_perfil'] = usuario_perfil
        session['usuario_nome'] = usuario_nome
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        session['user_email'] = user_email
        
        # 4. Aplicar a lógica de redirecionamento condicional
        if user_email == 'miguel.0205brgg@gmail.com':
            redirect_route = 'biblioteca.dashboard_dev'
        elif user_email == 'sigor2154@gmail.com':
            redirect_route = 'biblioteca.dashboard_usuario'
        else:
            # Redirecionamento padrão para outros usuários
            redirect_route = 'biblioteca.dashboard_usuario' 
            
        # 5. Redirecionar para a rota apropriada
        return jsonify({
            'success': True,
            'redirect_url': url_for(redirect_route)
        })
    except Exception as e:
        print(f"Erro ao definir o token de sessão: {e}")
        return jsonify({
            'success': False,
            'message': 'Erro interno ao processar o token.'
        }), 500

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
