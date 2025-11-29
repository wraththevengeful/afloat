from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# UPDATE THIS PATH: Use relative ("../data/afloat.db") or absolute paths
DB_PATH = os.getenv("DB_PATH", "db/afloat.db")

def add_task(description: str, frequency: str = "once"):
    """Saves a task to the specific SQLite database file."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("INSERT INTO tasks (description, frequency) VALUES (?, ?)", 
                  (description, frequency))
        
        conn.commit()
        return f"✅ Saved: '{description}' ({frequency})"
        
    except sqlite3.Error as e:
        return f"❌ Database Error: {e}"
    finally:
        if conn: conn.close()

# 2. Create the Agent with the specific instruction and tool
task_writer_agent = Agent(
    name="TaskWriter",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Personal Concierge responsible for task management.
    Your goal is to listen to the user, extract the task details, and save them.
    
    Rules:
    1. Distinguish between one-off tasks and recurring habits.
    2. If the user implies repetition (e.g., "every day", "daily"), set frequency accordingly.
    3. Always use the add_task tool to save the data.""",
    tools=[FunctionTool(add_task)],
    output_key="task_log", 
)

print("✅ task_writer_agent created and linked to add_task tool.")