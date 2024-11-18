import requests  # type: ignore

# Defining the base URL and API key to TMDB
api_key = "d3967d088d5c2e4baa702cf128358a62"
discover_url = "https://api.themoviedb.org/3/discover/movie"  # movies
genres_url = "https://api.themoviedb.org/3/genre/movie/list"  # movies genres
movie_details_url = "https://api.themoviedb.org/3/movie"  # movie details (for cast & crew)

# Fetch the genre list first by ID
def get_genres():
    response = requests.get(genres_url, params={"api_key": api_key, "language": "en-US"})
    if response.status_code == 200:
        genres_data = response.json()
        return {genre['id']: genre['name'] for genre in genres_data['genres']}
    else:
        print(f"Failed to retrieve genres: {response.status_code}")
        return {}

# Fetch the movie data across multiple pages to get 50 movies -> each page holds only 20 records and we want to show at least 50
def get_movies():
    movies = []
    for page in range(1, 4):  # Fetch pages 1 to 3
        params = {
            "api_key": api_key,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": page
        }
        response = requests.get(discover_url, params=params)
        
        if response.status_code == 200:
            movies.extend(response.json()['results'])
            if len(movies) >= 20:  # If we have at least 20 movies -> BREAK | can be modified to show less or more
                break 
        else:
            print(f"Failed to retrieve movies from page {page}: {response.status_code}")
            break

    return movies[:20]  # Return the first 20 movies found

def get_movie_cast_and_crew(movie_id):
    """Fetches detailed cast and crew information for a movie."""
    response = requests.get(f"{movie_details_url}/{movie_id}/credits", params={"api_key": api_key})
    if response.status_code == 200:
        credits = response.json()
        cast = [member['name'] for member in credits.get('cast', [])]  # Full list of cast
        crew = credits.get('crew', [])
        directors = [member['name'] for member in crew if member['job'] == 'Director']
        return cast, directors
    else:
        print(f"Failed to retrieve cast and crew for movie ID {movie_id}: {response.status_code}")
        return [], []


def get_movie_keywords(movie_id):
    """Fetches keywords for a specific movie."""
    response = requests.get(f"{movie_details_url}/{movie_id}/keywords", params={"api_key": api_key})
    if response.status_code == 200:
        keywords = response.json().get('keywords', [])
        return [keyword['name'] for keyword in keywords]
    else:
        print(f"Failed to retrieve keywords for movie ID {movie_id}: {response.status_code}")
        return []


def get_movie_akas(movie_id):
    """Fetches alternative titles (AKAs) for a specific movie."""
    response = requests.get(f"{movie_details_url}/{movie_id}/translations", params={"api_key": api_key})
    if response.status_code == 200:
        translations = response.json().get('translations', [])
        akas = [t['data']['title'] for t in translations if 'data' in t]
        return akas
    else:
        print(f"Failed to retrieve AKAs for movie ID {movie_id}: {response.status_code}")
        return []


# Fetch movie details including cast, crew, country of origin, and more
def get_movie_details(movie_id):
    response = requests.get(f"{movie_details_url}/{movie_id}", params={"api_key": api_key, "language": "en-US"})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve movie details for ID {movie_id}: {response.status_code}")
        return {}

# Format the viewers rating to 1 decimal place
def format_rating(rating):
    if rating is not None:
        return round(rating, 1)
    return "N/A"

def display_movie_details():
    genres_map = get_genres()
    movies = get_movies()
    
    if not genres_map or not movies:
        print("No data to display.")
        return
    
    for movie in movies:
        title = movie.get('title', "Unknown")
        overview = movie.get('overview', "Unknown")
        vote_average = movie.get('vote_average', 0)  # Default to 0 for formatting
        genre_ids = movie.get('genre_ids', [])
        release_date = movie.get('release_date', "Unknown")
        release_year = release_date.split('-')[0] if release_date != "Unknown" else "Unknown"
        genres = [genres_map.get(genre_id, "Unknown") for genre_id in genre_ids]
        
        # Fetch additional details
        movie_id = movie.get('id')
        cast, directors = get_movie_cast_and_crew(movie_id)
        keywords = get_movie_keywords(movie_id)
        akas = get_movie_akas(movie_id)
        
        # Fallbacks
        directors_str = ", ".join(directors) or "Unknown"
        actors_str = ", ".join(cast[:5]) + ("..." if len(cast) > 5 else "Unknown")  # Limit to 5 for brevity
        akas_str = ", ".join(akas) or "Unknown"
        keywords_str = ", ".join(keywords) or "Unknown"
        
        # Display all details
        print(f"Title: {title}")
        print(f"Plot: {overview}")
        print(f"Viewers Rating: {format_rating(vote_average)}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Actors: {actors_str}")
        print(f"Directors: {directors_str}")
        print(f"Release Year: {release_year}")
        print(f"AKAs: {akas_str}")
        print(f"Keywords: {keywords_str}")
        print("-" * 20)


# Display
display_movie_details()