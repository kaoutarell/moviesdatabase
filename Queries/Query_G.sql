-- BATCH UPDATE -> updating in bulk
-- rounds up all the ratings.

UPDATE movie
SET viewers_rating = CEIL(viewers_rating); -- CEIL func to round + no condition since it's bulk update
