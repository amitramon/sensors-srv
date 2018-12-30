"""Sensor Server initialization and main application factory."""

import os

from flask import Flask

from .db import db_core
from . import sensors_app


def create_app(test_config=None):
    """The main app factory - create and initialize an app instance.

    Return: the created instance.
    """

    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sensors.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database module.
    db_core.init_app(app)
    # Initialize Flask RESTful module.
    sensors_app.init_rest_api(app)

    return app
