"""
Multi-Agent System for ADK CLI
This file defines a multi-agent system that can be used with ADK CLI commands.

Usage:
    adk run          # Interactive CLI
    adk web          # Web interface
    adk api_server   # REST API server
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types


# Configure retry options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# Create specialized agents
research_agent = Agent(
    name="ResearchAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a specialized research agent. Use the google_search tool
    to find relevant information on the given topic and present findings with citations.""",
    tools=[google_search],
    output_key="research_findings",
)

summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Read the provided research findings: {research_findings}
    Create a concise summary with 3-5 key points in a bulleted list.""",
    output_key="final_summary",
)

# Create the root agent as a Sequential workflow
root_agent = SequentialAgent(
    name="ResearchPipeline",
    sub_agents=[research_agent, summarizer_agent],
)
