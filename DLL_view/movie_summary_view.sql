CREATE VIEW movie_summary AS
SELECT
    m.tmdb_id,
    m.imdb_id,
    m.title,
    m.plot,
    cr.rating AS content_rating, -- in content_rating 
    m.runtime,
    -- Count the number of keywords related to the movie
    (SELECT COUNT(*) FROM movie_keyword mk WHERE mk.movie_id = m.movie_id) AS num_keywords,
    -- Count the number of countries related to the movie
    (SELECT COUNT(*) FROM movie_country mc WHERE mc.movie_id = m.movie_id) AS num_countries
FROM
    movie m
    -- Join with content_rating table to get the rating
    LEFT JOIN movie_content_rating mcr ON m.movie_id = mcr.movie_id
    LEFT JOIN content_rating cr ON mcr.content_rating_id = cr.content_rating_id;
