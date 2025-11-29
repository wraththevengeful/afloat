import asyncio
import os
from dotenv import load_dotenv

# Import the new agent
from mood_logger import mood_agent

try:
    from google.adk.runners import InMemoryRunner
except ImportError:
    from google.adk import InMemoryRunner

# Setup
load_dotenv()

async def main():
    print("\n🔹 --- TEST: Mood Logging ---")
    runner = InMemoryRunner(agent=mood_agent)
    
    # Simulating a user venting
    user_input = "I am honestly just so tired of this project, it feels never-ending."
    print(f"User: '{user_input}'")
    
    await runner.run_debug(user_input)
    print("\n🔹 Mood tracking finished.")

if __name__ == "__main__":
    asyncio.run(main())