#!/bin/bash

if pgrep -u root -x "python" > /dev/null
then
	echo "Running"
else
	echo "Failed to find webserver"
	echo "Trying to restart"
	echo date
	sudo FLASK_APP=/home/pi/raspi_neopixel_lights/web/main.py python -m flask run --host=0.0.0.0 &>> /home/pi/raspi_neopixel_lights/web/flask_log &
fi
