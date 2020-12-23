from flask import Blueprint

from spotify_opus.services.oauth_service import verify_user

performance = Blueprint("performance", __name__, url_prefix="/works/<int:work_id>/performances")


@performance.route("/")
@verify_user
def get_by_work(work_id: int, user, req_header):
    """Get all of the performances of a particular work
    and display to the user."""

    return f"Viewing performances for work_id {work_id}"
