from flask import Blueprint, render_template, session, redirect, url_for
from src.config import SUPABASE_URL, SUPABASE_KEY
from src.services.supabase_service import supabase_client

frontend_bp = Blueprint("frontend", __name__, template_folder="../../templates")

@frontend_bp.route("/")
def index():
    return render_template("index.html")

@frontend_bp.route("/login")
def login_page():
    return render_template("login.html", SUPABASE_URL=SUPABASE_URL, SUPABASE_KEY=SUPABASE_KEY)

@frontend_bp.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html", SUPABASE_URL=SUPABASE_URL, SUPABASE_KEY=SUPABASE_KEY)

@frontend_bp.route("/dashboard_usuario")
def dashboard_usuario():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("frontend.login_page"))

    # Busca usuário no Supabase
    usuario_res = supabase_client.obter_usuario_por_email(usuario_id)
    if not usuario_res["success"]:
        session.pop("usuario_id", None)
        return redirect(url_for("frontend.login_page"))

    usuario = usuario_res["data"]
    return render_template("dashboard_usuario.html", usuario=usuario)

@frontend_bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    return redirect(url_for("frontend.login_page"))

@frontend_bp.route("/<path:filename>")
def serve_html_files(filename):
    # Rota para servir outros arquivos HTML do diretório 'templates'
    # Ex: /login -> login.html
    # Ex: /dashboard_usuario -> dashboard_usuario.html
    
    # Adiciona a extensão .html se não estiver presente
    if not filename.endswith(".html"):
        filename = filename + ".html"
        
    return render_template(filename)
