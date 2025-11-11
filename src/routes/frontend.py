from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__, template_folder="../../templates")

@frontend_bp.route("/")
def index():
    return render_template("index.html")

@frontend_bp.route("/<path:filename>")
def serve_html_files(filename):
    if not filename.endswith(".html"):
        filename += ".html"
    return render_template(filename)
