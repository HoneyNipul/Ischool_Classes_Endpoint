FROM postgres:latest
MAINTAINER Nick Lyga

ENV POSTGRES_PASSWORD ischooldev
ENV POSTGRES_USER ischooldevdbuser
ENV POSTGRES_DB dev_project

ADD create_extension.sh docker-entrypoint-initdb.d/create_extension.sh
