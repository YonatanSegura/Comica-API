--
-- File generated with SQLiteStudio v3.2.1 on lu. ago. 12 23:19:26 2019
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: auth_user
CREATE TABLE auth_user (
    id           INTEGER       NOT NULL
                               PRIMARY KEY AUTOINCREMENT,
    password     VARCHAR (128) NOT NULL,
    last_login   DATETIME,
    is_superuser BOOL          NOT NULL,
    username     VARCHAR (150) NOT NULL
                               UNIQUE,
    first_name   VARCHAR (30)  NOT NULL,
    email        VARCHAR (254) NOT NULL,
    is_staff     BOOL          NOT NULL,
    is_active    BOOL          NOT NULL,
    date_joined  DATETIME      NOT NULL,
    last_name    VARCHAR (150) NOT NULL
);


-- Table: comics_comic
CREATE TABLE comics_comic (
    id          INTEGER       NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    uuid        VARCHAR (36)  NOT NULL
                              UNIQUE,
    comic       VARCHAR (64)  NOT NULL,
    author      VARCHAR (64)  NOT NULL,
    url         TEXT          NOT NULL,
    description VARCHAR (512) NOT NULL,
    rewards     DECIMAL       NOT NULL,
    created_by  DATETIME      NOT NULL,
    state       SMALLINT      NOT NULL
);


-- Table: comics_comicsurl
CREATE TABLE comics_comicsurl (
    id         INTEGER      NOT NULL
                            PRIMARY KEY AUTOINCREMENT,
    uuid       VARCHAR (36) NOT NULL
                            UNIQUE,
    url        TEXT         NOT NULL,
    [index]    SMALLINT     NOT NULL,
    created_by DATETIME     NOT NULL,
    state      SMALLINT     NOT NULL,
    comic_id   INTEGER      NOT NULL
                            REFERENCES comics_comic (id) DEFERRABLE INITIALLY DEFERRED
);


-- Table: users_profile
CREATE TABLE users_profile (
    id          INTEGER       NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    uuid        VARCHAR (36)  NOT NULL,
    name        VARCHAR (85)  NOT NULL,
    description VARCHAR (500),
    user_id     INTEGER       NOT NULL
                              REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
);


-- Index: comics_comicsurl_comic_id_7226d2a2
CREATE INDEX comics_comicsurl_comic_id_7226d2a2 ON comics_comicsurl (
    "comic_id"
);


-- Index: users_profile_user_id_2112e78d
CREATE INDEX users_profile_user_id_2112e78d ON users_profile (
    "user_id"
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
