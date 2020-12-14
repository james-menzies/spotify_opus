from flask import Blueprint, render_template, redirect, url_for, session

from spotify_opus.models.viewmodels import CategoryResultVM, SearchItemVM

media = Blueprint("media", __name__)


@media.route("/")
def home_page():
    if 'token' not in session:
        return redirect(url_for("auth.log_in"))

    results = []

    for i in range(1, 4):

        cat = CategoryResultVM(f"Cat number {i}")
        for j in range(1, 5):
            item = SearchItemVM("", "")
            cat.items.append(item)

        results.append(cat)

    return render_template("media.html", results=results, navbar=True)
