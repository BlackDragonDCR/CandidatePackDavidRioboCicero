FROM nginx:alpine
COPY frontend/index.html /usr/share/nginx/html/index.html
COPY frontend/nginx/default.conf /etc/nginx/conf.d/default.conf

COPY frontend/script.js /usr/share/nginx/html/script.js
COPY frontend/styles.css /usr/share/nginx/html/styles.css

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]