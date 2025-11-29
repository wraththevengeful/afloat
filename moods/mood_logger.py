import sqlite3
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "db/afloat.db")

def log_mood(emotion: str, notes: str = ""):
    """
    Logs the user's mood into the database.
    Args:
        emotion: One word describing the feeling (e.g., 'Anxious', 'Happy', 'Tired').
        notes: A brief context or reason for the mood (e.g., 'Stressed about deadline').
    """
    # Ensure directory exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Create mood table
        c.execute('''CREATE TABLE IF NOT EXISTS mood_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emotion TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            
        c.execute("INSERT INTO mood_logs (emotion, notes) VALUES (?, ?)", 
                  (emotion, notes))
        
        conn.commit()
        return f"✅ Mood logged: '{emotion}'"
        
    except sqlite3.Error as e:
        return f"❌ Database Error: {e}"
    finally:
        if conn: conn.close()

# The Agent Definition
mood_agent = Agent(
    name="MoodTracker",
    model="gemini-2.5-flash-lite",
    instruction="""You are an Empathetic Listener. 
    Your goal is to detect the user's emotional state from their text and log it using `log_mood`.
    
    Rules:
    1. Infer the emotion (e.g., if user says "I'm swamped", emotion="Overwhelmed").
    2. Extract context for the 'notes' field.
    3. Be supportive but invisible; you don't need to give advice, just log the data.""",
    tools=[FunctionTool(log_mood)],
    output_key="mood_log", 
)

print("✅ mood_agent created and linked to log_mood tool.")