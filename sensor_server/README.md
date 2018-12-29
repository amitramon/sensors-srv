# Sensors Server

Sensor Server is a simple REST Service that manages a log of sensor
readings.

Using the server API clients can add sensor reading entries to the
database and retrieve stored entries. A sensor reading is comprised of
4 fields:

- `sensor Id`: an integer number that identifies a specific sensor.
- `reading type`: a string that describes the type of the reading (a
  sensor may have more than one reading type; for example, a sensor
  could have both `temperature` and `humidity` readings).
- `value`: a floating point value which is the reading. Note that the
  value should be interpreted in the context of the `reading type`.
- `timestamp`: the time in which the reading was logged by the server.

## Server API

The API for accessing the server by clients is described in the
following sections.

### Adding a Sensor Reading Entry

Adding a reading is done using the following URL (using a `POST` HTTP
request)

    /add/
   
The reading data is passed as `POST` data. For example, using `curl` the
command would look similar to this:

    $ curl -d "sensor-id=2000" -d "reading-type=humidity" -d "value=70" http://www.example.com/add/

(Note that when using `curl` a `-d` switch implies a `POST` request.)

As a response to this call the server return the record of the newly
added reading.

### Getting all Sensor Data

Accessing the server's root URL will return a list of all stored
reading entries, in ascending timestamp order.

`curl` example:

    $ curl http://www.example.com/

### Getting Available Sensor Ids

Use the following URL to obtain a list of all sensor Ids that exist in
the server's database

    /sensors/

The results are in ascending numerical order.

### Getting a Sensor Reading by Sensor Id

Use the following URL to obtain a list of all reading for the given
sensor.

    /sensors/<sensor_id>

The results are in ascending timestamp order. If the given Id dose not
exist in the database a 404 error is returned.
 
`curl` example:

    $ curl http://www.example.com/sensors/42
	
This return a list of all reading of the sensor identified by 42.
	
### Get a List of Available Reading Types

Use the following URL to obtain a list of all reading types that exist
in the server's database

	/types/

The results are in ascending alphabetical order.

### Get a Sensor Reading by Reading Type

Use the following URL to obtain a list of all reading (possibly from
different sensors) for the given reading type.

    /types/<reading_type>

The results are in ascending timestamp order. If the given reading
type dose not exist in the database a 404 error is returned.

`curl` example:

    $ curl http://www.example.com/types/temperature

### Notes

1. Note that URLs for retrieving lists of resources ends with a
   trailing slash (/). On calling the server without the trailing
   slash, the server will redirect the call to the same URL but with
   the trailing slash.

2. In case of invalid URL, including a non existing sensor id or
   reading type, the server return a 404 HTTP error code and an error
   message.

## Requirements

The server was built and tested for Python 3. In addition to the
standard Python modules the packages `Flask` and `Flask-RESTful` are
required.

## Running the Server

The server comes with two shell scripts for running it, one for
running it in development mode and one for production mode. Both
scripts need to be run from the parent directory of the
`sensor_server` directory (which contains these scripts).

Notes that these scripts assume the existing of a virtual environment
with the required modules installed.

In the following sections it is assumed that the system is installed
in a directory `<root-dir>`.

### Initializing the Database

Activate the virtual environment, then, from `<root-dir>`, run the
command

    FLASK_APP=sensor_server flask init-db

### Running in Development Mode

Use the command

    $ ./sensor_server/run_sensor_server_dev

The virtual environment should be `<root-dir>/venv_dev`.

### Running in Production Mode

There are different ways to choose from for deploying and running the
system in production. However, an easy way to do that is to use the
`waitress` Python WSGI server.

If you want to go that way, create a virtual environment
`<root-dir>/venv`, and install in it the packages `Flask`,
`Flask-RESTful` and `waitress`.

Then, from `<root-dir>`, run the command

    $ ./sensor_server/run_sensor_server

The server will start on port 8080.
