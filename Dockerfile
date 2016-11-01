FROM python:3-alpine

MAINTAINER Mike Chaliy

RUN set -ex \
	&& apk add --no-cache \
    alpine-sdk

ADD . /app
RUN set -ex \
  && cd /app \
  && pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8080
CMD ["python", "/app/app.py"]
