from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

task_sql_reader_agent = Agent(
    name="TaskAgentReader",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options= retry_config
    ),
    instruction="""You are a specialized Task Tracker agent.
        Your job is to generate a text summary from the provided task JSON, retrieved from a SQL database.

        The JSON object will contain exactly these four keys, with their corresponding data types and constraints:

        1.  `timestamp`: (Integer) The exact time of the request in UNIX timestamp format.
        2.  `description`: (String) A concise description of the task, not exceeding 50 words.
        3. `deadline`: (Integer) The exact time of the tasks deadline in UNIX timestamp format.


        Your output **must be a text summary not more than 50 words** from these three keys and their values.""",
    tools=[google_search],
    output_key="task_data_sql_json"
)