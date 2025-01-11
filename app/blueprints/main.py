import base64
from logging import getLogger

from flask import Blueprint, render_template, request

from app.api_client import Client

main_bp = Blueprint("main", __name__)

client = Client(getLogger(__name__))


@main_bp.route("/")
def home():
    return render_template("main/index.html", title="Page d'accueil", movies_now_playing=client.get_movies_now_playing())


@main_bp.route("/search")
def search():
    results = client.get_movie_by_title(request.args.get("title") or "")
    return render_template("main/search.html", title="Recherche", movies=results["movies"], total_results=results["total_results"])


@main_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        profile_data = {}
        profile_data.update({"username": request.form.get("username")})
        profile_data.update({"mail": request.form.get("email")})
        profile_picture = request.files.get("file")
        if profile_picture and profile_picture != "":
            profile_data.update(
                {"profile_image": base64.b64encode(profile_picture.read()).decode()}
            )

        if profile_data:
            client.update_user(request.cookies["token"], profile_data)

    return render_template("main/profile.html", title="Profil")
