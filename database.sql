DROP TABLE IF EXISTS urls;
CREATE TABLE urls(
id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
name varchar(255) NOT NULL,
created_at date NOT NULL
);
DROP TABLE IF EXISTS urls_checks;
CREATE TABLE urls_checks(
id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
url_id bigint REFERENCES urls (id),
response_code int,
h1 varchar(255),
title varchar(255),
description varchar(255),
created_at date NOT NULL
);