from logging import getLogger

from flask import Blueprint, render_template, request

from app.api_client import Client

person_bp = Blueprint("person", __name__, url_prefix="/person")

client = Client(getLogger(__name__))


@person_bp.route("/")
def popular():
    persons = client.get_popular_persons()
    return render_template("person/popular.html", title="Liste d'artistes", persons=persons)


@person_bp.route("/search")
def search():
    query = request.args.get("query")
    # persons = client.search_persons(query)
    return render_template("person/search.html", title="Recherche d'artistes", persons={})


@person_bp.route("/<int:person_id>")
def details(person_id: int):
    person = client.get_person(person_id)
    return render_template("person/details.html", title="Détails d'un acteur", person=person)
