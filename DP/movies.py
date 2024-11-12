#-------------------------------------------------- DATA POPULATION ---------------------------------------------------------------

#print("Hello, Python!")

# --------------- PART 2 : Consume a web service, either via a small code that performs get operations for each movie in question

import requests # type: ignore

# Define the base URL and API key
api_key = "d3967d088d5c2e4baa702cf128358a62"
discover_url = "https://api.themoviedb.org/3/discover/movie" # movies API
genres_url = "https://api.themoviedb.org/3/genre/movie/list" # movies genres API

# Fetch the genre list
def get_genres():
    response = requests.get(genres_url, params={"api_key": api_key, "language": "en-US"})
    if response.status_code == 200:
        genres_data = response.json()
        return {genre['id']: genre['name'] for genre in genres_data['genres']}
    else:
        print(f"Failed to retrieve genres: {response.status_code}")
        return {}

# Fetch the movie data
def get_movies():
    params = {
        "api_key": api_key,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": 1  # You can change this to get data for different pages
    }
    
    response = requests.get(discover_url, params=params)
    
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Failed to retrieve movies: {response.status_code}")
        return []

# Main function to print the movie details
def display_movie_details():
    genres_map = get_genres()
    movies = get_movies()
    
    if not genres_map or not movies:
        print("No data to display.")
        return
    
    for movie in movies:
        title = movie.get('title')
        original_title = movie.get('original_title')
        overview = movie.get('overview')
        release_date = movie.get('release_date')
        popularity = movie.get('popularity')
        vote_average = movie.get('vote_average')
        vote_count = movie.get('vote_count')
        genre_ids = movie.get('genre_ids', []) # genres are listed by id on another API link -> showed above
        
        # Map genre_ids to genre names
        genres = [genres_map.get(genre_id, "Unknown") for genre_id in genre_ids]
        
        print(f"Title: {title}")
        print(f"Original Title: {original_title}")
        print(f"Description: {overview}")
        print(f"Release Date: {release_date}")
        print(f"Popularity: {popularity}")
        print(f"Vote Average: {vote_average}")
        print(f"Vote Count: {vote_count}")
        print(f"Genres: {', '.join(genres)}")
        print("-" * 50)

# Call the function to display movie details
display_movie_details()

