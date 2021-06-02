#builder
FROM node:12.18.3-alpine3.9 as builder

WORKDIR /usr/src/app

COPY ./saphire-frontend/package.json .
RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++ \
    && npm install \
    && apk del .gyp

COPY ./saphire-frontend .

ARG API_SERVER
ENV REACT_APP_API_SERVER=${API_SERVER}
RUN REACT_APP_API_SERVER=${API_SERVER} \
    npm run build 

#final
FROM node:12.18.3-alpine3.9

WORKDIR /usr/src/app

RUN npm install -g serve

COPY --from=builder /usr/src/app/build ./build