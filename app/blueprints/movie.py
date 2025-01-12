from logging import getLogger

from flask import Blueprint, render_template

from app.api_client import Client

movie_bp = Blueprint("movie", __name__, url_prefix="/movies")

client = Client(getLogger(__name__))


@movie_bp.route("/popular")
def popular():
    return render_template(
        "movie/index.html", title="Films populaires", movies=client.get_popular_movies()
    )


@movie_bp.route("/trending")
def trending():
    return render_template(
        "movie/index.html", title="Films tendances", movies=client.get_trending_movies()
    )


@movie_bp.route("/upcoming")
def upcoming():
    return render_template(
        "movie/index.html", title="Films à venir", movies=client.get_upcoming_movies()
    )


@movie_bp.route("/top_rated")
def top_rated():
    return render_template(
        "movie/index.html",
        title="Films les mieux notés",
        movies=client.get_top_rating_movies(),
    )


@movie_bp.route("/<int:movie_id>")
def details(movie_id: int):
    return render_template(
        "movie/details.html",
        title="Détails du film",
        movie=client.get_movie_by_id(movie_id),
        credits=client.get_movie_credits(movie_id),
    )
