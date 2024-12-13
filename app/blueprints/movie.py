from flask import Blueprint, render_template

movie_bp = Blueprint("movie", __name__, url_prefix="/movie")


@movie_bp.route("/")
def movie_catalog():
    return render_template("movie/discover.html", title="Liste de films")
