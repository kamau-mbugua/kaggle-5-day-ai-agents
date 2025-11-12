"""
Code Execution - Enhanced Currency Converter
Based on the Kaggle 5-Day Agents Course - Day 2a

This demonstrates how to improve agent reliability using code execution.
Instead of asking the LLM to do math (unreliable), we have it generate Python
code and execute it for precise calculations.

Enhanced workflow:
1. Agent uses custom tools to get fees and rates
2. Agent generates Python code for calculations
3. BuiltInCodeExecutor runs the code for precise results
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
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor
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


def show_python_code_and_result(response):
    """Helper function to extract and display generated Python code and results."""
    print("\n📊 Generated Code & Results:")
    print("="*80)

    for i in range(len(response)):
        # Check if the response contains a valid function call result
        if (
            (response[i].content.parts)
            and (response[i].content.parts[0])
            and (response[i].content.parts[0].function_response)
            and (response[i].content.parts[0].function_response.response)
        ):
            response_code = response[i].content.parts[0].function_response.response
            if "result" in response_code and response_code["result"] != "```":
                if "tool_code" in response_code["result"]:
                    code = response_code["result"].replace("tool_code", "")
                    print("🐍 Python Code Generated:")
                    print("-"*80)
                    print(code)
                    print("-"*80)
                else:
                    print("📈 Code Execution Result:")
                    print(response_code["result"])

    print("="*80)


def create_calculation_agent(retry_config):
    """
    Create a specialized calculator agent that ONLY generates and executes Python code.

    This agent uses BuiltInCodeExecutor to run code in a sandbox, providing:
    - Reliable mathematical calculations (no LLM math errors)
    - Repeatable results
    - Clear computational logic
    """

    agent = LlmAgent(
        name="CalculationAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized calculator that ONLY responds with Python code.

        Your task is to take a request for a calculation and translate it into a single
        block of Python code that calculates the answer.

        **RULES:**
        1. Your output MUST be ONLY a Python code block.
        2. Do NOT write any text before or after the code block.
        3. The Python code MUST calculate the result.
        4. The Python code MUST print the final result to stdout.
        5. You are PROHIBITED from performing the calculation yourself.
           Your only job is to generate the code that will perform the calculation.

        Failure to follow these rules will result in an error.
        """,
        code_executor=BuiltInCodeExecutor(),  # Enables code execution
    )

    return agent


def create_enhanced_currency_agent(retry_config, calculation_agent):
    """
    Create an enhanced currency converter that uses a calculation agent for math.

    This agent:
    1. Uses custom tools to get fees and rates
    2. Delegates calculations to the calculation_agent (an Agent Tool)
    3. Provides detailed breakdowns with precise calculations
    """

    agent = LlmAgent(
        name="enhanced_currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a smart currency conversion assistant.
        You must strictly follow these steps and use the available tools.

        For any currency conversion request:

        1. Get Transaction Fee: Use get_fee_for_payment_method() to determine the fee.
        2. Get Exchange Rate: Use get_exchange_rate() to get the conversion rate.
        3. Error Check: After each tool call, check the "status" field.
           If status is "error", stop and explain the issue to the user.
        4. Calculate Final Amount (CRITICAL): You are strictly PROHIBITED from
           performing arithmetic calculations yourself. You MUST use the
           calculation_agent tool to generate Python code that calculates the
           final converted amount using the fee and rate from steps 1 and 2.
        5. Provide Detailed Breakdown: In your summary, state:
           * The final converted amount
           * How the result was calculated:
             - Fee percentage and fee amount in original currency
             - Amount remaining after deducting the fee
             - Exchange rate applied
        """,
        tools=[
            get_fee_for_payment_method,
            get_exchange_rate,
            AgentTool(agent=calculation_agent),  # Using another agent as a tool!
        ],
    )

    return agent


async def demo_code_execution():
    """Demonstrate code execution for reliable calculations."""

    print("\n" + "="*80)
    print("🐍 CODE EXECUTION - Enhanced Currency Converter")
    print("="*80 + "\n")

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create agents
    print("🤖 Creating calculation agent (specialist)...")
    calculation_agent = create_calculation_agent(retry_config)
    print("✅ Calculation agent created with BuiltInCodeExecutor\n")

    print("🤖 Creating enhanced currency agent (coordinator)...")
    agent = create_enhanced_currency_agent(retry_config, calculation_agent)
    print("✅ Enhanced currency agent created\n")

    print("🔧 Tool types used:")
    print("  • Function Tools (fees, rates)")
    print("  • Agent Tool (calculation specialist)")
    print("  • BuiltInCodeExecutor (Python code execution)\n")

    # Create runner
    runner = InMemoryRunner(agent=agent)

    # Test query
    query = "Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation."

    print(f"💬 Query: {query}\n")
    print("-"*80)

    response = await runner.run_debug(query)

    print("-"*80)

    # Show generated code and results
    show_python_code_and_result(response)

    print("\n✅ Enhanced conversion completed!")

    print("\n" + "="*80)
    print("💡 Key Takeaways:")
    print("="*80)
    print("1. LLMs can make math errors - code execution is more reliable")
    print("2. Agent Tools let you use one agent as a tool in another")
    print("3. BuiltInCodeExecutor runs Python code in a sandbox")
    print("4. Generated code is visible and auditable")
    print("5. Calculations are precise and repeatable")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_code_execution()

        # Interactive mode
        print("\n" + "="*80)
        print("🎯 Try Your Own Conversions with Code Execution")
        print("="*80)
        print("\nWant to try more conversions? (y/n)")
        choice = input("> ").strip().lower()

        if choice == 'y':
            load_api_key()
            retry_config = create_retry_config()
            calculation_agent = create_calculation_agent(retry_config)
            agent = create_enhanced_currency_agent(retry_config, calculation_agent)
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
                response = await runner.run_debug(query)
                print("-"*80)
                show_python_code_and_result(response)
                print()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
