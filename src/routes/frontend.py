from flask import Blueprint, render_template
from src.config import SUPABASE_URL, SUPABASE_KEY

frontend_bp = Blueprint("frontend", __name__, template_folder="../../templates")

@frontend_bp.route("/")
def index():
    return render_template("index.html")

@frontend_bp.route("/login")
def login_page():
    # Envia as variáveis do Supabase para o HTML
    return render_template("login.html", SUPABASE_URL=SUPABASE_URL, SUPABASE_KEY=SUPABASE_KEY)

@frontend_bp.route("/<path:filename>")
def serve_html_files(filename):
    if not filename.endswith(".html"):
        filename += ".html"
    return render_template(filename)
