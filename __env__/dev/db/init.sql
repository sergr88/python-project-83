ALTER SYSTEM SET LOG_TIMEZONE = 'Europe/Moscow';

CREATE USER page_analyzer_admin PASSWORD 'pa';

CREATE DATABASE page_analyzer OWNER page_analyzer_admin;
ALTER DATABASE page_analyzer SET log_statement = 'all';

\connect page_analyzer page_analyzer_admin
\include /docker-entrypoint-initdb.d/include/database.sql
