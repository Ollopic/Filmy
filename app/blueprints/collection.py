import base64
from logging import getLogger

import flask
from flask import Blueprint, redirect, render_template, request, url_for

from app.api_client import Client

collection_bp = Blueprint("collection", __name__, url_prefix="/collection")

client = Client(getLogger(__name__))


@collection_bp.route("/")
def hub():
    return render_template(
        "collection/index.html",
        title="Liste de vos collections",
        collections=client.get_all_collections(request.cookies["token"]),
    )


@collection_bp.route("/<int:collection_id>")
def view(collection_id):
    collection = client.get_collection(request.cookies["token"], collection_id)
    return render_template(
        "collection/view.html", title="Vue d'une collection", collection=collection
    )

@collection_bp.route("/add_collection_item", methods=["POST"])
def add_collection_item():
    collection = request.form.get("collection")
    state = request.form.get("state")
    film_id = request.form.get("film-id")

    is_wishlist = request.args.get("wishlist")

    if request.cookies["token"]:
        if is_wishlist:
            res = client.transfer_wishlist_to_collection(request.cookies["token"], collection, film_id, state)
        else:
            res = client.add_item_into_collection(
                request.cookies["token"], collection, film_id, state
            )
        if res.get("error"):
            flask.flash(res["error"], "error")
        return redirect(url_for("movie.details", movie_id=film_id))

    return render_template(
        "main/index.html",
        title="Page d'accueil",
        movies_now_playing=client.get_movies_now_playing(),
    )


@collection_bp.route("/add", methods=["POST"])
def add_collection():
    name = request.form.get("name")
    token = request.cookies["token"]
    if token:
        res = client.create_collection(token, name)
        if res.get("error"):
            flask.flash(res["error"], "error")

        flask.flash("Film bien ajouté à votre collection !", "success")
        return redirect(url_for("collection.hub"))

    return render_template(
        "main/index.html",
        title="Page d'accueil",
        movies_now_playing=client.get_movies_now_playing(),
    )


@collection_bp.route("/<int:collection_id>/delete", methods=["POST"])
def delete_collection(collection_id):
    collection = client.delete_collection(request.cookies["token"], collection_id)
    if collection.get("error"):
        flask.flash(collection["error"], "error")
        return redirect(url_for("collection.hub"))

    flask.flash("Collection bien supprimée !", "success")
    return redirect(url_for("collection.hub"))


@collection_bp.route("/<int:collection_id>/edit", methods=["GET", "POST"])
def edit(collection_id):
    if request.method == "POST":
        collection_data = {}
        collection_data.update({"name": request.form.get("name")})
        picture = request.files.get("file")
        if picture and picture != "":
            collection_data.update(
                {"picture": base64.b64encode(picture.read()).decode()}
            )

        if collection_data:
            res = client.update_collection(
                request.cookies["token"], collection_id, collection_data
            )
            if res.get("error"):
                flask.flash(res["error"], "error")
                return redirect(url_for("collection.edit", collection_id=collection_id))

        flask.flash("Collection bien mise à jour !", "success")
        return redirect(url_for("collection.view", collection_id=collection_id))

    collection = client.get_collection(request.cookies["token"], collection_id)
    return render_template(
        "collection/edit.html", title="Edition d'une collection", collection=collection
    )


@collection_bp.route("/<int:collection_id>/<int:movie_id>/update", methods=["POST"])
def update_item(collection_id: int, movie_id: int):
    token = request.cookies.get("token")
    if token:
        item_data = {}
        borrowed = request.form.get("borrowed")
        if borrowed:
            item_data.update({"borrowed": borrowed == "true"})
        favorite = request.form.get("favorite")
        if favorite:
            item_data.update({"favorite": favorite == "true"})

        res = client.update_collection_item(token, collection_id, movie_id, item_data)
        if res.get("error"):
            flask.flash(res["error"], "error")
            return redirect(
                url_for("movie.details", collection_id=collection_id, movie_id=movie_id)
            )

        flask.flash("Opération menée avec succès !", "success")
        return redirect(
            url_for("movie.details", collection_id=collection_id, movie_id=movie_id)
        )

    return redirect(url_for("main.home"))

@collection_bp.route("/<int:collection_id>/<int:movie_id>/delete", methods=["POST"])
def delete_collection_item(collection_id, movie_id):
    collection = client.delete_collection_item(request.cookies["token"], collection_id, movie_id)
    if collection.get("error"):
        flask.flash(collection["error"], "error")
        return redirect(url_for("collection.hub"))

    flask.flash("Film bien supprimé de votre collection !", "success")
    return redirect(url_for("collection.view", collection_id=collection_id))