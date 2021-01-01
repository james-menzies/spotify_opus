from flask import Blueprint, render_template, request, abort
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import asc, func

from spotify_opus import db
from spotify_opus.models.Composer import Composer
from spotify_opus.models.Work import Work
from spotify_opus.services.oauth_service import VerifyUser

work = Blueprint(
    "work", __name__, url_prefix='/composers/<int:composer_id>/works')

standard_limit = 30


@work.route("/")
@VerifyUser()
def get_all(composer_id: int, user, req_header):
    """Gets all works written by the composer ID contained in the
    path of the url."""
    per_page = 30
    page = request.args.get(get_page_parameter(), type=int, default=1)

    work_query = db.session.query(Work)
    work_query = work_query.join(Work.composer)
    work_query = work_query.filter(Composer.composer_id == composer_id)
    work_query = work_query.order_by(asc(Work.name))
    work_query = work_query.limit(per_page)
    work_query = work_query.offset((page - 1) * per_page)

    works = work_query.all()

    count_query = db.session.query(func.count(Work.work_id))
    count_query = count_query.join(Work.composer)
    count_query = count_query.filter(Composer.composer_id == composer_id)

    count = db.session.execute(count_query).scalar()

    composer = db.session.query(Composer).get(composer_id)

    pagination = Pagination(page=page, total=count, per_page=per_page,
                            css_framework='bootstrap4')

    return render_template("works.jinja2", works=works,
                           navbar=True, user=user,
                           composer=composer.name, pagination=pagination)
