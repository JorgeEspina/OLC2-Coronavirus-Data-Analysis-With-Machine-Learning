FROM nginx:alpine

LABEL author="Jorge Espina" 

# Copy custom nginx config
COPY ./.docker/nginx.conf /etc/nginx/nginx.conf
COPY ./dist/dashboard /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]

