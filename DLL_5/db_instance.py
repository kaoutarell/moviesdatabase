import psycopg2 # type: ignore
from psycopg2 import sql # type: ignore

# connection to PostgreSQL database in Docker
conn = psycopg2.connect(
    dbname="movies_db",  # db name 
    user="kel",  # usrname
    password="soen363",  
    host="localhost",  
    port="5431"
)

cur = conn.cursor()

# db tables/relations to be created
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        plot TEXT,
        release_year INT,
        runtime VARCHAR(20),
        imdb_id VARCHAR(20) UNIQUE, -- New column for IMDb ID (VARCHAR to store the IMDb ID / optional might be empty for some records)
        tmdb_id VARCHAR(20) UNIQUE NOT NULL   
    );
""")

# Create the Watchmode table ---> MANY TO MANY CS A MOVIE CAN HAVE MORE THAN 1 WATCHMODE
cur.execute("""
    CREATE TABLE IF NOT EXISTS watchmode (
        watchmode_id SERIAL PRIMARY KEY,
        wname VARCHAR(100) NOT NULL,
        CONSTRAINT watchmode_wname_unique UNIQUE (wname) 
    );
""")

# Create the many-to-many relationship between movie and watchmode (movie_watchmode table)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_watchmode (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        watchmode_id INT REFERENCES watchmode(watchmode_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, watchmode_id)
    );
""")

# Create the Reviews table -- FOR THE QUERIES IN PART 7
cur.execute("""
    CREATE TABLE IF NOT EXISTS review (
        review_id SERIAL PRIMARY KEY,
        viewer_rating NUMERIC(3, 1),  -- Viewer rating as a numeric value
        review_content TEXT
    );
""")

# Create the many-to-many relationship between movie and review (movie_review table)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_review (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        review_id INT REFERENCES review(review_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, review_id)
    );
""")

# Create the Content Rating table -- should be in a separate table --> requirements
cur.execute("""
    CREATE TABLE IF NOT EXISTS content_rating (
        content_rating_id SERIAL PRIMARY KEY,
        rating VARCHAR(10) NOT NULL  -- E.g., PG, PG-13, R, etc.
    );
""")

# Create the many-to-many relationship between movie and content_rating (content_rating_review table)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_content_rating (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        content_rating_id INT REFERENCES content_rating(content_rating_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, content_rating_id)
    );
""")


# Create the Genres table
cur.execute("""
    CREATE TABLE IF NOT EXISTS genre (
        genre_id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );
""")

# Create the movie_genres table (many-to-many relationship between movies and genres)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_genre (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        genre_id INT REFERENCES genre(genre_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, genre_id)
    );
""")

# Create the Actors table
cur.execute("""
    CREATE TABLE IF NOT EXISTS actor (
        actor_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_actors table (many-to-many relationship between movies and actors)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_actor (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        actor_id INT REFERENCES actor(actor_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, actor_id)
    );
""")

# Create the Directors table
cur.execute("""
    CREATE TABLE IF NOT EXISTS director (
        director_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_directors table (many-to-many relationship between movies and directors)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_director (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        director_id INT REFERENCES director(director_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, director_id)
    );
""")

# Create the Countries table
cur.execute("""
    CREATE TABLE IF NOT EXISTS country (
        country_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        country_code VARCHAR(10) UNIQUE CHECK (length(country_code) BETWEEN 2 AND 3)  -- Constraint for 2 or 3 characters (requirements)
    );
""")

# Create the movie_countries table (many-to-many relationship between movies and countries)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_country (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        country_id INT REFERENCES country(country_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, country_id)
    );
""")

# Create the Languages table
cur.execute("""
    CREATE TABLE IF NOT EXISTS language_ (
        language_id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );
""")

# Create the movie_languages table (many-to-many relationship between movies and languages)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_language (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        language_id INT REFERENCES language_(language_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, language_id)
    );
""")

# Create the Keywords table
cur.execute("""
    CREATE TABLE IF NOT EXISTS keyword (
        keyword_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_keywords table (many-to-many relationship between movies and keywords)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_keyword (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        keyword_id INT REFERENCES keyword(keyword_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, keyword_id)
    );
""")

# Create the AKAs 
cur.execute("""
    CREATE TABLE IF NOT EXISTS aka (
        aka_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        country_id INT REFERENCES country(country_id) ON DELETE CASCADE ON UPDATE CASCADE
    );
""")

# Create the AKA movie relationship
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_aka (
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        aka_id INT REFERENCES aka(aka_id) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (movie_id, aka_id)
    );
""")

# commit changes 
conn.commit()
print("Schema created successfully.")


#no tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = cur.fetchall()
print(tables)

#DB connected ok
cur.execute("SELECT current_database();")
db_name = cur.fetchone()[0]
print(f"Connected to: {db_name}")


#ALLES GUTE -- test the connection : db + user
try:
    cur.execute("SELECT CURRENT_USER;")
    current_user = cur.fetchone()
    print(f"Connected as user: {current_user[0]}")
    
    # Run a simple test query
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    print(f"Simple query result: {result}")
except Exception as e:
    print(f"Error during simple query: {e}")


# closing the connection
cur.close()
conn.close()



## How to reset postgres tables for tests:
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
# GRANT ALL ON SCHEMA public TO postgres;
# GRANT ALL ON SCHEMA public TO public;
