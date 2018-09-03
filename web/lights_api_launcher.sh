#!/bin/bash

if pgrep -u root -x "python" > /dev/null
then
	echo "Running"
else
	sudo FLASK_APP=main.py python -m flask run --host=0.0.0.0
fi
