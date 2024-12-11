from flask import Blueprint, redirect, render_template, url_for

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html", title="Page de connexion")


@auth_bp.route("/register")
def register():
    return render_template("auth/register.html", title="Page d'inscription")


@auth_bp.route("/logout")
def logout():
    return redirect(url_for("main.home"))
