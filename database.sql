CREATE TABLE IF NOT EXISTS urls (
    id serial CONSTRAINT urls_pk PRIMARY KEY,
    name varchar NOT NULL CONSTRAINT urls_uq UNIQUE,
    created_at timestamp with time zone NOT NULL DEFAULT now()
);

ALTER TABLE urls OWNER TO page_analyzer_admin;

CREATE TABLE IF NOT EXISTS url_checks (
    id serial CONSTRAINT url_checks_pk PRIMARY KEY,
    url_id int NOT NULL REFERENCES urls,
    status_code int,
    h1 varchar,
    title varchar,
    description varchar,
    created_at timestamp with time zone NOT NULL DEFAULT now()
);

ALTER TABLE url_checks OWNER TO page_analyzer_admin;
