"""
Sample Agent for ADK Web UI
This agent is designed to work with the ADK CLI tools (adk web, adk run, adk api_server).
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types


# Configure retry options for handling transient errors
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# Create the root agent
# This agent will be automatically loaded by ADK CLI commands
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions using Google Search.",
    instruction="You are a helpful assistant. Use Google Search for current information or when you're unsure about something.",
    tools=[google_search],
)
