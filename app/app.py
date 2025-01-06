from flask import Flask, request

from . import config
from .blueprints import artist_bp, auth_bp, main_bp, movie_bp

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY


@app.context_processor
def is_user_connected():
    token = request.cookies.get("token")
    return dict(is_connected=token is not None)


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(artist_bp)
