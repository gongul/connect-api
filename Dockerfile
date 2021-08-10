FROM jfloff/alpine-python:3.8-slim

LABEL "maintainer"="gongul <projectgongul@gmail.com>"

# python 라이브러리에 필요한것들 
RUN apk add --no-cache python3-dev build-base linux-headers pcre-dev libffi-dev && \
    apk add --no-cache mariadb-connector-c-dev make && \
    apk add --no-cache jpeg-dev zlib-dev libmagic && \
    apk add --no-cache --virtual .build-deps && \
    apk add --no-cache tzdata \
    build-base \
    mariadb-dev 

# 컨테이너 날짜
ENV TZ=Asia/Seoul 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk del --no-cache --purge .build-deps && \
    rm -rf /var/cache/apk/* 

WORKDIR /connect/connection-api

ADD docker-requirements.txt ./requirements.txt
RUN pip install -q -r requirements.txt

ADD . ./

WORKDIR /connect/connection-api/src

RUN chmod a+x ./manage.py

CMD ["gunicorn common.wsgi.development:application --max-requests 1000 --max-requests-jitter 60 --bind 0.0.0.0:3000"]


