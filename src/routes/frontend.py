from flask import Blueprint, render_template, session, redirect, url_for
from src.services.supabase_service import supabase_client

frontend_bp = Blueprint("frontend", __name__, template_folder="../../templates")

@frontend_bp.route("/")
def index():
    return render_template("index.html")

@frontend_bp.route("/login")
def login_page():
    return render_template("login.html")

@frontend_bp.route("/dashboard_usuario")
def dashboard_usuario():
    email = session.get("usuario_email")
    if not email:
        return redirect(url_for("frontend.login_page"))

    # Busca usuário no Supabase
    usuario_res = supabase_client.obter_usuario_por_email(email)
    if not usuario_res["success"]:
        session.pop("usuario_email", None)
        return redirect(url_for("frontend.login_page"))

    usuario = usuario_res["data"]
    return render_template("dashboard_usuario.html", usuario=usuario)

@frontend_bp.route("/logout")
def logout():
    session.pop("usuario_email", None)
    return redirect(url_for("frontend.login_page"))
