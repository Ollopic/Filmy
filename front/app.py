from flask import Flask

from .blueprints import auth_bp, main_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
