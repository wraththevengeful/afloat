import asyncio
import os
import sys

# 1. Setup path to find siblings (tasks, moods)
# We calculate the PROJECT ROOT (one level up from this script)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# 2. FORCE SHARED DB PATH
# We set this BEFORE importing agents so they all pick up the same path.
# This prevents "tasks/" creating a db and "concierge/" creating a separate empty db.
shared_db_path = os.path.join(project_root, "db", "afloat.db")
os.environ["DB_PATH"] = shared_db_path

print(f"✅ Forced Shared DB Path: {shared_db_path}")

from dotenv import load_dotenv
from main_agent import afloat_concierge

try:
    from google.adk.runners import InMemoryRunner
except ImportError:
    from google.adk import InMemoryRunner

# Setup
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️ Warning: GOOGLE_API_KEY not found.")

async def main():
    print("\n🌊 --- Afloat Terminal Session (Type 'exit' to quit) ---")
    
    # Initialize runner with the coordinator agent
    runner = InMemoryRunner(agent=afloat_concierge)
    
    while True:
        try:
            user_input = input("\n👤 You > ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            if not user_input.strip():
                continue

            # Usage from lesson: await runner.run_debug(input_string)
            # The "Warning" you see is normal; it just means the AI decided to use a tool.
            # We wait for the loop to finish.
            await runner.run_debug(user_input)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())