FROM node:16-alpine3.14

COPY / /app

RUN cd /app \
    && npm install

WORKDIR /app

EXPOSE 3000

ENTRYPOINT npm start
