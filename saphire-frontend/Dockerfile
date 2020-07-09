FROM node:13.12.0-alpine

WORKDIR /saphire-frontend

ENV PATH /saphire-frontend/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN yarn install --silent
RUN yarn global add react-scripts@3.4.1 --silent

COPY . ./

#CMD ["yarn", "start"]