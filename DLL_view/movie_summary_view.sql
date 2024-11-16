CREATE OR REPLACE VIEW movie_summary AS
SELECT 
    m.tmdb_id AS tmdb_key,
    m.imdb_id AS imdb_key,
    m.title,
    m.plot AS description,
    m.content_rating,
    COUNT(DISTINCT mk.keyword_id) AS number_of_keywords,
    COUNT(DISTINCT mc.country_id) AS number_of_countries
FROM 
    movie m
LEFT JOIN movie_keyword mk ON m.movie_id = mk.movie_id -- we want to return all rows from movies + for movies that do not have associated keywords or countries, NULL values will be used.
LEFT JOIN movie_country mc ON m.movie_id = mc.movie_id
GROUP BY 
    m.tmdb_id, m.imdb_id, m.title, m.plot, m.content_rating;