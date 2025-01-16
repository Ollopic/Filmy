from logging import getLogger

from flask import Blueprint, render_template, request

from app.api_client import Client

movie_bp = Blueprint("movie", __name__, url_prefix="/movies")

client = Client(getLogger(__name__))

movie_genres = client.get_movie_genres()


@movie_bp.route("/")
def home():
    params = {
        "sort_by": request.args.get("sort_by"),
        "with_genres": request.args.getlist("with_genres"),
        "release_date.gte": request.args.get("release_date.gte"),
        "release_date.lte": request.args.get("release_date.lte"),
        "with_runtime.gte": request.args.get("with_runtime.gte"),
        "with_runtime.lte": request.args.get("with_runtime.lte"),
    }
    movies = client.discover_movies(params)
    return render_template(
        "movie/index.html",
        title="Films",
        movies=movies,
        movie_genres=movie_genres,
    )

@movie_bp.route("/search")
def search():
    results = client.get_movie_by_title(request.args.get("title") or "")
    return render_template("movie/search.html", title="Recherche", movies=results["movies"], total_results=results["total_results"])


@movie_bp.route("/popular")
def popular():
    return render_template(
        "movie/index.html", title="Films populaires", movies=client.get_popular_movies(), movie_genres=movie_genres
    )


@movie_bp.route("/trending")
def trending():
    return render_template(
        "movie/index.html", title="Films tendances", movies=client.get_trending_movies(), movie_genres=movie_genres
    )


@movie_bp.route("/upcoming")
def upcoming():
    return render_template(
        "movie/index.html", title="Films à venir", movies=client.get_upcoming_movies(), movie_genres=movie_genres
    )


@movie_bp.route("/top_rated")
def top_rated():
    return render_template(
        "movie/index.html",
        title="Films les mieux notés",
        movies=client.get_top_rating_movies(),
        movie_genres=movie_genres
    )


@movie_bp.route("/<int:movie_id>")
def details(movie_id: int):
    return render_template(
        "movie/details.html",
        title="Détails du film",
        movie=client.get_movie_by_id(movie_id),
        credits=client.get_movie_credits(movie_id),
    )
