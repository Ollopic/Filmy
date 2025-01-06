from logging import getLogger

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from app.api_client import Client

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

client = Client(getLogger(__name__))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            token = client.get_token(email, password)
            resp = make_response(redirect(url_for("main.home")))
            resp.set_cookie("token", token)
            flash("Connexion réussie !", "success")
            return resp
        except Exception:
            flash("E-mail ou mot de passe incorrect", "error")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", title="Page de connexion")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            client.create_user(username, email, password)
            flash("Utilisateur créé avec succès !", "success")
            return redirect(url_for("auth.login"))
        except Exception:
            flash("Erreur lors de la création de l'utilisateur", "error")
            return redirect(url_for("auth.register"))

    return render_template("auth/register.html", title="Page d'inscription")


@auth_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.home")))
    resp.delete_cookie("token")
    flash("Déconnexion réussie !", "success")
    return resp
