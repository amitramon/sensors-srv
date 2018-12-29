"""Sensor Server database query and insertion."""

from datetime import datetime
from time import time
from . import db_core
from .. import (SENSOR_ID_KEY,
                READING_TYPE_KEY,
                VALUE_KEY,
                TIMESTAMP_KEY)


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
        SENSOR_ID_KEY: row[0],
        READING_TYPE_KEY: row[1],
        VALUE_KEY: row[2],
        TIMESTAMP_KEY: time_sec_to_isoformat(row[3])
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
        SENSOR_ID_KEY: sensor_id,
        READING_TYPE_KEY: reading_type,
        VALUE_KEY: value,
        TIMESTAMP_KEY: time_sec_to_isoformat(time_now)
    }


def get_sensor_ids():
    """Return a list of all stored sensor IDs."""

    return get_col_values('SELECT distinct sensor_id '
                          'FROM sensor ORDER BY sensor_id')


def get_sensor_types():
    """Return a list of all available sensor types."""

    return get_col_values('SELECT distinct reading_type '
                          'FROM sensor ORDER BY reading_type')
