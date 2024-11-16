-- Find the total number of movies with and without IMDB id in the database.
-- Use one query.

SELECT 
    COUNT(CASE WHEN imdb_id IS NOT NULL THEN 1 END) AS with_imdb_id,
    COUNT(CASE WHEN imdb_id IS NULL THEN 1 END) AS without_imdb_id
FROM movie;


-- Expected result is : 20 with and 30 without (given the data we have)