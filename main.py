import asyncio
import os
import sys
from dotenv import load_dotenv

# --- 1. PROJECT SETUP & PATHS ---
# Assuming main.py is in the PROJECT ROOT.
# We ensure the current directory is in sys.path so we can import 'concierge', 'tasks', etc.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Force a shared database path for all agents (CRITICAL fix from test_concierge)
SHARED_DB_PATH = os.path.join(current_dir, "db", "afloat.db")
os.environ["DB_PATH"] = SHARED_DB_PATH

# --- 2. IMPORTS ---
# Import the agent we verified in the test
try:
    from concierge.main_agent import afloat_concierge
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure you are running main.py from the project root.")
    sys.exit(1)

try:
    from google.adk.runners import InMemoryRunner
except ImportError:
    from google.adk import InMemoryRunner

# --- 3. CONFIGURATION ---
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️ Warning: GOOGLE_API_KEY not found in environment.")

# --- 4. MAIN EXECUTION (Matches test_concierge logic) ---
async def main():
    print(f"\n🌊 --- Afloat Concierge (DB: {SHARED_DB_PATH}) ---")
    print("Type 'exit' to quit.\n")
    
    # Initialize runner once to maintain context
    runner = InMemoryRunner(agent=afloat_concierge)
    
    while True:
        try:
            user_input = input("\n👤 You > ")
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "q"]:
                print("🌊 Goodbye!")
                break
            
            if not user_input.strip():
                continue

            # Run the agent using the debug runner (proven to work)
            await runner.run_debug(user_input)

        except KeyboardInterrupt:
            print("\n🌊 Goodbye!")
            break
        except Exception as e:
            print(f"❌ System Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())