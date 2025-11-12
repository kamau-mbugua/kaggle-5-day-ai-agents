"""
Custom Function Tools - Currency Converter Agent
Based on the Kaggle 5-Day Agents Course - Day 2a

This demonstrates how to turn Python functions into agent tools following
ADK best practices: dictionary returns, clear docstrings, type hints, and error handling.

The currency converter agent uses two custom tools:
1. get_fee_for_payment_method - Looks up transaction fees
2. get_exchange_rate - Gets currency conversion rates
"""

import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# Import our custom tools
from tools import get_fee_for_payment_method, get_exchange_rate


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


def create_currency_agent(retry_config):
    """
    Create a currency converter agent with custom function tools.

    The agent uses two custom tools:
    - get_fee_for_payment_method: Looks up company fee structure
    - get_exchange_rate: Gets currency conversion rates

    Both tools follow ADK best practices:
    - Return dictionaries with 'status' field
    - Include clear docstrings for LLM understanding
    - Use type hints for proper schema generation
    - Handle errors gracefully
    """

    agent = LlmAgent(
        name="currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a smart currency conversion assistant.

        For currency conversion requests:
        1. Use `get_fee_for_payment_method()` to find transaction fees
        2. Use `get_exchange_rate()` to get currency conversion rates
        3. Check the "status" field in each tool's response for errors
        4. Calculate the final amount after fees and provide a clear breakdown.
        5. First, state the final converted amount.
           Then, explain how you got that result by showing:
           - The fee percentage and its value in the original currency
           - The amount remaining after the fee
           - The exchange rate used for the final conversion

        If any tool returns status "error", explain the issue to the user clearly.
        """,
        tools=[get_fee_for_payment_method, get_exchange_rate],
    )

    return agent


async def demo_currency_conversion():
    """Demonstrate the currency converter agent."""

    print("\n" + "="*80)
    print("🔧 CUSTOM FUNCTION TOOLS - Currency Converter Agent")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create agent
    print("🤖 Creating currency converter agent...")
    agent = create_currency_agent(retry_config)
    print("✅ Agent created with custom function tools\n")

    print("🔧 Available tools:")
    print("  • get_fee_for_payment_method - Looks up company fee structure")
    print("  • get_exchange_rate - Gets current exchange rates\n")

    # Create runner
    runner = InMemoryRunner(agent=agent)

    # Test queries
    test_queries = [
        "I want to convert 500 US Dollars to Euros using my Platinum Credit Card. How much will I receive?",
        "Convert 1,250 USD to INR using a Bank Transfer. Show me the calculation.",
        "How much will I get if I convert 1000 EUR to USD using a Gold Debit Card?",
    ]

    # Run first query
    query = test_queries[0]
    print(f"💬 Query: {query}\n")
    print("-"*80)

    response = await runner.run_debug(query)

    print("-"*80)
    print("\n✅ Conversion completed!")

    print("\n" + "="*80)
    print("💡 Key Takeaways:")
    print("="*80)
    print("1. Python functions become agent tools automatically")
    print("2. Tools return dictionaries with 'status' for error handling")
    print("3. Clear docstrings help LLMs understand when to use tools")
    print("4. Type hints enable proper schema generation")
    print("5. Agents can call multiple tools to solve complex tasks")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_currency_conversion()

        # Interactive mode
        print("\n" + "="*80)
        print("🎯 Try Your Own Conversions")
        print("="*80)
        print("\nWant to try more conversions? (y/n)")
        choice = input("> ").strip().lower()

        if choice == 'y':
            load_api_key()
            retry_config = create_retry_config()
            agent = create_currency_agent(retry_config)
            runner = InMemoryRunner(agent=agent)

            print("\nEnter your conversion requests (type 'exit' to quit):\n")

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
