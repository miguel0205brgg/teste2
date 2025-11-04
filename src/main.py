import os
import sys
from flask import Flask, render_template, redirect, jsonify, request, session
from src.routes.biblioteca import biblioteca_bp
from src.config import SECRET_KEY, DEBUG
from src.services.supabase_service import SupabaseService

# Não altere esta linha
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Define o caminho base do projeto (TESTE2-MAIN)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),
    static_url_path='/static',  # Adicionado para garantir o mapeamento correto
    template_folder=os.path.join(BASE_DIR, 'templates')
)
app.config['SECRET_KEY'] = SECRET_KEY

# Inicializar serviço Supabase
supabase_service = SupabaseService()

# Registrar as rotas da biblioteca
app.register_blueprint(biblioteca_bp, url_prefix='/api')


@app.route('/')
def index():
    """Renderiza a página inicial"""
    return render_template('index.html')


@app.route('/cadastro')
def cadastro():
    """Renderiza a página de cadastro"""
    return render_template('cadastro.html')


@app.route("/login")
def login():
    """Renderiza a página de login"""
    return render_template("login.html")

@app.route("/biblioteca")
def biblioteca():
    """Renderiza a página da biblioteca após o login"""
    return render_template("biblioteca.html")

@app.route("/dashboard-dev")
def dashboard_dev():
    """Renderiza a página de dashboard de desenvolvedor"""
    return render_template("dashboard_dev.html")


@app.route("/perfil")
def perfil():
    """Renderiza a página de perfil do usuário"""
    # TODO: Implementar lógica para buscar dados do usuário da sessão/banco de dados
    # Por enquanto, retorna a página com dados de exemplo
    usuario = {
        'nome': 'Usuário Exemplo',
        'email': 'usuario@exemplo.com',
        'perfil': 'USER',
        'criado_em': '2025-01-01T10:00:00',
        'leitor': None
    }
    return render_template("perfil.html", usuario=usuario)


@app.route("/api/perfil/atualizar", methods=["POST"])
def atualizar_perfil():
    """Endpoint para atualizar os dados do perfil do usuário"""
    try:
        # Verificar se o usuário está autenticado
        if 'usuario_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Usuário não autenticado'
            }), 401
        
        # Obter dados do formulário
        data = request.json
        nome = data.get('nome')
        email = data.get('email')
        
        # Validar dados obrigatórios
        if not nome or not email:
            return jsonify({
                'success': False,
                'message': 'Nome e e-mail são obrigatórios'
            }), 400
        
        # Atualizar dados do usuário no banco de dados
        result = supabase_service.atualizar_usuario(
            usuario_id=session['usuario_id'],
            nome=nome,
            email=email
        )
        
        if result['success']:
            # Atualizar dados da sessão
            session['usuario_nome'] = nome
            return jsonify({
                'success': True,
                'message': 'Perfil atualizado com sucesso',
                'data': result.get('data')
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result.get('message', 'Erro ao atualizar perfil')
            }), 400
    
    except Exception as e:
        print(f"[ERROR] Erro ao atualizar perfil: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro interno do servidor'
        }), 500


@app.route("/logout")
def logout():
    """Realiza logout do usuário"""
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
