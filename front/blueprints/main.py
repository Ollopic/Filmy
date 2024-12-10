from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("main/index.html", title="Page d'accueil")
