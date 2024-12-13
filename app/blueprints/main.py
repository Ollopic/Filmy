from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("main/index.html", title="Page d'accueil")


@main_bp.route("/search")
def search():
    return render_template("main/search.html", title="Recherche")
