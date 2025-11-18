from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

activity_sql_reader_agent = Agent(
    name="ActivityAgentReader",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options= retry_config
    ),
    instruction="""You are a specialized Activity Tracker agent.
        Your job is to generate a summary from the provided activity JSON, retrieved a SQL database.

        The JSON object contains exactly these four keys, with their corresponding data types and constraints:

        1.  `timestamp`: (Integer) The exact time of the request in UNIX timestamp format.
        2.  `category`: (String) Must be one of: 'mental_health', 'daily_essentials', 'weekly_activities', 'monthly', 'custom'.
        3.  `description`: (String) A concise description of the activity, not exceeding 100 words.
        4.  `impact`: (String) Must be either 'negative' or 'positive'.

        You are allowed to use Google Search to gather any necessary data related to the activity to write your summary.

        Your output **must be a valid text paragraph not more than 250 lines** built on these four keys and their values.""",
    tools=[google_search],
    output_key="activity_data_text_summary"
)