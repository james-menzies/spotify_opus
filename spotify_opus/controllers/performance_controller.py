from flask import Blueprint, url_for, render_template
from sqlalchemy.orm import joinedload

from spotify_opus import db
from spotify_opus.models.Performance import Performance
from spotify_opus.models.Work import Work
from spotify_opus.models.viewmodels import CategoryResultVM, SearchItemVM, AlbumVM, TrackVM
from spotify_opus.services.oauth_service import VerifyUser

performance = Blueprint("performance", __name__)


@performance.route("/works/<int:work_id>/performances")
@VerifyUser()
def get_by_work(work_id: int, user, req_header):
    """Get all of the performances of a particular work
    and display to the user."""

    work = db.session.query(Work).get(work_id)

    query = db.session.query(Performance)
    query = query.join(Performance.work)
    query = query.filter(Work.work_id == work_id)
    query = query.options(joinedload(Performance.album))

    performances = query.all()

    container = CategoryResultVM(f"{work.name} ({work.composer.name})")
    results = [container]

    for performance in performances:
        album = performance.album

        artist_names = [artist.name for artist in performance.tracks[0].artists]

        if len(artist_names) > 1:
            artist_names.remove(work.composer.name)

        vm = SearchItemVM(url=url_for(".playback", performance_id=performance.performance_id, ),
                          image_url=album.image_url,
                          primary_label=artist_names[0],
                          sec_labels=artist_names[1:])
        container.items.append(vm)

    username = user["display_name"]

    return render_template("media.html", results=results, navbar=True, username=username)


@performance.route("/performances/<int:performance_id>")
@VerifyUser()
def playback(performance_id: int, user, req_header):
    """Render the playback page for a performance."""

    query = db.session.query(Performance)
    query = query.options(joinedload(Performance.album))

    performance = query.get(performance_id)

    vm = AlbumVM(performance.album.name)
    vm.image_url = performance.album.image_url
    vm.artists = [artist.name for artist in performance.tracks[0].artists]

    for track in performance.tracks:

        total_duration_in_seconds = track.duration_ms // 1000
        sec_attr = total_duration_in_seconds % 60
        min_attr = total_duration_in_seconds // 60
        final_duration = f"{min_attr}:{sec_attr:02}"
        track_vm = TrackVM(track.sanitized_name, duration=final_duration)
        vm.tracks.append(track_vm)

    return render_template("album.html", album=vm)


