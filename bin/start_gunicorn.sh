#!/bin/bash
source /home/www/code/todo/env/bin/activate
exec gunicorn -c "/home/www/code/todo/src/gunicorn_config.py" config.wsgi
