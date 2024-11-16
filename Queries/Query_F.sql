-- Find top 2 comedies (higher ratings).

SELECT 
    m.title,
    m.viewers_rating
FROM movie m
JOIN movie_genre mg ON m.movie_id = mg.movie_id
JOIN genre g ON mg.genre_id = g.genre_id
WHERE g.name = 'Comedy'
ORDER BY m.viewers_rating DESC -- (highest first)
LIMIT 2; -- We only want 2