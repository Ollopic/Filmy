from datetime import datetime
from logging import getLogger

import requests
from flask import Flask, flash, redirect, request, url_for

from . import config
from .api_client import Client
from .blueprints import person_bp, auth_bp, main_bp, movie_bp, collection_bp

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

client = Client(getLogger(__name__))


# Protect routes that require authentication by checking the token validity
@app.before_request
def validate_token():
    if "token" in request.cookies:
        token = request.cookies["token"]
        try:
            client.get_me(token)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422 or (
                e.response.status_code == 401
                and e.response.json().get("msg") == "Token has expired"
            ):
                flash("Token expiré, veuillez vous reconnecter", "error")
                response = redirect(url_for("auth.login"))
                response.delete_cookie("token")
                return response


@app.template_filter()
def minutes_to_hours(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}min"

@app.template_filter('age')
def calculate_age(birthdate: str):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    if birthdate:
        today = datetime.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    return ''

@app.template_filter("strftime")
def _jinja2_filter_datetime(date, fmt="%d %b. %Y"):
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    native = date.replace(tzinfo=None)
    date_format = fmt
    return native.strftime(date_format)


@app.context_processor
def is_user_connected():
    token = request.cookies.get("token")
    try:
        user_data = client.get_me(request.cookies["token"]) if token else {}
    except requests.exceptions.HTTPError:
        return dict(is_connected=False, user_data={})

    return dict(is_connected=token is not None, user_data=user_data)


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(person_bp)
app.register_blueprint(collection_bp)
