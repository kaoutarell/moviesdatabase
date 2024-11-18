-- Pick an actor -> id:1 / name: Tom Hardy given our data
-- Find all movies by that actor that is released between 2000 and 2020. 
-- List TMDB-id, IMDB-id, movie title, release date, and watchmode-id.

SELECT 
    m.tmdb_id, 
    m.imdb_id, 
    m.title, 
    m.release_year, 
    wm.watchmode_id
FROM 
    actor a
JOIN 
    movie_actor ma ON a.actor_id = ma.actor_id
JOIN 
    movie m ON ma.movie_id = m.movie_id
JOIN 
    movie_watchmode mw ON m.movie_id = mw.movie_id
JOIN 
    watchmode wm ON mw.watchmode_id = wm.watchmode_id
WHERE 
    a.actor_id = 1 -- Actor chosen : Tom Hardy
    AND m.release_year BETWEEN 2000 AND 2020;


-- Query shows 2 results 