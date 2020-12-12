from flask import Blueprint

media = Blueprint("media", __name__)


@media.route("/")
def home_page():

    content
