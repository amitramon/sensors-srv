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

"""Constants and variables common to Sensor Server modules."""

# Constants used for describing data key names (in REST requests and
# in JSON data).
SENSOR_ID_KEY = 'sensor-id'
READING_TYPE_KEY = 'reading-type'
VALUE_KEY = 'value'
TIMESTAMP_KEY = 'timestamp'
READINGS_LIST_KEY = 'sensor-readings'
