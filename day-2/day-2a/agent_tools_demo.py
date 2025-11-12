"""
Agent Tools - Interactive Demo
Based on the Kaggle 5-Day Agents Course - Day 2a

Explore all agent tool patterns in one place:
1. Custom Function Tools - Turn Python functions into agent tools
2. Code Execution - Use BuiltInCodeExecutor for reliable calculations
3. Agent as Tool - Use specialist agents within coordinator agents
"""

import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types

from tools import get_fee_for_payment_method, get_exchange_rate


def load_api_key():
    """Load API key from environment."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found. Create a .env file with your API key.\n"
            "Get your key from: https://aistudio.google.com/app/apikey"
        )
    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


def create_retry_config():
    """Create retry configuration."""
    return types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )


# Pattern 1: Custom Function Tools
def create_currency_agent(retry_config):
    """Create currency converter with custom function tools."""
    return LlmAgent(
        name="currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Currency conversion assistant. Use get_fee_for_payment_method()
        and get_exchange_rate(). Check 'status' field. Calculate and explain breakdown.""",
        tools=[get_fee_for_payment_method, get_exchange_rate],
    )


# Pattern 2: Code Execution
def create_calculation_agent(retry_config):
    """Create calculator agent with code execution."""
    return LlmAgent(
        name="CalculationAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Generate ONLY Python code for calculations. No text.
        Code must print result.""",
        code_executor=BuiltInCodeExecutor(),
    )


def create_enhanced_currency_agent(retry_config, calculation_agent):
    """Create enhanced currency agent with code execution."""
    return LlmAgent(
        name="enhanced_currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Currency conversion assistant. Get fees and rates.
        Use calculation_agent for precise math. Provide detailed breakdown.""",
        tools=[
            get_fee_for_payment_method,
            get_exchange_rate,
            AgentTool(agent=calculation_agent),
        ],
    )


# Pattern 3: Agent as Tool
def create_specialist_agents(retry_config):
    """Create specialist agents."""
    data_analyst = LlmAgent(
        name="DataAnalystAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Data analyst. Analyze numerical data, identify trends,
        calculate metrics.""",
    )

    summarizer = LlmAgent(
        name="SummarizerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Summarizer. Create concise bullet summaries (3-5 points).""",
    )

    return data_analyst, summarizer


def create_coordinator_agent(retry_config, data_analyst, summarizer):
    """Create coordinator agent."""
    return LlmAgent(
        name="ResearchCoordinator",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research coordinator. Use google_search, DataAnalystAgent
        for data, SummarizerAgent for summaries.""",
        tools=[
            google_search,
            AgentTool(agent=data_analyst),
            AgentTool(agent=summarizer),
        ],
    )


def print_menu():
    """Display main menu."""
    print("\n" + "="*80)
    print("🧰 AGENT TOOLS - Interactive Demo")
    print("="*80)
    print("\nChoose a tool pattern to explore:\n")
    print("  1️⃣  Custom Function Tools    - Currency converter with custom tools")
    print("  2️⃣  Code Execution           - Enhanced converter with reliable calculations")
    print("  3️⃣  Agent as Tool            - Research coordinator with specialists")
    print("  4️⃣  Exit\n")
    print("="*80)


async def run_pattern(pattern_choice, retry_config):
    """Run the selected pattern."""

    if pattern_choice == "1":
        print("\n🔧 Running Custom Function Tools...")
        agent = create_currency_agent(retry_config)
        prompt = "Convert 500 USD to EUR using Platinum Credit Card"

    elif pattern_choice == "2":
        print("\n🐍 Running Code Execution...")
        calc_agent = create_calculation_agent(retry_config)
        agent = create_enhanced_currency_agent(retry_config, calc_agent)
        prompt = "Convert 1,250 USD to INR using Bank Transfer with precise calculation"

    elif pattern_choice == "3":
        print("\n🤖 Running Agent as Tool...")
        data_analyst, summarizer = create_specialist_agents(retry_config)
        agent = create_coordinator_agent(retry_config, data_analyst, summarizer)
        prompt = "Research top 5 tech companies market cap and summarize trends"

    else:
        print("❌ Invalid choice!")
        return

    print(f"📝 Prompt: {prompt}\n")
    print("-"*80)

    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(prompt)

    print("-"*80)
    print("\n✅ Complete!\n")


async def main():
    """Main function."""
    print("\n🚀 Welcome to Agent Tools Demo!")

    try:
        load_api_key()
        print("✅ API key loaded successfully.")
    except Exception as e:
        print(f"\n{e}")
        return

    retry_config = create_retry_config()

    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "4":
            print("\n👋 Goodbye!\n")
            break

        if choice in ["1", "2", "3"]:
            try:
                await run_pattern(choice, retry_config)
                input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\n\n⏸️  Operation cancelled.\n")
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
        else:
            print("❌ Invalid choice! Please enter 1-4.\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
