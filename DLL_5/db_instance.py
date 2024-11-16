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
        content_rating VARCHAR(10),
        viewers_rating DECIMAL(3, 1),
        release_year INT,
        imdb_id VARCHAR(20) UNIQUE, -- New column for IMDb ID (VARCHAR to store the IMDb ID / optional might be empty for some records)
        tmdb_id VARCHAR(20) UNIQUE NOT NULL   
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
        country_code VARCHAR(10) -- New column for country code (can store 2 or 3 character country codes)
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

# Create the AKAs (Alternative Titles) table
cur.execute("""
    CREATE TABLE IF NOT EXISTS aka (
        aka_id SERIAL PRIMARY KEY,
        movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
        title VARCHAR(255),
        country VARCHAR(10)
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


# test insertion -- alles gute
def insert_movie(title, plot, content_rating, viewers_rating, release_year, imdb_id, tmdb_id):
    cur.execute(
        """
        INSERT INTO movie (title, plot, content_rating, viewers_rating, release_year, imdb_id, tmdb_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING movie_id;
        """,
        (title, plot, content_rating, viewers_rating, release_year, imdb_id, tmdb_id)
    )
    conn.commit()
    movie_id = cur.fetchone()[0]  # Retrieve the inserted movie ID
    return movie_id

movie_id = insert_movie(
    "Spider-Man : New home",
    "An upcoming superhero film based on the Marvel Comics character Spider-Man",
    "SP-13",
    10.0,
    2024,
    "tt1234567",
    "tm9876543"
)

# closing the connection
cur.close()
conn.close()



## How to reset postgres tables for tests:
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
# GRANT ALL ON SCHEMA public TO postgres;
# GRANT ALL ON SCHEMA public TO public;
