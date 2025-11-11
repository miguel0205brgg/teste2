from flask import Flask, render_template
from flask_cors import CORS
from src.routes.biblioteca import biblioteca_bp
from src.routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(biblioteca_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
