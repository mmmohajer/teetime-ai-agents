FROM node:18.20.4-alpine3.20
LABEL Developer = "Moahammad Mahdi Mohajer"

WORKDIR /usr/src/app

COPY ./package.json .
RUN npm install


COPY . .
RUN npm run build

EXPOSE 3000

RUN addgroup app && adduser -SG app app
RUN chown -R app:app .
USER app