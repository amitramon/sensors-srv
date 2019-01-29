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

"""Sensor Server database query and insertion."""

from datetime import datetime
from time import time

from .. import commons as cmn
from . import db_core


def time_sec_to_isoformat(time_sec):
    """Helper that convert the number of seconds since epoch into
    ISO 8601 timestamp string.
    """
    return datetime.fromtimestamp(time_sec).isoformat()


def get_col_values(query_str):
    """Query the database using given query string.

    Return: list of valued of the first column in the fetched rows.
    """
    conn = db_core.get_db_connection()
    rows = conn.execute(query_str).fetchall()
    return [row[0] for row in rows]


def get_rows(query_str, params=[]):
    """Query the database using given query string and parameters.

    Return: list of dictionaries, each describing a
    single sensor reading.
    """

    conn = db_core.get_db_connection()
    rows = conn.execute(query_str, params).fetchall()

    return [{
        cmn.SENSOR_ID_KEY: row[0],
        cmn.READING_TYPE_KEY: row[1],
        cmn.VALUE_KEY: row[2],
        cmn.TIMESTAMP_KEY: time_sec_to_isoformat(row[3])
    } for row in rows]


def get_sensor_readings(sensor_id=None):
    """Get sensor readings from the database.

    When sensor_id is provided, get readings for that
    sensor; otherwise get all existing readings.

    Return: list of dictionaries, each describing a sensor readings,
    ordered by the reading timestamp.
    """

    query_str = 'SELECT sensor_id, reading_type, value, read_time FROM sensor'

    if sensor_id:
        query_str += ' WHERE sensor_id = ?'
        params = [sensor_id]
    else:
        params = []

    query_str += ' ORDER BY read_time'
    return get_rows(query_str, params)


def get_sensor_readings_by_type(reading_type):
    """Get sensor readings from the database for the given reading type.

    Return: list of dictionaries, each describing a sensor readings,
    ordered by the reading timestamp.
    """

    query_str = 'SELECT sensor_id, reading_type, value, read_time' \
                ' FROM sensor' \
                ' WHERE reading_type = ?' \
                ' ORDER BY read_time'

    return get_rows(query_str, [reading_type])


def add_sensor_reading(sensor_id, reading_type, value):
    """Add a new sensor reading to the readings database.

    Return: a dictionary descibing the newly added reading.
    """

    time_now = time()           # current time as seconds since epoch
    conn = db_core.get_db_connection()
    conn.execute(
        'INSERT INTO sensor (sensor_id, reading_type, value, read_time)'
        'VALUES (?, ?, ?, ?)',
        (sensor_id, reading_type, value, time_now)
    )
    conn.commit()

    return {
        cmn.SENSOR_ID_KEY: sensor_id,
        cmn.READING_TYPE_KEY: reading_type,
        cmn.VALUE_KEY: value,
        cmn.TIMESTAMP_KEY: time_sec_to_isoformat(time_now)
    }


def get_sensor_ids():
    """Return a list of all stored sensor IDs."""

    return get_col_values('SELECT distinct sensor_id '
                          'FROM sensor ORDER BY sensor_id')


def get_sensor_types():
    """Return a list of all available sensor types."""

    return get_col_values('SELECT distinct reading_type '
                          'FROM sensor ORDER BY reading_type')
