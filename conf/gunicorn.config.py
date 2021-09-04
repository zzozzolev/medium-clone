# reference: https://docs.gunicorn.org/en/stable/settings.html#config

wsgi_app = "apps.wsgi:application"
bind = "0.0.0.0:8000"
workers = 1
