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
    name = request.args.get("name")
    results = client.get_artist_by_name(name)
    return render_template("person/search.html", title="Recherche d'artistes", persons=results["persons"], total_results=results["total_results"])


@person_bp.route("/<int:person_id>")
def details(person_id: int):
    person = client.get_person(person_id)

    def get_sort_date(credit):
        if credit['media_type'] == 'tv' and credit.get('first_air_date'):
            return credit['first_air_date']
        elif credit.get('release_date'):
            return credit['release_date']
        else:
            return '1900-01-01'

    person['combined_credits']['cast'] = sorted(
        person['combined_credits']['cast'],
        key=get_sort_date,
        reverse=True
    )

    person['combined_credits']['crew'] = sorted(
        person['combined_credits']['crew'],
        key=get_sort_date,
        reverse=True
    )
    return render_template("person/details.html", title="Détails d'un acteur", person=person)
