import sys
import os

# Add parent directory to path so we can import from tasks/ and moods/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# IMPORTS: We import the functions directly now, bypassing the sub-agent wrappers
from tasks.task_writer import add_task
from tasks.task_reader import get_tasks
from moods.mood_logger import log_mood

# Root Coordinator: Now holds the tools directly for reliable execution
afloat_concierge = Agent(
    name="AfloatConcierge",
    model="gemini-2.5-flash-lite",
    instruction="""You are 'Afloat', an empathetic personal concierge. 
    Your goal is to help the user manage their life while validating their feelings.
    
    You have access to three specialized tools:
    1. `log_mood`: Call this if the user expresses emotion, vents, or shares how they feel.
    2. `add_task`: Call this if the user wants to add, remind, or schedule a task/habit.
    3. `get_tasks`: Call this if the user asks what they have to do or checks their list.
    
    Workflow:
    - Listen to the user.
    - If they are venting ("I'm so overwhelmed"), FIRST acknowledge it warmly, THEN call `log_mood`.
    - If they give a command ("Remind me to..."), call `add_task`.
    - If they ask for info ("What's next?"), call `get_tasks`.
    - You can call multiple tools if needed (e.g., log mood then check tasks).
    """,
    tools=[
        FunctionTool(log_mood),
        FunctionTool(add_task),
        FunctionTool(get_tasks)
    ],
)

print("✅ Afloat Concierge (Direct Tools) created.")