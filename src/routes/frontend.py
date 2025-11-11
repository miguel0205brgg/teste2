from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__, template_folder="../../templates")

@frontend_bp.route("/")
def index():
    # Renderiza o template index.html
    return render_template("index.html")

@frontend_bp.route("/<path:filename>")
def serve_html_files(filename):
    # Rota para servir outros arquivos HTML do diretório 'templates'
    # Ex: /dashboard_usuario.html
    if filename.endswith(".html"):
        return render_template(filename)
    # Se não for um arquivo HTML, deixa o Flask retornar 404 ou procurar em 'static'
    return render_template(filename) # Isso ainda pode causar TemplateNotFound, mas é o que o código original faria.
