from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.adk.tools import AgentTool
from google.genai import types

from worker_agents.activity_sql_reader_agent import activity_sql_reader_agent
from worker_agents.activity_sql_writer_agent import activity_sql_writer_agent
from worker_agents.task_sql_reader_agent import task_sql_reader_agent
from worker_agents.task_sql_writer_agent import task_sql_writer_agent

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
)

root_agent = Agent(
    name = "UserLevelCoordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a coordinator agent for a task and resource manager.
    Your goal is orchestrating a workflow.
    Under you are multiple agents and tools.
    When an user interacts with you, you are supposed to find the next best course of action and the next tool or agent
    you have to use to retrieve and/or send information.

    Your task can be one of these follows:

    1. When an user says they have finished an activity, you MUST call the `ActivityAgentWriter` and send a summary 
    of what the user accomplished to the agent. The summary must include the timestamp. Either the user will enter a timestamp 
    or you can use the timestamp the request was made. The timestamp is in UNIX format.

    2. When an user asks about an activity they previously, you MUST call the `ActivityAgentReader` and ask for a summary of the activity. 
    The summary will be a text format. You can then use that summary to answer the user.

    3. When an user says they have a task to finish, you MUST call the `TaskAgentWriter` and send a summary of the task to that agent.
    The summary must include a timestamp in UNIX format. If no timestamp is provided, you use the time the request was made at.
    You MUST also ask for a deadline and a description of the task. Remember deadline is MANDATORY but description can be made by you if not explicity provided.
    
    4. When an user asks about tasks or a specific they have to finish, you MUST call the `TaskAgentReader` and query a summary of the task to that agent or all tasks.
    The summary must include a deadline in UNIX format. If no deadline is provided, you must ask the agent for such.
    Then you can process the deadline UNIX format to human readable format. 
    Remember deadline is MANDATORY. 
    """,
    tools=[AgentTool(activity_sql_reader_agent), AgentTool(activity_sql_writer_agent), AgentTool(task_sql_reader_agent), AgentTool(task_sql_writer_agent)],
)

