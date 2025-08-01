from dotenv import load_dotenv
import os
from tmdbv3api import TMDb, Movie, TV
import requests
import time
import logging

load_dotenv(override=True)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
API_TOKEN = os.getenv("API_TOKEN")

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

    def search_tv(self, show_name, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                response = self.tv.search(show_name)
                results = list(response["results"])
                max_results = min(5, len(results))
                results = results[:max_results]
                return results
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}. Retrying in {2**retries} seconds...")
                time.sleep(2**retries)  # Exponential backoff
                retries += 1
        raise Exception("Failed to fetch movie data after multiple retries.")