from typing import Annotated
import os
from langchain_core.tools import tool
from src.app.movie_fetcher import MovieFetcher
from dotenv import load_dotenv

load_dotenv(override=True)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
API_TOKEN = os.getenv("API_TOKEN")

@tool
def search_movie(movie_name: str):
    """
    Use this function to search for a movie.

    Args:
        movie_name (str): The name of the movie to search for.
    """
    movie_fetcher = MovieFetcher(api_key=TMDB_API_KEY, api_token=API_TOKEN)
    results = movie_fetcher.search_movie(movie_name)
    
    new_res_dict = {}
    for res_num, res in enumerate(results):
        new_res_dict[f"Option_{res_num + 1}"] = {
            "id": res["id"],
            "title": res["title"],
            "overview": res["overview"],
            "release_date": res["release_date"],
            "language": res["original_language"],
        }

    return new_res_dict


@tool
def get_movie_reviews(movie_id: str):
    """
    Use this function to get reviews for a movie.

    Args:
        movie_id (str): The id of the movie the user has selected from the given options
    """
    if not movie_id:
        return "The selected movie is not available"
    movie_fetcher = MovieFetcher(api_key=TMDB_API_KEY, api_token=API_TOKEN)
    reviews = movie_fetcher.get_movie_reviews(movie_id)
    all_reviews = [review["content"] for review in reviews]

    return all_reviews


@tool
def fetch_movie_details_by_name(movie_name: str):
    """
    Use this function to get details for a movie instantly

    Args:
        movie_name (str): name of the movie user has asked for
    """

    movie_fetcher = MovieFetcher(api_key=TMDB_API_KEY, api_token=API_TOKEN)
    details = movie_fetcher.fetch_movie_details_title(movie_name)
    return details


@tool
def fetch_movie_details_by_id(movie_id: str):
    """
    Use this function to get details for a movie. Use the ID after searching for the movie using the search_movie tool and confirming it with the user.

    Args:
        movie_id (str): id of the movie
    """

    movie_fetcher = MovieFetcher(api_key=TMDB_API_KEY, api_token=API_TOKEN)
    imdb_id = movie_fetcher.get_imdb_id(movie_id)
    details = movie_fetcher.fetch_movie_details_id(imdb_id)
    return details