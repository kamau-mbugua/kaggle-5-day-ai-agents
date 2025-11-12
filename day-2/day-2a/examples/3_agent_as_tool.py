"""
Agent as Tool - Delegation Pattern
Based on the Kaggle 5-Day Agents Course - Day 2a

This demonstrates the difference between Agent Tools and Sub-Agents:

Agent Tools (this example):
- Agent A calls Agent B as a tool
- Agent B's response goes back to Agent A
- Agent A stays in control
- Use case: Delegation for specific tasks

Sub-Agents (different pattern):
- Agent A transfers control completely to Agent B
- Agent B takes over and handles future input
- Use case: Handoff to specialists

In this example, we have a research agent that delegates to specialist agents.
"""

import os
import asyncio
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
from google.genai import types


def load_api_key():
    """Load the Google API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found. Please create a .env file with your API key.\n"
            "Get your API key from: https://aistudio.google.com/app/apikey"
        )

    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


def create_retry_config():
    """Create retry configuration for handling transient errors."""
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )


def create_specialist_agents(retry_config):
    """
    Create specialist agents that can be used as tools.

    These agents are experts in specific domains:
    - DataAnalystAgent: Analyzes numerical data and trends
    - SummarizerAgent: Creates concise summaries
    """

    # Data Analyst Agent
    data_analyst = LlmAgent(
        name="DataAnalystAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized data analyst.

        Your only job is to analyze numerical data and identify trends.

        When given data:
        1. Identify key numerical patterns
        2. Calculate important metrics (averages, growth rates, etc.)
        3. Highlight significant trends
        4. Present findings in a clear, structured format

        Keep your analysis focused and data-driven.
        """,
    )

    # Summarizer Agent
    summarizer = LlmAgent(
        name="SummarizerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized summarizer.

        Your only job is to create concise summaries from information.

        When given text:
        1. Extract the most important points
        2. Create a bulleted summary (3-5 key points)
        3. Keep it brief and clear
        4. Maintain factual accuracy

        Do not add opinions or extra information.
        """,
    )

    return data_analyst, summarizer


def create_coordinator_agent(retry_config, data_analyst, summarizer):
    """
    Create a coordinator agent that uses specialist agents as tools.

    This agent:
    - Receives user requests
    - Decides which specialist agent to call
    - Combines results to give a final answer
    - Stays in control throughout the interaction
    """

    coordinator = LlmAgent(
        name="ResearchCoordinator",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a research coordinator that manages specialist agents.

        You have access to specialist agents as tools:
        - DataAnalystAgent: Use for analyzing numerical data and trends
        - SummarizerAgent: Use for creating concise summaries of information
        - google_search: Use for finding current information

        For research requests:
        1. Use google_search to find relevant information
        2. If the information contains numerical data, call DataAnalystAgent
        3. Call SummarizerAgent to create a final concise summary
        4. Present the combined results to the user

        You coordinate the workflow but stay in control throughout.
        """,
        tools=[
            google_search,
            AgentTool(agent=data_analyst),  # Specialist agent as tool
            AgentTool(agent=summarizer),    # Specialist agent as tool
        ],
    )

    return coordinator


async def demo_agent_as_tool():
    """Demonstrate using agents as tools."""

    print("\n" + "="*80)
    print("🤖 AGENT AS TOOL - Delegation Pattern")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create specialist agents
    print("🔧 Creating specialist agents...")
    data_analyst, summarizer = create_specialist_agents(retry_config)
    print("✅ Specialist agents created:")
    print("  • DataAnalystAgent - Analyzes numerical data and trends")
    print("  • SummarizerAgent - Creates concise summaries\n")

    # Create coordinator
    print("🤖 Creating coordinator agent...")
    coordinator = create_coordinator_agent(retry_config, data_analyst, summarizer)
    print("✅ Coordinator created with specialist agents as tools\n")

    print("📋 How it works:")
    print("  1. Coordinator receives request")
    print("  2. Coordinator searches for information")
    print("  3. Coordinator calls DataAnalystAgent for numerical analysis")
    print("  4. Coordinator calls SummarizerAgent for summary")
    print("  5. Coordinator presents combined results")
    print("  ℹ️  Coordinator stays in control throughout!\n")

    # Create runner
    runner = InMemoryRunner(agent=coordinator)

    # Test query
    query = "Research the current market capitalization of the top 5 tech companies and summarize the key trends"

    print(f"💬 Query: {query}\n")
    print("-"*80)

    response = await runner.run_debug(query)

    print("-"*80)
    print("\n✅ Research completed!")

    print("\n" + "="*80)
    print("💡 Agent Tools vs Sub-Agents")
    print("="*80)
    print("\nAgent Tools (what we just used):")
    print("  ✅ Agent A calls Agent B as a tool")
    print("  ✅ Agent B's response goes back to Agent A")
    print("  ✅ Agent A stays in control")
    print("  ✅ Use case: Delegation for specific tasks")
    print("\nSub-Agents (different pattern):")
    print("  • Agent A transfers control completely to Agent B")
    print("  • Agent B takes over and handles future input")
    print("  • Use case: Handoff to specialists")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_agent_as_tool()

        # Interactive mode
        print("\n" + "="*80)
        print("🎯 Try Your Own Research Queries")
        print("="*80)
        print("\nWant to try more research queries? (y/n)")
        choice = input("> ").strip().lower()

        if choice == 'y':
            load_api_key()
            retry_config = create_retry_config()
            data_analyst, summarizer = create_specialist_agents(retry_config)
            coordinator = create_coordinator_agent(retry_config, data_analyst, summarizer)
            runner = InMemoryRunner(agent=coordinator)

            print("\nEnter your research requests (type 'exit' to quit):")
            print("Examples:")
            print("  - Research AI adoption rates in healthcare")
            print("  - Analyze renewable energy market trends")
            print("  - What are the latest developments in quantum computing?\n")

            while True:
                query = input("💬 Your request: ").strip()

                if query.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break

                if not query:
                    continue

                print("\n" + "-"*80)
                await runner.run_debug(query)
                print("-"*80 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
