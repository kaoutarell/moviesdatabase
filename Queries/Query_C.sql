-- Find movies that have highest number of reviews. 
-- List top 3.


SELECT m.title, COUNT(mr.review_id) AS review_count
FROM movie m
JOIN movie_review mr ON m.movie_id = mr.movie_id
GROUP BY m.movie_id
ORDER BY review_count DESC
LIMIT 3;

-- Gives 3 results given the data we have