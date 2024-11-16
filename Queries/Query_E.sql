-- For each language list how many movies are there in the database. Order by highest rank.

SELECT 
    l.name AS language,
    COUNT(m.movie_id) AS number_of_movies
FROM language_ l
JOIN movie_language ml ON l.language_id = ml.language_id
JOIN movie m ON ml.movie_id = m.movie_id
GROUP BY l.language_id -- Necessary for the count grouping
ORDER BY number_of_movies DESC; -- highest rank to lowest -> descendant ordering

