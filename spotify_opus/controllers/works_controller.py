from flask import Blueprint, render_template

from spotify_opus import db
from spotify_opus.models.Composer import Composer
from spotify_opus.models.Work import Work
from spotify_opus.services.oauth_service import verify_user

work = Blueprint(
    "work", __name__, url_prefix='/composers/<int:composer_id>/works')

@work.route("/")
@verify_user
def get_all(composer_id: int, user, req_header):
    """Gets all works written by the composer ID contained in the
    path of the url."""

    query = db.session.query(Work)
    query = query.join(Work.composer)
    query = query.filter(Composer.composer_id == composer_id)

    works = query.all()

    return render_template("works.html", works=works)




