"""Sensor Server core database functionality.

Include functions for database initialization, and for opening and
closing database connections.
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db_connection():
    """Get or create database connection."""

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db_connection(e=None):
    """Close an opened database connection."""

    conn = g.pop('db', None)

    if conn is not None:
        conn.close()


def init_db():
    """Initialize database.

    Create a new database if one does not exist, or reset an existing
    database. Use with care - calling this function when a database
    exists will clear all existing data.
    """

    conn = get_db_connection()

    with current_app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""

    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Called by the app factory for database commands initialization."""

    app.teardown_appcontext(close_db_connection)
    app.cli.add_command(init_db_command)
