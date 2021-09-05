FROM nginx:1.20.1

COPY conf/nginx/default.conf /etc/nginx/conf.d/default.conf
# You must run `python3 manage.py collectstatic` first, if you don't have `static` directory.
COPY static /data/static