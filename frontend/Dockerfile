FROM nginx

COPY dist/ /etc/nginx/html/generate
# COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-1.conf /etc/nginx/conf.d/a.conf
COPY proxy_params /etc/nginx/proxy_params