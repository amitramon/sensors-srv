# sensor_server - simple demo of Flask RESTful service.
#
# Copyright (C) 2019 Amit Ramon <amit.ramon@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Sensor Server REST API.

Includes URL routing defintions and request handling rutines.
"""

from flask_restful import reqparse, abort, Api, Resource

from . import commons as cmn
from .db import db_access


class SensorError(Exception):
    """Exception thrown on data errors."""

    def __init__(self, err_code, message):
        super().__init__(message)
        self.err_code = err_code


def error_abort(func):
    """Decorator for handling excepions thrown by data access methods."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SensorError as e:
            abort(e.err_code, message=str(e))
        except Exception as e:
            abort(500, message=f'An error occurred: {str(e)}')

    return wrapper


class SensorRequestParser(reqparse.RequestParser):
    """Parser for paring 'add reading' rquest data."""

    def __init__(self):
        super().__init__()
        self.add_argument(cmn.SENSOR_ID_KEY, type=int,
                          help='id of sensor; type: integer value')
        self.add_argument(cmn.READING_TYPE_KEY,
                          help='type of sensor reading; type: string')
        self.add_argument(cmn.VALUE_KEY, type=float,
                          help='value of sensor reading;'
                          ' type: floating point value')


class SensorData(Resource):

    @error_abort
    def get(self):
        """Get list of all stored readings."""

        return {cmn.READINGS_LIST_KEY: db_access.get_sensor_readings()}


class SensorAdd(Resource):

    def __init__(self):
        self._parser = SensorRequestParser()

    @error_abort
    def post(self):
        """Add a new sensor reading."""

        args = self._parser.parse_args()
        new_reading = db_access.add_sensor_reading(args[cmn.SENSOR_ID_KEY],
                                                   args[cmn.READING_TYPE_KEY],
                                                   args[cmn.VALUE_KEY])

        # Return the newly added data and HTTP 'Created' status (201).
        return new_reading, 201


class Sensor(Resource):

    @error_abort
    def get(self):
        """Get a list of available Sensor Id."""

        return {'sensor-ids': db_access.get_sensor_ids()}


class SensorType(Resource):

    @error_abort
    def get(self):
        """Get a list of all available sensor types."""

        return {'sensor-types': db_access.get_sensor_types()}


class SensorById(Resource):

    @error_abort
    def get(self, sensor_id):
        """Get all readings for the given sensor_id."""

        readings = db_access.get_sensor_readings(sensor_id)

        if not readings:
            raise SensorError(404,
                              f"Sensor Id {sensor_id} doesn't exist")

        return {cmn.SENSOR_ID_KEY: sensor_id,
                cmn.READINGS_LIST_KEY: readings}


class SensorByType(Resource):

    @error_abort
    def get(self, reading_type):
        """Get all readings for the given reading type."""

        readings = db_access.get_sensor_readings_by_type(reading_type)

        if not readings:
            raise SensorError(404,
                              f"Reading Type {reading_type} doesn't exist")

        return {cmn.READING_TYPE_KEY: reading_type,
                cmn.READINGS_LIST_KEY: readings}


def init_rest_api(app):
    """Initialize Flask restful and set up the URL routing rules."""

    api = Api(app, catch_all_404s=True)

    # Get all sensors data.
    api.add_resource(SensorData, '/')

    # Add a new reading (using POST).
    api.add_resource(SensorAdd, '/add/')

    # Get a list of available Sensor Ids.
    api.add_resource(Sensor, '/sensors/')

    # Get a sensor reading by Sensor Id.
    api.add_resource(SensorById, '/sensors/<sensor_id>')

    # Get a list of available sensor types.
    api.add_resource(SensorType, '/types/')

    # Get a sensor reading record by reading type.
    api.add_resource(SensorByType, '/types/<reading_type>')
