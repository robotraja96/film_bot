import logging
from typing import Annotated, TypedDict
import os
# This below line is added so that Windows users can import from src without getting no module found error
import sys
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# LangGraph and Langchain imports
from langgraph.graph import StateGraph, END, START, add_messages
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

# Custom imports
from src.app.prompts import conv_prompt
from src.app.tools import search_movie, get_movie_reviews



# Configure logging settings for debugging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for extensive logging
logger = logging.getLogger(__name__)

memory = InMemorySaver()
class Agent(TypedDict):
    messages: Annotated[list, add_messages]
    results: dict
    remaining_steps: int


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    name="conversation_agent",
    temperature=0.7,
    api_key=os.getenv("GOOGLE_API_KEY"),

)



tools = [search_movie, get_movie_reviews]
tool_node = ToolNode(tools)



def convo_agent(state :Agent):
    # The agent expects the full state dictionary as input
    # and returns a dictionary with the updated state.
    conversation_agent = create_react_agent(
    model=llm,
    prompt=conv_prompt,
    state_schema=Agent,
    tools=tools
)
    response = conversation_agent.invoke(state)
    return response




def build_graph():
    builder = StateGraph(Agent)
    # builder.add_node("end", END)
    builder.add_node("conversation_agent", convo_agent)
    builder.add_edge(START, "conversation_agent")
    builder.add_edge("conversation_agent", END)

    graph = builder.compile(checkpointer=memory)

    return graph


