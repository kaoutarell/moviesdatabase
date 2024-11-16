-- BATCH UPDATE -> updating in bulk
-- rounds up all the ratings.

UPDATE review
SET viewer_rating = CEIL(viewer_rating); -- CEIL func to round + no condition since it's bulk update
