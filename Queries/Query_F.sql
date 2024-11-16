-- Find top 2 comedies (higher ratings).
-- ROUND is used to have only 1 decimal digit - without it, I get 6 digits

SELECT m.title, ROUND(AVG(r.viewer_rating), 1) AS avg_rating
FROM movie m
JOIN movie_genre mg ON m.movie_id = mg.movie_id
JOIN genre g ON mg.genre_id = g.genre_id
JOIN movie_review mr ON m.movie_id = mr.movie_id
JOIN review r ON mr.review_id = r.review_id
WHERE g.name = 'Comedy'
GROUP BY m.movie_id
ORDER BY avg_rating DESC
LIMIT 2;

-- Gives 2 results 