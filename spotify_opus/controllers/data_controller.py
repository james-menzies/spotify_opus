import csv
import os
import shutil
import zipfile
from datetime import datetime
from os.path import basename
from pathlib import Path

from flask import Blueprint, redirect, url_for, flash

from spotify_opus import db
from spotify_opus.services.oauth_service import VerifyUser

data = Blueprint("data", __name__, url_prefix="/data")
success = "Data successfully backed up to server."
error = "Error in backing up data to server."


@data.route("/")
@VerifyUser(admin=True)
def download(user, req_header):
    """Writes all data to a csv file, minus sensitive information, and prepares
    it as a download for the user."""

    try:
        create_backup_archive()
        flash(success, "success")
        return redirect(url_for("composer.get_all"))
    except:
        flash(error, "danger")
        return redirect(url_for("composer.get_all"))


def create_backup_archive():
    dir = Path.cwd().joinpath("temp")
    if not dir.exists():
        dir.mkdir(parents=True)

    tables = [
        "albums",
        "artists",
        "composers",
        "performances",
        "tracks",
        "tracks_artists",
        "works"
    ]

    for table in tables:
        result = db.engine.execute(f"SELECT * FROM {table};").fetchall()
        filename = dir.joinpath(f"{table}.csv")

        with open(filename, "w", encoding="utf-8") as file:
            csv.writer(file).writerows(result)

    stamp = datetime.now().timestamp()

    with zipfile.ZipFile(f"backup/backup_{stamp}.zip", "w") as zfile:
        for dirname, subfolders, filenames in os.walk(dir):
            for filename in filenames:
                filepath = os.path.join(dirname, filename)
                zfile.write(filepath, basename(filepath))

    shutil.rmtree(dir)

    return True
