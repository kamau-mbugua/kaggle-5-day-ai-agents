"""
Simple AI Agent with Google ADK
Based on the Kaggle 5-Day Agents Course - Day 1

This script demonstrates how to create and run a basic AI agent
that can use Google Search to answer questions.
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types


def load_api_key():
    """Load the Google API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found in environment variables.\n"
            "Please create a .env file with your API key or set it as an environment variable.\n"
            "Get your API key from: https://aistudio.google.com/app/apikey"
        )

    os.environ["GOOGLE_API_KEY"] = api_key
    print("✅ Gemini API key loaded successfully.")
    return api_key


def create_retry_config():
    """Create retry configuration for handling transient errors."""
    return types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,  # Initial delay before first retry (in seconds)
        http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
    )


def create_agent(retry_config):
    """Create and configure the AI agent with tools."""
    agent = Agent(
        name="helpful_assistant",
        model=Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        description="A simple agent that can answer general questions.",
        instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
        tools=[google_search],
    )
    print("✅ Agent created successfully.")
    return agent


async def run_agent_query(runner, query):
    """Run a query through the agent and display the response."""
    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print(f"{'='*80}\n")

    response = await runner.run_debug(query)

    print(f"\n{'='*80}")
    print("✅ Query completed successfully!")
    print(f"{'='*80}\n")


async def main():
    """Main function to set up and run the agent."""
    print("\n🚀 Starting AI Agent with Google ADK\n")

    # 1. Load API key
    load_api_key()

    # 2. Configure retry options
    print("\n📋 Configuring retry options...")
    retry_config = create_retry_config()
    print("✅ Retry configuration created.")

    # 3. Create agent
    print("\n🤖 Creating AI agent...")
    agent = create_agent(retry_config)

    # 4. Create runner
    print("\n⚙️  Creating runner...")
    runner = InMemoryRunner(agent=agent)
    print("✅ Runner created successfully.")

    # 5. Run example queries
    print("\n" + "="*80)
    print("Running Example Queries")
    print("="*80)

    # Example 1: Ask about ADK
    await run_agent_query(
        runner,
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )

    # Example 2: Ask about current information
    await run_agent_query(
        runner,
        "What's the weather in London?"
    )

    # Interactive mode
    print("\n" + "="*80)
    print("Interactive Mode")
    print("="*80)
    print("You can now ask your own questions. Type 'exit' or 'quit' to end.\n")

    while True:
        try:
            user_query = input("Your question: ").strip()

            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not user_query:
                print("Please enter a question.\n")
                continue

            await run_agent_query(runner, user_query)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
