--@ init none
SET search_path TO animalfarm, public;

--@ ready one
SELECT EXISTS (SELECT * FROM pg_namespace WHERE nspname = 'animalfarm');

--@ make_tables none
CREATE SCHEMA IF NOT EXISTS animalfarm;

SET LOCAL search_path TO animalfarm, public;

CREATE TABLE IF NOT EXISTS animal (
  id            uuid PRIMARY KEY NOT NULL,
  responds_to   text NOT NULL,
  kind          text NOT NULL,
  pig           boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS farm (
  farm          uuid PRIMARY KEY NOT NULL,
  name          text UNIQUE NOT NULL,
  location      polygon NOT NULL
);

CREATE TABLE IF NOT EXISTS "animal*farm" (
  animal        uuid NOT NULL REFERENCES animal
                              ON DELETE CASCADE ON UPDATE CASCADE
                              DEFERRABLE INITIALLY DEFERRED,
  farm          uuid NOT NULL REFERENCES farm
                              ON DELETE CASCADE ON UPDATE CASCADE
                              DEFERRABLE INITIALLY DEFERRED,
  t             timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (animal, farm)
);


--@ get_farm one? ro
SELECT * FROM farm WHERE name = %(farm)s;

--@ farms ro
SELECT * FROM farm;

--@ new_farm one
INSERT INTO farm (name, location) VALUES (%(farm)s, %(poly)s)
  RETURNING farm;

--@ new_animal one
WITH _(animal) AS (INSERT INTO animal (responds_to, kind, pig)
                    VALUES (%(responds_to)s, %(kind)s, %(pig)s
                 RETURNING animal),
     __(farm) AS (SELECT farm FROM farm WHERE name = %(farm)s)
INSERT INTO "animal*farm" (animal, farm) SELECT * FROM _ CROSS JOIN __
  RETURNING animal, farm;

--@ server_time one ro
SELECT * FROM now();
