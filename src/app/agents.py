import logging
from typing import Annotated, Literal, TypedDict
import os

# This below line is added so that Windows users can import from src without getting no module found error
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# LangGraph and Langchain imports
from langgraph.graph import StateGraph, END, START, add_messages
from langgraph.prebuilt import create_react_agent, ToolNode
from langchain_core.messages import SystemMessage, BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field



# Custom imports
from src.app.prompts import reviews_prompt, router_prompt, general_conv_prompt
from src.app.tools import search_movie, get_movie_reviews, fetch_movie_details_by_name, fetch_movie_details_by_id


# Configure logging settings for debugging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for extensive logging
logger = logging.getLogger(__name__)

# Memory checkpoint object
memory = InMemorySaver()

# Agent definition
class Agent(TypedDict):
    messages: Annotated[list, add_messages]

# Router pydantic model
class RouteQuery(BaseModel):
    """Route a user query to the most relevant agent."""

    route: Literal["reviews", "general_conversation"] = Field(
        ...,
        description="Given a user question choose which agent would be most appropriate for answering their question.",
    )


# LLM with function calling
router_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
structured_llm = router_llm.with_structured_output(RouteQuery)

# # Define router
# router = router_prompt | structured_llm


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    name="conversation_agent",
    temperature=0.5,
)

# Define the tools for the review agent
review_tools = [search_movie, get_movie_reviews]
review_tool_node = ToolNode(review_tools)

# Define the review agent
review_agent = create_react_agent(
    model=llm,
    prompt=reviews_prompt,
    tools=review_tools,
)

# Define the tools for the general conversation agent
general_tools = [search_movie, fetch_movie_details_by_id, fetch_movie_details_by_name]

# Define the general conversation agent
general_conversation_agent = create_react_agent(
    model=llm,
    prompt=general_conv_prompt,
    tools=general_tools,
)


def should_route(state: Agent):
    messages = [SystemMessage(content=router_prompt)] + state["messages"]
    route = structured_llm.invoke(messages)
    if route.route == "reviews":
        return "reviews"
    else:
        return "general_conversation"


def build_graph():
    # Initialize the StateGraph
    builder = StateGraph(Agent)

    # Add nodes
    builder.add_node("reviews_agent", review_agent)
    builder.add_node("general_conversation_agent", general_conversation_agent)

    # Add edges
    builder.add_conditional_edges(
        START,
        should_route,
        {
            "reviews": "reviews_agent",
            "general_conversation": "general_conversation_agent",
        },
    )

    builder.add_edge("reviews_agent", END)
    builder.add_edge("general_conversation_agent", END)

    # Compile the graph
    graph = builder.compile(checkpointer=memory)

    return graph
