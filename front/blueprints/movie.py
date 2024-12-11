from flask import Blueprint, render_template

movie_bp = Blueprint("movie", __name__, url_prefix="/movie")


@movie_bp.route("/")
def catalog():
    return render_template("movie/index.html", title="Liste de films")
