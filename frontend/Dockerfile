FROM node:latest

RUN mkdir /crawler-front
WORKDIR /crawler-front
COPY . /crawler-front/

RUN apt-get -y update
RUN npm install

EXPOSE 3000:3000

CMD [ "npm", "start" ]