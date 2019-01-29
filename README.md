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

## Server API Summary

This section describes briefly the URLs for accessing the server.

* `/add/`: add a new sensor reading entry. The data should be provided
  in the request's POST data. For more details see the following
  sections.
  
* `/`: list all stored sensor readings.

* `/sensors/`: list the distinct IDs of all stored sensors.

* `/sensors/<sensor_id>`: list all sensor readings for the
  given sensor.

* `/types/`: list the distinct types of all stored sensors.

* `/types/<reading-type>`: list all sensor reading that
  have the given reading type.

## Server API

The following sections describe the server API in details.

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

### Getting all Sensor Readings

Accessing the server's root URL will return a list of all stored
reading entries, in ascending timestamp order.

`curl` example:

    $ curl http://www.example.com/

### Getting Available Sensor Ids

Use the following URL to obtain a list of all sensor Ids that exist in
the server's database

    /sensors/

The results are in ascending numerical order.

### Getting Sensor Readings by Sensor Id

Use the following URL to obtain a list of all reading for the given
sensor.

    /sensors/<sensor_id>

The results are in ascending timestamp order. If the given Id dose not
exist in the database a 404 error is returned.
 
`curl` example:

    $ curl http://www.example.com/sensors/42
	
This return a list of all reading of the sensor identified by 42.
	
### Getting Available Reading Types

Use the following URL to obtain a list of all reading types that exist
in the server's database

	/types/

The results are in ascending alphabetical order.

### Getting Sensor Readings by Reading Type

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

## Building and Running a Docker Container

The system is ready for packing it in a Docker container. To build a
container run the following command from `<root-dir>`:

    $ docker-compose build

You will then be able to run it with:

    $ docker-compose up

The system's default configuration maps the service's port to port
*8080* on the host, and the `sqlite3` database directory will be mapped
to a local directory named `server_instance`.

## Running the Server Locally

The server comes with two shell scripts for running it, one for
running it in development mode and one for production mode. Both
scripts need to be run from the parent directory of the
`sensor_server` directory (which contains these scripts).

Notes that these scripts assume the existing of a virtual environment
with the required modules installed.

In the following sections it is assumed that the system is installed
in a directory `<root-dir>`.

### Initializing a Local Database

Use the command

    $ ./bin/init_db

The database will be created in a directory named `instance` in the
current directory.

Note: if you run this command when a database already exists it will
be completely cleared. Use caution!

### Running in Development Mode

Use the command

    $ ./bin/run_sensor_server_dev

The virtual environment should be `<root-dir>/venv_dev`.

### Testing Production Mode

In production mode the system uses the **Waitress WSGI** server. You can
run it locally in that mode for testing the configuration.

You will first have to create a virtual environment
`<root-dir>/venv`, and install in it the packages listed in the
`requirements.txt` file.

Then, from `<root-dir>`, run the command

    $ ./bin/run_sensor_server

The server will start on port 8080.

## License

This project is released under GNU General Public License v3.0.
