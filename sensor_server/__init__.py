"""Sensor Server initialization and main application factory."""

import os
from flask import Flask

# Constants used for describing data key names (in REST requests and
# in JSON data).
SENSOR_ID_KEY = 'sensor-id'
READING_TYPE_KEY = 'reading-type'
VALUE_KEY = 'value'
TIMESTAMP_KEY = 'timestamp'
READINGS_LIST_KEY = 'sensor-readings'


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
    from .db import db_core
    db_core.init_app(app)
    # Initialize Flask RESTful module.
    from . import sensors_app
    sensors_app.init_rest_api(app)

    return app
