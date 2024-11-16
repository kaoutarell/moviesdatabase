-- Find the number of movies that are in more than one language.

SELECT COUNT(DISTINCT m1.movie_id)
FROM movie_language m1
JOIN movie_language m2 -- SELF JOIN ON THE SAME TABLE
    ON m1.movie_id = m2.movie_id
    AND m1.language_id <> m2.language_id;


-- Expected result : 10