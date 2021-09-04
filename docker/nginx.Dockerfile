FROM nginx:1.20.1

COPY conf/nginx/default.conf /etc/nginx/conf.d/default.conf
