from app.agents import graph
import uuid

config = {"configurable": {"thread_id": str(uuid.uuid4())}}
if __name__ == "__main__":
    user_input = str(input("Enter your message: "))

    while user_input != "exit":
        ai_response = graph.invoke({"messages": {"role": "user", "content": user_input}, "results": {}}, config=config)
        print(ai_response["messages"][-1])
        print(graph.get_state(config=config))
        user_input = str(input("Enter your message: "))
