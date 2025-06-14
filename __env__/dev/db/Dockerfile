FROM postgres:16

ENV POSTGRES_PASSWORD postgres

WORKDIR /docker-entrypoint-initdb.d/

COPY __env__/dev/db/init.sql .
COPY database.sql include/
