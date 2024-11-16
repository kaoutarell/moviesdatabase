# Movies Database - Assignment 2

## Questions are answered in separate folders/files

- DLL Queries (part 1) : DLL_1 folder
- Data Population (part 2 and 3) : DP folder
- ERD (part 4) : ERD folder
- Database DLL (part 5) : DLL_5
- Use of views (part 6) : DLL_view
- Queries (part 7) : Queries (each query is written in separate file)

## General Note

In our project, we'll be using three different APIs from TMDB (The Movie Database) to gather information about movies:

1. Discover API (discover_url): This API allows us to retrieve a list of movies based on specific filters, such as genre, release date, etc.
2. Genres API (genres_url): This API provides a list of movie genres, which helps categorize the movies.
3. Movie Details API (movie_details_url): This API gives detailed information about each movie, including the cast and crew.
4. Reviews table has been added to the ERD, database instance and APIs calls are adjusted accordingly
5. The APIs used don't show the imdb and tmdb, those ones are generated in the python code in db_pop_dll.py file > DLL_5

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
docker run --name postgres-container --network pgnetwork -e POSTGRES_USER=kel -e POSTGRES_PASSWORD=soen363 -e POSTGRES_DB=movies_db -p 5431:5432 -d postgres

```
