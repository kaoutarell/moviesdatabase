# Movies Database - Assignment 2 

## General Note

In our project, we'll be using three different APIs from TMDB (The Movie Database) to gather information about movies:

1. Discover API (discover_url): This API allows us to retrieve a list of movies based on specific filters, such as genre, release date, etc.
2. Genres API (genres_url): This API provides a list of movie genres, which helps categorize the movies.
3. Movie Details API (movie_details_url): This API gives detailed information about each movie, including the cast and crew.

Since the information about actors, directors, and genres is not included in the same response as the other movie details, we loop through all three APIs in our code. This allows us to gather the necessary data and combine it, ensuring that we can display complete movie details including the cast, crew, and genres.

> API Links :
- [https://api.themoviedb.org/3/discover/movie]
- [https://api.themoviedb.org/3/genre/movie/list]
- [https://api.themoviedb.org/3/movie]

## Python Config

#### Install python :

```
brew install python
```

#### Check python's version :

```
python3 --version
```

#### Install request library using PIP :

```
pip3 install requests
```

#### Install Psycopg2

```
brew install postgresql
```

```
pip3 install psycopg2
```

#### Install Postgres

```
brew install postgresql
```

#### Requests library used to fetch the API :

```
pip3 install requests
```

#### Request doesn't work unless a virtual environment is set :

```
python3 -m venv path/to/venv
```

```
python3 -m venv myenv
```

#### Activate the Virtual Environment :

```
source myenv/bin/activate
```

#### Command to run movies.py :

```
python3 movies.py
```

## POSTGRES CONFIG

```
docker run --name postgres-container --network pgnetwork -e POSTGRES_USER=kel -e POSTGRES_PASSWORD=soen363 -e POSTGRES_DB=movies_db -p 5432:5432 -d postgres

```
