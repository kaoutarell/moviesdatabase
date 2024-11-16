-- PART 1

--------------------------------- Relations --------------------------------------

CREATE TABLE IF NOT EXISTS movie (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        plot TEXT,
        release_year INT,
        runtime VARCHAR(20),
        imdb_id VARCHAR(20) UNIQUE, -- New column for IMDb ID (VARCHAR to store the IMDb ID / optional might be empty for some records)
        tmdb_id VARCHAR(20) UNIQUE NOT NULL   
    );

CREATE TABLE IF NOT EXISTS watchmode (
        watchmode_id SERIAL PRIMARY KEY,
        wname VARCHAR(100) NOT NULL,
        CONSTRAINT watchmode_wname_unique UNIQUE (wname) 
    );
CREATE TABLE IF NOT EXISTS review (
        review_id SERIAL PRIMARY KEY,
        viewer_rating NUMERIC(3, 1),  -- Viewer rating as a numeric value
        review_content TEXT
    );

CREATE TABLE IF NOT EXISTS content_rating (
        content_rating_id SERIAL PRIMARY KEY,
        rating VARCHAR(10) NOT NULL  -- E.g., PG, PG-13, R, etc.
    );

CREATE TABLE IF NOT EXISTS genre (
        genre_id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );

CREATE TABLE IF NOT EXISTS actor (
        actor_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );

CREATE TABLE IF NOT EXISTS director (
        director_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );

CREATE TABLE IF NOT EXISTS country (
        country_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        country_code VARCHAR(10) -- New column for country code (can store 2 or 3 character country codes)
    );

CREATE TABLE IF NOT EXISTS keyword (
        keyword_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );

CREATE TABLE IF NOT EXISTS language_ (
        language_id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );

CREATE TABLE IF NOT EXISTS aka (
        aka_id SERIAL PRIMARY KEY,
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        title VARCHAR(255),
        country VARCHAR(10)
    );

---------------------------------- Relationships -------------------------------------
CREATE TABLE IF NOT EXISTS movie_watchmode (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        watchmode_id INT REFERENCES watchmode(watchmode_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, watchmode_id)
    );

CREATE TABLE IF NOT EXISTS movie_review (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        review_id INT REFERENCES review(review_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, review_id)
    );

CREATE TABLE IF NOT EXISTS movie_content_rating (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        content_rating_id INT REFERENCES content_rating(content_rating_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, content_rating_id)
    );


CREATE TABLE IF NOT EXISTS movie_genre (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        genre_id INT REFERENCES genre(genre_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, genre_id)
    );


CREATE TABLE IF NOT EXISTS movie_actor (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        actor_id INT REFERENCES actor(actor_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, actor_id)
    );


CREATE TABLE IF NOT EXISTS movie_director (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        director_id INT REFERENCES director(director_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, director_id)
    );


CREATE TABLE IF NOT EXISTS movie_country (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        country_id INT REFERENCES country(country_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, country_id)
    );


CREATE TABLE IF NOT EXISTS movie_language (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        language_id INT REFERENCES language_(language_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, language_id)
    );


CREATE TABLE IF NOT EXISTS movie_keyword (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        keyword_id INT REFERENCES keyword(keyword_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, keyword_id)
    );


