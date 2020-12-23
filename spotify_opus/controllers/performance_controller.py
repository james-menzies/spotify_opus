from flask import Blueprint
from sqlalchemy.orm import joinedload

from spotify_opus import db
from spotify_opus.models.Performance import Performance
from spotify_opus.models.Work import Work
from spotify_opus.services.oauth_service import verify_user

performance = Blueprint("performance", __name__, url_prefix="/works/<int:work_id>/performances")


@performance.route("/")
@verify_user
def get_by_work(work_id: int, user, req_header):
    """Get all of the performances of a particular work
    and display to the user."""

    work = db.session.query(Work).get(work_id)

    query = db.session.query(Performance)
    query = query.join(Performance.work)
    query = query.filter(Work.work_id == work_id)
    query = query.options(joinedload(Performance.album))

    performances = query.all()


