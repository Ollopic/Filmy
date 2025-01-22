from logging import getLogger

from flask import Blueprint, render_template, request, url_for, flash, redirect

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
    return render_template(
        "movie/search.html",
        title="Recherche",
        movies=results["movies"],
        total_results=results["total_results"],
    )


@movie_bp.route("/popular")
def popular():
    page = request.args.get("page", 1, type=int)

    return render_template(
        "movie/index.html",
        title="Films populaires",
        movies=client.get_popular_movies(page=page),
        movie_genres=movie_genres,
    )


@movie_bp.route("/trending")
def trending():
    page = request.args.get("page", 1, type=int)

    return render_template(
        "movie/index.html",
        title="Films tendances",
        movies=client.get_trending_movies(page=page),
        movie_genres=movie_genres,
    )


@movie_bp.route("/upcoming")
def upcoming():
    page = request.args.get("page", 1, type=int)

    return render_template(
        "movie/index.html",
        title="Films à venir",
        movies=client.get_upcoming_movies(page=page),
        movie_genres=movie_genres,
    )


@movie_bp.route("/top_rated")
def top_rated():
    page = request.args.get("page", 1, type=int)

    return render_template(
        "movie/index.html",
        title="Films les mieux notés",
        movies=client.get_top_rating_movies(page=page),
        movie_genres=movie_genres,
    )


@movie_bp.route("/<int:movie_id>")
def details(movie_id: int):
    token = request.cookies.get("token")
    collections = client.get_all_collections(token) if token else None
    return render_template(
        "movie/details.html",
        title="Détails du film",
        movie=client.get_movie_by_id(movie_id, token),
        credits=client.get_movie_credits(movie_id),
        collections=collections,
    )

@movie_bp.route("/<int:movie_id>/wishlist", methods=["POST"])
def wishlist(movie_id: int):
    token = request.cookies.get("token")

    res = client.add_to_wishlist(token, movie_id)
    if res.get("error"):
        flash(res["error"], "error")

    return redirect(url_for("movie.details", movie_id=movie_id))
