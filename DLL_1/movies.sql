-- PART 1

------------------------------------------------------- Relations ----------------------------------------------------------
CREATE TABLE movie (
    movie_id SERIAL PRIMARY KEY, -- integer auto increment
    tmdb_id VARCHAR(20) UNIQUE NOT NULL, -- required -> NOT NULL
    imdb_id VARCHAR(20) UNIQUE, -- not required
    title VARCHAR(255) NOT NULL,
    plot TEXT,
    content_rating_id INT REFERENCES content_rating(content_rating_id), -- FK to content_rating
    viewers_rating NUMERIC(3, 1) CHECK (viewers_rating BETWEEN 0 AND 10), -- apply the range condition
    release_year INT,
    watchmode_id VARCHAR(20) -- may or may not be present
);

-- stores genres : comedy, drama etc. - foreign table 1 
CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- foreign table 2
CREATE TABLE content_rating (
    content_rating_id SERIAL PRIMARY KEY,
    rating VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE actor (
    actor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE director (
    director_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL, -- full country name 
    country_code CHAR(2) NOT NULL UNIQUE -- short code for countries
);

-- Watchmode Table 
CREATE TABLE watchmode (
    watchmode_id SERIAL PRIMARY KEY,
    platform_name VARCHAR(100) NOT NULL, -- e.g., Netflix, Hulu, etc.
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE -- FK to movies
);


----------------------------------------------------- Relationships ----------------------------------------------------------

CREATE TABLE movie_genre (
    movie_id INT REFERENCES movie(movie_id), -- referential integrity
    genre_id INT REFERENCES genre(genre_id), -- referential integrity
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE movie_keyword (
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    keyword_id INT REFERENCES keyword(keyword_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, keyword_id)
);

CREATE TABLE movie_actor (
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    actor_id INT REFERENCES actor(actor_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, actor_id)
);

CREATE TABLE movie_director (
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    director_id INT REFERENCES director(director_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, director_id)
);

CREATE TABLE movie_country (
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    country_id INT REFERENCES country(country_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, country_id)
);
