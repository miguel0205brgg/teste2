from flask import Flask, render_template
from flask_cors import CORS
from src.routes.biblioteca import biblioteca_bp
from src.routes.auth import auth_bp
from src.routes.frontend import frontend_bp

app = Flask(__name__, template_folder="templates")
CORS(app)

app.register_blueprint(biblioteca_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(frontend_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
