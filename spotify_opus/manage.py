import itertools
import os
from pathlib import Path

import click
import pandas
from flask import Blueprint
from flask_migrate import upgrade
from sqlalchemy import inspect

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
    create_defaults()
    print("Defaults added to database.")


@manage_commands.cli.command("delete")
def delete_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")


@manage_commands.cli.command("seed")
@click.pass_context
def seed_db(ctx):

    ctx.invoke(reset_db)
    dir_path = Path.cwd().joinpath("resources", "sample_data")
    add_csv_files(dir_path)
    print("Sample data added to database")

@manage_commands.cli.command("pull")
@click.argument('composer_id')
def pull_external_data(composer_id: int):

    from spotify_opus.services.data_extraction import extract_data

    try:
        composer_id = int(composer_id)
    except ValueError:
        print("Please supply a valid Composer ID")

    extract_data(composer_id)



def add_csv_files(dir_path: Path, custom_order=None):
    """
    Will add all of the csv files to a database provided that
    the database has been properly initialized by Flask Migrate.
    """
    if custom_order:
        filenames = [f"{file}.csv" for file in custom_order]
    else:
        filenames = [scope[2] for scope in os.walk(dir_path)]  # type: ignore
        filenames = list(itertools.chain(*filenames))

    for filename in filenames:
        file_path = dir_path.joinpath(filename)
        data = pandas.read_csv(file_path)
        inspector = inspect(db.engine)
        if file_path.stem not in inspector.get_table_names():
            raise ValueError(
                "Tried to import data where table name does not exist")
        data.to_sql(file_path.stem, db.engine, if_exists='append', index=False)


def create_defaults():
    dir_path = Path.cwd().joinpath("resources", "default_data")
    add_csv_files(dir_path)
