FROM nginx:1.20.2-alpine

COPY ./configs/default.conf /etc/nginx/conf.d/default.conf
COPY ./configs/uwsgi_params /etc/nginx/uwsgi_params
COPY ./configs/nginx.conf /etc/nginx/nginx.conf
COPY ./configs/stream.conf /etc/nginx/stream.conf

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static
