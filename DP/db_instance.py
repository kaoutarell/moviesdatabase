## ---------------------------------- PART 3 -----------------------------------------

import psycopg2 # type: ignore
from psycopg2 import sql # type: ignore

# connection to PostgreSQL database in Docker
conn = psycopg2.connect(
    dbname="movies_db",  # db name 
    user="kel",  # usrname
    password="soen363",  
    host="localhost",  
    port="5432"
)

cur = conn.cursor()

# db tables/relations to be created
cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        plot TEXT,
        content_rating VARCHAR(10),
        viewers_rating DECIMAL(3, 1),
        release_year INT
    );
""")

# Create the Genres table
cur.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        genre_id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );
""")

# Create the movie_genres table (many-to-many relationship between movies and genres)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_genres (
        movie_id INT REFERENCES movies(movie_id),
        genre_id INT REFERENCES genres(genre_id),
        PRIMARY KEY (movie_id, genre_id)
    );
""")

# Create the Actors table
cur.execute("""
    CREATE TABLE IF NOT EXISTS actors (
        actor_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_actors table (many-to-many relationship between movies and actors)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_actors (
        movie_id INT REFERENCES movies(movie_id),
        actor_id INT REFERENCES actors(actor_id),
        PRIMARY KEY (movie_id, actor_id)
    );
""")

# Create the Directors table
cur.execute("""
    CREATE TABLE IF NOT EXISTS directors (
        director_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_directors table (many-to-many relationship between movies and directors)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_directors (
        movie_id INT REFERENCES movies(movie_id),
        director_id INT REFERENCES directors(director_id),
        PRIMARY KEY (movie_id, director_id)
    );
""")

# Create the Countries table
cur.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        country_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_countries table (many-to-many relationship between movies and countries)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_countries (
        movie_id INT REFERENCES movies(movie_id),
        country_id INT REFERENCES countries(country_id),
        PRIMARY KEY (movie_id, country_id)
    );
""")

# Create the Languages table
cur.execute("""
    CREATE TABLE IF NOT EXISTS languages (
        language_id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );
""")

# Create the movie_languages table (many-to-many relationship between movies and languages)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_languages (
        movie_id INT REFERENCES movies(movie_id),
        language_id INT REFERENCES languages(language_id),
        PRIMARY KEY (movie_id, language_id)
    );
""")

# Create the Keywords table
cur.execute("""
    CREATE TABLE IF NOT EXISTS keywords (
        keyword_id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
""")

# Create the movie_keywords table (many-to-many relationship between movies and keywords)
cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_keywords (
        movie_id INT REFERENCES movies(movie_id),
        keyword_id INT REFERENCES keywords(keyword_id),
        PRIMARY KEY (movie_id, keyword_id)
    );
""")

# Create the AKAs (Alternative Titles) table
cur.execute("""
    CREATE TABLE IF NOT EXISTS akas (
        aka_id SERIAL PRIMARY KEY,
        movie_id INT REFERENCES movies(movie_id),
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
def insert_movie(title, plot, content_rating, viewers_rating, release_year):
    cur.execute(
        """
        INSERT INTO movies (title, plot, content_rating, viewers_rating, release_year)
        VALUES (%s, %s, %s, %s, %s) RETURNING movie_id;
        """,
        (title, plot, content_rating, viewers_rating, release_year)
    )
    conn.commit()
    movie_id = cur.fetchone()[0]  # Retrieve the inserted movie ID
    return movie_id

movie_id = insert_movie(
    "Spider-Man : New home",
    "An upcoming superhero film based on the Marvel Comics character Spider-Man",
    "SP-13",
    10.0,
    2024
)

# closing the connection
cur.close()
conn.close()
