from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Shared DB path
DB_PATH = os.getenv("DB_PATH", "db/afloat.db")

def get_tasks(status: str = "pending"):
    """
    Retrieves tasks from the database.
    Args:
        status: Filter tasks by 'pending', 'completed', or 'all'. Defaults to 'pending'.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Allows accessing columns by name
        c = conn.cursor()
        
        # Select tasks based on status
        if status == 'all':
            query = "SELECT * FROM tasks ORDER BY created_at DESC"
            params = ()
        else:
            query = "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC"
            params = (status,)
            
        rows = c.execute(query, params).fetchall()
        
        if not rows:
            return "No tasks found."
            
        # Format the output for the LLM to read easily
        task_list = []
        for row in rows:
            task_list.append(f"- [ID: {row['id']}] {row['description']} ({row['frequency']})")
            
        return "\n".join(task_list)

    except sqlite3.Error as e:
        return f"❌ Database Error: {e}"
    finally:
        if conn: conn.close()

# Create the Agent
task_reader_agent = Agent(
    name="TaskReader",
    model="gemini-2.5-flash-lite",
    instruction="""You are a Personal Concierge helper.
    Your goal is to retrieve the user's tasks and present them in a friendly, organized way.
    
    Rules:
    1. Use the `get_tasks` tool to fetch data. Default to 'pending' tasks unless asked otherwise.
    2. If the user asks for "all tasks" or "history", set status='all'.
    3. Present the list clearly. If the list is empty, offer encouragement.""",
    tools=[FunctionTool(get_tasks)],
    output_key="task_summary", 
)

print("✅ task_reader_agent created and linked to get_tasks tool.")