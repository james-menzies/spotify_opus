import importlib

import click
from flask import Blueprint
from flask_migrate import upgrade

from spotify_opus import db

manage_commands = Blueprint("manage", __name__)


@manage_commands.cli.command("reset")
@click.option('--migrate/--no-migrate', default=True)
@click.pass_context
def reset_db(ctx, migrate):
    """This operation will set up a database as if it were brand
    new for production, with no additional data."""
    ctx.invoke(delete_db)
    if migrate:
        upgrade()
    else:
        db.create_all()

    print("Empty tables created.")


@manage_commands.cli.command("delete")
def delete_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")


@manage_commands.cli.command("pull")
@click.argument('composer_id')
def pull_external_data(composer_id):
    from scripts.data_extraction import extract_data

    try:
        composer_id = int(composer_id)
    except ValueError:
        print("Please supply a valid Composer ID")

    extract_data(composer_id)


@manage_commands.cli.command("run")
@click.argument("module")
def generate_works(module):
    """
    Will run a specific script located in the scripts folder. This is mainly
    a pass through method to provide an application context for the script.
    """
    importlib.import_module(f"scripts.{module}")
