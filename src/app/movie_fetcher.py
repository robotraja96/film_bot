from dotenv import load_dotenv
import os
from tmdbv3api import TMDb, Movie, TV
import requests
import time
import logging

load_dotenv(override=True)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
API_TOKEN = os.getenv("API_TOKEN")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MovieFetcher:
    def __init__(self, api_key, api_token):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.movie = Movie()
        self.tv = TV()
        self.api_token = api_token
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

    def search_movie(self, movie_name, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                response = self.movie.search(movie_name)
                results = list(response["results"])
                max_results = min(5, len(results))
                results = results[:max_results]
                return results
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}. Retrying in {2**retries} seconds...")
                time.sleep(2**retries)  # Exponential backoff
                retries += 1
        raise Exception("Failed to fetch movie data after multiple retries.")


    def get_movie_reviews(self, movie_id, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json().get('results', [])
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}. Retrying in {2**retries} seconds...")
                time.sleep(2**retries)
                retries += 1
        raise Exception("Failed to fetch movie reviews after multiple retries.")


    def get_imdb_id(self, movie_id, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                imdb_id = response.json().get("imdb_id", [])
                logging.info(f"Successfully fetched IMDb ID for movie ID: {movie_id}")
                return imdb_id
            except requests.exceptions.ConnectionError as e:
                logging.error(f"Connection error: {e}. Retrying in {2**retries} seconds...")
                time.sleep(2**retries)
                retries += 1
        logging.error(f"Failed to fetch IMDb ID for movie ID: {movie_id} after multiple retries.")
        raise Exception("Failed to fetch IMDb ID after multiple retries.")


    def fetch_movie_details_title(self, movie_title, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}. Retrying in {2**retries} seconds...")
                time.sleep(2**retries)
                retries += 1
        raise Exception("Failed to fetch movie reviews after multiple retries.")
    
    def fetch_movie_details_id(self, movie_id, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                url = f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}"
                print(url)
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}. Retrying in {2**retries} seconds...")
                time.sleep(2**retries)
                retries += 1
        raise Exception("Failed to fetch movie reviews after multiple retries.")
    


if __name__ == "__main__":
    fetcher = MovieFetcher(TMDB_API_KEY, API_TOKEN)
    # print(fetcher.search_movie("Sinners"))
    # print(fetcher.search_tv("The Office"))
    # print(fetcher.get_movie_reviews(603))
    # print(fetcher.get_imdb_id(603))
    #
    # print(fetcher.fetch_movie_details_id("tt0133093"))
    # print(fetcher.fetch_movie_details_title("Your Name"))