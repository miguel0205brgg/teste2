import os
import sys
from flask import Flask, render_template, redirect
from src.routes.biblioteca import biblioteca_bp
from src.config import SECRET_KEY, DEBUG

# Não altere esta linha
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
)
app.config['SECRET_KEY'] = SECRET_KEY

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


@app.route('/login')
def login():
    """Renderiza a página de login"""
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
