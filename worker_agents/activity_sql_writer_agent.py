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

activity_sql_writer_agent = Agent(
    name="ActivityAgentWriter",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options= retry_config
    ),
    instruction="""You are a specialized Activity Tracker agent.
        Your job is to generate a JSON object from the provided activity data, suitable for direct insertion into a SQL database.

        The JSON object must contain exactly these four keys, with their corresponding data types and constraints:

        1.  `timestamp`: (Integer) The exact time of the request in UNIX timestamp format.
        2.  `category`: (String) Must be one of: 'mental_health', 'daily_essentials', 'weekly_activities', 'monthly', 'custom'.
        3.  `description`: (String) A concise description of the activity, not exceeding 100 words.
        4.  `impact`: (String) Must be either 'negative' or 'positive'.

        You are allowed to use Google Search to gather any necessary data related to the activity to populate these fields.

        REMEMBER sometimes the timestamp could be empty. `timestamp` is the only attribute you can leave empty.

        Your output **must be a valid JSON object** with these four keys and their values.""",
    tools=[google_search],
    output_key="activity_data_sql_json"
)