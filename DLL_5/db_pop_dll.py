import requests  # type: ignore
import psycopg2  # type: ignore
import random  # type: ignore
from psycopg2 import sql  # type: ignore
from faker import Faker # type: ignore

# Define the base URLs and API key
api_key = "d3967d088d5c2e4baa702cf128358a62"
discover_url = "https://api.themoviedb.org/3/discover/movie"
movie_details_url = "https://api.themoviedb.org/3/movie/{}"
genres_url = "https://api.themoviedb.org/3/genre/movie/list"
watchmode_url = "https://api.watchmode.com/v1/api/"
content_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17', 'R']
watch_modes = ['SD', 'HD', '4K', 'HDR', 'Dolby', 'Rent', 'Buy', 'Free', 'Interactive', 'On-demand']

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="movies_db",
    user="kel",
    password="soen363",
    host="localhost",
    port="5431"
)
cur = conn.cursor()


# -------- Insert reviews in reviews table -- generated randomly

fake = Faker()
# Function to generate random review data
def generate_random_review():
    # Generate a random rating
    rating = round(random.uniform(1.0, 10.0), 1)
    content = fake.text(max_nb_chars=200)  # Generate random review content
    return rating, content

for _ in range(100):
    rating, content = generate_random_review()
    insert_query = """
    INSERT INTO review (viewer_rating, review_content)
    VALUES (%s, %s);
    """
    cur.execute(insert_query, (rating, content))

# ---------- Insert watch modes into the watchmode table if they don't already exist
def insert_watch_modes():
    for wname in watch_modes:
        cur.execute("""
            INSERT INTO watchmode (wname)
            VALUES (%s)
            ON CONFLICT (wname) DO NOTHING;
        """, (wname,))
    conn.commit()
insert_watch_modes()


# Fetch and insert genres
def fetch_and_insert_genres():
    response = requests.get(genres_url, params={"api_key": api_key, "language": "en-US"})
    if response.status_code == 200:
        genres_data = response.json().get('genres', [])
        for genre in genres_data:
            genre_id = genre['id']
            genre_name = genre['name']
            cur.execute("""
                INSERT INTO genre (genre_id, name)
                VALUES (%s, %s)
                ON CONFLICT (genre_id) DO NOTHING;
            """, (genre_id, genre_name))
        conn.commit()
    else:
        print(f"Failed to fetch genres: {response.status_code}")

# Insert data into tables with conflict handling
def insert_if_not_exists(table, columns, values):
    placeholders = ", ".join(["%s"] * len(values))
    column_names = ", ".join(columns)
    cur.execute(
        f"INSERT INTO {table} ({column_names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;",
        values
    )

def generate_random_imdb_id():
    # Randomly generate an imdb_id in the format tt########
    return "tt" + str(random.randint(1000000, 9999999))

def generate_random_tmdb_id(existing_ids): # Random tmdb_id in the format tm########
    while True:
        tmdb_id = "tm" + str(random.randint(1000000, 9999999))
        if tmdb_id not in existing_ids:
            existing_ids.add(tmdb_id)
            return tmdb_id

# Fetch and insert movies and related data
def fetch_and_insert_movies(min_movies=50):
    page = 1
    total_movies_inserted = 0

    existing_tmdb_ids = set()

    # Fetch all existing tmdb_ids to avoid duplicates
    cur.execute("SELECT tmdb_id FROM movie WHERE tmdb_id IS NOT NULL")
    for row in cur.fetchall():
        existing_tmdb_ids.add(row[0])

    while total_movies_inserted < min_movies:
        params = {
            "api_key": api_key,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": page
        }
        response = requests.get(discover_url, params=params)
        if response.status_code == 200:
            movies_data = response.json().get('results', [])
            if not movies_data:
                print("No more movies to fetch.")
                break

            for movie in movies_data:
                title = movie.get('title')
                plot = movie.get('overview')
                content_rating = movie.get('content_rating', random.choice(content_ratings))
                viewers_rating = movie.get('vote_average', 0.0)
                release_date = movie.get('release_date', "0000-00-00")
                release_year = int(release_date.split('-')[0]) if release_date else None

                # Generate unique tmdb_id -> UNIQUE FIELD
                tmdb_id = generate_random_tmdb_id(existing_tmdb_ids)

                # Generate a random IMDB ID
                imdb_id = None
                if random.random() > 0.5:  # 50% chance to assign a random imdb_id
                    imdb_id = generate_random_imdb_id()

                # Insert movie into movie table
                if imdb_id:
                    cur.execute("""
                        INSERT INTO movie (title, plot, release_year, imdb_id, tmdb_id)
                        VALUES (%s, %s, %s, %s, %s) RETURNING movie_id;
                    """, (title, plot, release_year, imdb_id, tmdb_id))
                else:
                    cur.execute("""
                        INSERT INTO movie (title, plot, release_year, tmdb_id)
                        VALUES (%s, %s, %s, %s) RETURNING movie_id;
                    """, (title, plot, release_year, tmdb_id))

                movie_id = cur.fetchone()[0]

                # Insert genres for the movie
                genre_ids = movie.get('genre_ids', [])
                for genre_id in genre_ids:
                    cur.execute("""
                        INSERT INTO movie_genre (movie_id, genre_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING;
                    """, (movie_id, genre_id))

                if content_rating:
                    # Check if the content rating exists in the content_rating table
                    cur.execute("""
                        SELECT content_rating_id FROM content_rating WHERE rating = %s;
                    """, (content_rating,))
                    result = cur.fetchone()

                    # If no content_rating_id is found, insert the new content rating into the table
                    if result is None:
                        cur.execute("""
                            INSERT INTO content_rating (rating) VALUES (%s) RETURNING content_rating_id;
                        """, (content_rating,))
                        content_rating_id = cur.fetchone()[0]  # Get the newly inserted content_rating_id
                    else:
                        content_rating_id = result[0]  # Use the existing content_rating_id

                    # Insert the content rating and movie association into the content_rating_review table
                    cur.execute("""
                        INSERT INTO movie_content_rating (movie_id, content_rating_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING;
                    """, (movie_id, content_rating_id))

                # Fetch and insert movie details (e.g., actors, directors, countries)
                fetch_and_insert_movie_details(movie_id, movie['id'])

                total_movies_inserted += 1
                if total_movies_inserted >= min_movies:
                    break

            page += 1
            conn.commit()
        else:
            print(f"Failed to fetch movies on page {page}: {response.status_code}")
            break

# Fetch and insert movie details (actors, directors, countries, languages, keywords, AKAs)
def fetch_and_insert_movie_details(movie_id, tmdb_movie_id):
    details_response = requests.get(movie_details_url.format(tmdb_movie_id), params={"api_key": api_key, "append_to_response": "credits,keywords,releases,translations"})
    if details_response.status_code == 200:
        details = details_response.json()

        # Insert actors
        for actor in details['credits']['cast'][:10]:  # Limit to top 10 cast members
            insert_if_not_exists("actor", ["name"], [actor['name']])
            cur.execute("SELECT actor_id FROM actor WHERE name = %s", (actor['name'],))
            actor_id = cur.fetchone()[0]
            cur.execute("INSERT INTO movie_actor (movie_id, actor_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, actor_id))

        # Insert directors
        for crew in details['credits']['crew']:
            if crew['job'] == 'Director':
                insert_if_not_exists("director", ["name"], [crew['name']])
                cur.execute("SELECT director_id FROM director WHERE name = %s", (crew['name'],))
                director_id = cur.fetchone()[0]
                cur.execute("INSERT INTO movie_director (movie_id, director_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, director_id))

        # Insert countries and country codes
        for country in details.get('production_countries', []):
            insert_if_not_exists("country", ["name", "country_code"], [country['name'], country['iso_3166_1']])
            cur.execute("SELECT country_id FROM country WHERE name = %s AND country_code = %s", (country['name'], country['iso_3166_1']))
            country_id = cur.fetchone()[0]
            cur.execute("INSERT INTO movie_country (movie_id, country_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, country_id))

        # Insert languages
        for language in details.get('spoken_languages', []):
            insert_if_not_exists("language_", ["name"], [language['name']])
            cur.execute("SELECT language_id FROM language_ WHERE name = %s", (language['name'],))
            language_id = cur.fetchone()[0]
            cur.execute("INSERT INTO movie_language (movie_id, language_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, language_id))

        # Insert keywords
        for keyword in details['keywords']['keywords']:
            insert_if_not_exists("keyword", ["name"], [keyword['name']])
            cur.execute("SELECT keyword_id FROM keyword WHERE name = %s", (keyword['name'],))
            keyword_id = cur.fetchone()[0]
            cur.execute("INSERT INTO movie_keyword (movie_id, keyword_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, keyword_id))

        # Insert AKAs (Alternative Titles)
        for aka in details.get('translations', {}).get('translations', []):
            title = aka.get('title')
            country = aka.get('iso_3166_1')
            if title:
                cur.execute("""
                    INSERT INTO aka (movie_id, title, country)
                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
                """, (movie_id, title, country))

        conn.commit()
    else:
        print(f"Failed to fetch details for movie {tmdb_movie_id}: {details_response.status_code}")

# Run functions to fetch and insert data
fetch_and_insert_genres()
fetch_and_insert_movies(min_movies=50)

# Close the connection
cur.close()
conn.close()
print("Data insertion complete.")
