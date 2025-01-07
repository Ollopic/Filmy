from logging import getLogger

import requests
from flask import Flask, flash, redirect, request, url_for

from . import config
from .api_client import Client
from .blueprints import artist_bp, auth_bp, main_bp, movie_bp

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

client = Client(getLogger(__name__))


# Protect routes that require authentication by checking the token validity
@app.after_request
def validate_token(response):
    if "token" in request.cookies:
        token = request.cookies["token"]
        try:
            client.get_me(token)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422 or (
                e.response.status_code == 401
                and e.response.json().get("msg") == "Token has expired"
            ):
                response = redirect(url_for("auth.login"))
                response.delete_cookie("token")
                flash("Token expiré, veuillez vous reconnecter", "error")
                return response

    return response


@app.context_processor
def is_user_connected():
    token = request.cookies.get("token")
    return dict(is_connected=token is not None)


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(artist_bp)
