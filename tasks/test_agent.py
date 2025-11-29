import asyncio
import os
from dotenv import load_dotenv

# --- IMPORTS FROM MODULES ---
from task_writer import task_writer_agent
from task_reader import task_reader_agent

# Attempting standard import path for the runner
try:
    from google.adk.runners import InMemoryRunner
except ImportError:
    from google.adk import InMemoryRunner

# 0. Setup: Load Environment Variables
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️ Warning: GOOGLE_API_KEY not found in environment or .env file.")

# 1. Setup: DB Path Check (Optional safety check)
DB_PATH = os.getenv("DB_PATH", "db/afloat.db")
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)

# --- RUNNER ---

async def main():
    # TEST 1: Write
    print("\n🔹 --- TEST 1: Writing a Task ---")
    writer_runner = InMemoryRunner(agent=task_writer_agent)
    write_input = "Remind me to take my coffee every morning."
    print(f"User: '{write_input}'")
    await writer_runner.run_debug(write_input)

    # TEST 2: Read
    print("\n🔹 --- TEST 2: Reading Tasks ---")
    reader_runner = InMemoryRunner(agent=task_reader_agent)
    read_input = "What do I have to do today?"
    print(f"User: '{read_input}'")
    await reader_runner.run_debug(read_input)
    
    print("\n🔹 Sequence finished.")

if __name__ == "__main__":
    asyncio.run(main())