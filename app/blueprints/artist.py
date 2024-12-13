from flask import Blueprint, render_template

artist_bp = Blueprint("artist", __name__, url_prefix="/artist")


@artist_bp.route("/")
def artist_list():
    return render_template("artist/discover.html", title="Liste d'artistes")
