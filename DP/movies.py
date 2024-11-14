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
            if len(movies) >= 50:  # If we have at least 50 movies -> BREAK
                break
        else:
            print(f"Failed to retrieve movies from page {page}: {response.status_code}")
            break

    return movies[:50]  # Return the first 50 movies found

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

# Print the movie details
def display_movie_details():
    genres_map = get_genres()
    movies = get_movies()
    
    if not genres_map or not movies:
        print("No data to display.")
        return
    
    for movie in movies:
        title = movie.get('title')
        overview = movie.get('overview')
        vote_average = movie.get('vote_average')  # Viewers rating
        genre_ids = movie.get('genre_ids', [])  # genres are listed by id on another API link -> showed above
        release_date = movie.get('release_date')
        
        # Extract the release year
        release_year = release_date.split('-')[0] if release_date else "N/A"
        
        # Assign genre_ids to genre names
        genres = [genres_map.get(genre_id, "Unknown") for genre_id in genre_ids]
        
        # Get the movie details (cast, crew, country of origin, AKAs, languages, and keywords)
        movie_details = get_movie_details(movie.get('id'))
        
        if movie_details:
            # Get content rating
            content_rating = movie_details.get('release_dates', {}).get('results', [{}])[0].get('certification', "N/A")
            # Get directors (crew)
            directors = [member['name'] for member in movie_details.get('credits', {}).get('crew', []) if member['job'] == 'Director']
            # Get actors (cast)
            actors = [member['name'] for member in movie_details.get('credits', {}).get('cast', [])]
            # Get alternative titles (AKAs)
            akas = [title['title'] for title in movie_details.get('translations', {}).get('translations', []) if title.get('iso_3166_1') == "US"]
            # Get production countries
            countries = [country['name'] for country in movie_details.get('production_countries', [])]
            # Get languages
            languages = [language['name'] for language in movie_details.get('spoken_languages', [])]
            # Get keywords
            keywords_data = movie_details.get('keywords', {}).get('keywords', [])
            keywords = [keyword['name'] for keyword in keywords_data]
            
            # Prepare the list of directors, actors, and countries to display
            directors_str = ", ".join(directors) if directors else "N/A"
            actors_str = ", ".join(actors[:5]) + ("..." if len(actors) > 5 else "")  # Limit to 5 actors for brevity
            akas_str = ", ".join(akas) if akas else "N/A"
            countries_str = ", ".join(countries) if countries else "N/A"
            languages_str = ", ".join(languages) if languages else "N/A"
            keywords_str = ", ".join(keywords) if keywords else "N/A"
            
            # Display all the data
            print(f"Title: {title}")
            print(f"Plot: {overview}")
            print(f"Content Rating: {content_rating}")
            print(f"Viewers Rating: {format_rating(vote_average)}")
            print(f"Genres: {', '.join(genres)}")
            print(f"Actors: {actors_str}")
            print(f"Directors: {directors_str}")
            print(f"Release Year: {release_year}")
            print(f"AKAs: {akas_str}")
            print(f"Countries: {countries_str}")
            print(f"Languages: {languages_str}")
            print(f"Keywords: {keywords_str}")
        else:
            print(f"Movie Details not found for {title}")
        
        print("-" * 50)

# Display
display_movie_details()
