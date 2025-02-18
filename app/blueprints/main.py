import base64
from logging import getLogger

from flask import Blueprint, redirect, render_template, request, url_for

from app.api_client import Client

main_bp = Blueprint("main", __name__)

client = Client(getLogger(__name__))


@main_bp.route("/")
def home():
    return render_template(
        "main/index.html",
        title="Page d'accueil",
        movies_now_playing=client.get_movies_now_playing(),
    )


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

        return redirect(url_for("main.profile"))

    return render_template(
        "main/profile.html",
        title="Profil",
        wishlist=client.get_wishlist(request.cookies["token"]),
    )


@main_bp.route("/about", methods=["GET"])
def about():
    return render_template("main/about.html", title="A propos")


@main_bp.route("/confidentiality", methods=["GET"])
def confidentiality():
    return render_template(
        "main/confidentiality.html", title="Politique de confidentialité"
    )


@main_bp.route("/licence", methods=["GET"])
def licence():
    return render_template("main/licence.html", title="Licence")
