import os
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
import asyncio

from root_agents.root_agent import root_agent


try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    print("Google API Key found!")
except Exception as e:
    print(f"Error. No key found. Please make sure you added an API key. Details: {e}")


runner = InMemoryRunner(agent=root_agent, app_name="UserLevelCoordinatorApp")

async def getResponse(question):
    response = await runner.run_debug(question)
    return response
if __name__ == "__main__":
    asyncio.run(getResponse("The user wants to add a task to get apples tomorrow")) 