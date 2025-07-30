import os
# This below line is added so that Windows users can import from src without getting no module found error
import sys
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from src.app.agents import build_graph
from fastapi import FastAPI

app = FastAPI()
graph = build_graph()



# Initialize the CopilotKit SDK 
sdk = CopilotKitRemoteEndpoint(agents=[
        LangGraphAgent(
            name="agent",
            description="A bot that answers questions about movies",
            graph=graph,
        )
    ], actions=[])

# Add the CopilotKit endpoint to your FastAPI app 
add_fastapi_endpoint(app, sdk, "/copilotkit_remote", max_workers=10)

def main():
    """Run the uvicorn server."""
    import uvicorn
    uvicorn.run("src.app.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()