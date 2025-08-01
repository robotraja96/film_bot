from app.agents import build_graph
import uuid
from langchain_core.messages import HumanMessage

graph = build_graph()

config = {"configurable": {"thread_id": str(uuid.uuid4())}}
if __name__ == "__main__":
    user_input = str(input("Enter your message: "))

    while user_input != "exit":        
        ai_response = graph.invoke({"messages": HumanMessage(content=user_input)}, config=config)        
        print(str(ai_response["messages"][-1].content) + "\n\n")   
        user_input = str(input("Enter your message: "))     
        # print(graph.get_state(config=config))        user_input = str(input("Enter your message: "))
