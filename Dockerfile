FROM python:3.7

LABEL maintainer="amit.ramon@gmail.com"

# main app dir
RUN mkdir /sensor_server_app

# sqlite3 database dir
RUN mkdir /sensor_server_app/instance

# copy application files
COPY sensor_server /sensor_server_app/sensor_server

# pip requirements file
COPY requirements.txt /sensor_server_app

# bootstrap script
COPY bin/run_app.sh /sensor_server_app

# install python packages
RUN pip install -r /sensor_server_app/requirements.txt

# allow mapping database directory to host
VOLUME ["/sensor_server_app/instance"]
# allow mapping this port to host
EXPOSE 8080

WORKDIR /sensor_server_app

ENTRYPOINT ./run_app.sh




