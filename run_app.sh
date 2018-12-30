#!/bin/bash

ROOT_DIR=/sensor_server_app
DB_DIR=$ROOT_DIR/instance
DB_FILE=$DB_DIR/sensors.sqlite

FLASK=/usr/local/bin/flask
WAITRESS=/usr/local/bin/waitress-serve

PORT=8080
export FLASK_APP=sensor_server

cd $ROOT_DIR

# if database does not exist, initialize it
[[ -f $DB_DIR/sensors.sqlite ]] || $FLASK init-db

# start the server
$WAITRESS --port $PORT --call $FLASK_APP:create_app
