from typing import Annotated
import os
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langchain_core.tools.base import InjectedToolCallId
from langgraph.types import Command
from src.app.movie_fetcher import MovieFetcher
from dotenv import load_dotenv

load_dotenv(override=True)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
API_TOKEN = os.getenv("API_TOKEN")

REVIIEW_RESULTS = {}


@tool
def search_movie(
    movie_name,
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    """
    Use this function to search for a movie.

    Args:
        movie_name (str): The name of the movie to search for.
    """
    global REVIIEW_RESULTS
    movie_fetcher = MovieFetcher(api_key=TMDB_API_KEY, api_token=API_TOKEN)
    results = movie_fetcher.search_movie(movie_name)
    print(type(results))
    new_res_dict = {}
    for res_num, res in enumerate(results):
        new_res_dict[f"Option_{res_num + 1}"] = {}
        new_res_dict[f"Option_{res_num + 1}"]["id"] = res["id"]
        new_res_dict[f"Option_{res_num + 1}"]["title"] = res["title"]
        new_res_dict[f"Option_{res_num + 1}"]["overview"] = res["overview"]
        new_res_dict[f"Option_{res_num + 1}"]["release_date"] = res["release_date"]
        new_res_dict[f"Option_{res_num + 1}"]["language"] = res["original_language"]

    REVIIEW_RESULTS = new_res_dict
    return Command(
        graph=Command.PARENT,
        update={
            "results": new_res_dict,
            "messages": state["messages"]
            + [
                ToolMessage(
                    content=new_res_dict,
                    tool_call_id=tool_call_id,
                )
            ],
        },
    )


@tool
def get_movie_reviews(
    movie_id,
    # state: Annotated[dict, InjectedState]
):
    """
    Use this function to get reviews for a movie.

    Args:
        movie_id (str): The id of the movie the user has selected from the given options
    """
    # print(state["results"].keys())

    # movie_id = state["results"][user_option]["id"]
    if not movie_id:
        return "The selected movie not available"
    movie_fetcher = MovieFetcher(api_key=TMDB_API_KEY, api_token=API_TOKEN)
    reviews = movie_fetcher.get_movie_reviews(movie_id)
    all_reviews = []
    for review in reviews:
        all_reviews.append(review["content"])

    # systen_prompt = SystemMessage(content=synthesis_prompt)
    # response = synthesis_llm.invoke([systen_prompt] + all_reviews)
    return all_reviews
