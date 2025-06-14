CREATE TABLE IF NOT EXISTS urls (
    id serial CONSTRAINT urls_pk PRIMARY KEY,
    name varchar NOT NULL CONSTRAINT urls_uq UNIQUE,
    created_at timestamp with time zone NOT NULL DEFAULT now()
);

ALTER TABLE urls OWNER TO page_analyzer_admin;
