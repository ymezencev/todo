command = '/home/www/code/todo/env/bin/gunicorn'
pythonpath = '/home/www/code/todo/src'
bind = '127.0.0.1:8001'
workers = 3
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings'
