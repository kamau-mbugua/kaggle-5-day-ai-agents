"""
Example 1: Basic Logging Setup

Demonstrates:
- Configure logging with different log levels (DEBUG, INFO, WARNING, ERROR)
- Understanding what each log level captures
- How to read and interpret log files
- When to use each logging level

Key Pattern:
logging.basicConfig(level=logging.DEBUG)  # Captures everything

Run:
python examples/example_1_basic_logging.py
"""

import asyncio
import sys
import os
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools.google_search_tool import google_search

from utils import (
    load_api_key,
    create_retry_config,
    setup_logging,
    cleanup_logs,
    run_agent_with_logging,
    print_log_summary,
)


async def demo_basic_logging():
    """
    Demonstrate basic logging configuration and usage.

    Shows:
    1. Different log levels (DEBUG, INFO, WARNING, ERROR)
    2. What information each level captures
    3. How to configure logging for development vs production
    """
    print("\n" + "=" * 80)
    print("Example 1: Basic Logging Setup")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Clean up old logs
    print("\n" + "-" * 80)
    print("SETUP: Cleaning up old log files")
    print("-" * 80)
    cleanup_logs("debug.log", "info.log", "warning.log", "error.log")

    # Demo 1: DEBUG level logging (most verbose)
    print("\n" + "-" * 80)
    print("DEMO 1: DEBUG Level Logging (Development)")
    print("-" * 80)
    print()
    print("DEBUG level captures:")
    print("  • Full LLM requests (system instructions, tools)")
    print("  • Complete LLM responses")
    print("  • Tool call arguments and results")
    print("  • Internal state transitions")
    print("  • Everything that happens under the hood")
    print()
    print("Use case: Development, debugging, troubleshooting")
    print()

    setup_logging("debug.log", logging.DEBUG)

    # Create simple search agent
    search_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="SearchAgent",
        instruction="Use google_search to find information.",
        tools=[google_search],
    )

    runner = InMemoryRunner(agent=search_agent)

    await run_agent_with_logging(
        runner,
        "What is quantum computing?",
    )

    print("\n✅ Check debug.log for detailed logs")
    print_log_summary("debug.log", max_lines=20)

    # Demo 2: INFO level logging (standard)
    print("\n" + "-" * 80)
    print("DEMO 2: INFO Level Logging (Production)")
    print("-" * 80)
    print()
    print("INFO level captures:")
    print("  • Agent starts and completions")
    print("  • Tool invocations")
    print("  • Major events and milestones")
    print("  • High-level execution flow")
    print()
    print("Use case: Production monitoring, general observability")
    print()

    setup_logging("info.log", logging.INFO)

    runner = InMemoryRunner(agent=search_agent)

    await run_agent_with_logging(
        runner,
        "What is the capital of France?",
    )

    print("\n✅ Check info.log for standard logs")
    print_log_summary("info.log", max_lines=15)

    # Demo 3: WARNING level logging
    print("\n" + "-" * 80)
    print("DEMO 3: WARNING Level Logging")
    print("-" * 80)
    print()
    print("WARNING level captures:")
    print("  • Potential issues (slow responses, retries)")
    print("  • Deprecated features")
    print("  • Non-critical errors")
    print()
    print("Use case: Monitoring for potential problems")
    print()

    setup_logging("warning.log", logging.WARNING)

    runner = InMemoryRunner(agent=search_agent)

    await run_agent_with_logging(
        runner,
        "Hello",
    )

    print("\n✅ Check warning.log")
    print_log_summary("warning.log", max_lines=10)

    # Demo 4: ERROR level logging
    print("\n" + "-" * 80)
    print("DEMO 4: ERROR Level Logging")
    print("-" * 80)
    print()
    print("ERROR level captures:")
    print("  • Exception messages")
    print("  • Stack traces")
    print("  • Critical failures")
    print()
    print("Use case: Alerting, incident response")
    print()

    setup_logging("error.log", logging.ERROR)

    # This will generate errors to demonstrate ERROR logging
    broken_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="BrokenAgent",
        instruction="This is a test agent.",
        tools=[],  # No tools - will fail for certain queries
    )

    runner = InMemoryRunner(agent=broken_agent)

    await run_agent_with_logging(
        runner,
        "Search for Python tutorials",  # Will fail - no search tool
    )

    print("\n✅ Check error.log")
    print_log_summary("error.log", max_lines=10)

    # Summary comparison
    print("\n" + "=" * 80)
    print("Log Level Comparison")
    print("=" * 80)
    print()
    print("┌─────────────┬──────────────────────────┬─────────────────────────┐")
    print("│ Level       │ What It Captures         │ When to Use             │")
    print("├─────────────┼──────────────────────────┼─────────────────────────┤")
    print("│ DEBUG       │ Everything (verbose)     │ Development, debugging  │")
    print("│ INFO        │ Key events, flow         │ Production monitoring   │")
    print("│ WARNING     │ Potential issues         │ Problem detection       │")
    print("│ ERROR       │ Failures, exceptions     │ Incident response       │")
    print("└─────────────┴──────────────────────────┴─────────────────────────┘")
    print()

    # Best practices
    print("=" * 80)
    print("✅ Basic Logging Complete!")
    print("=" * 80)
    print()
    print("Best Practices:")
    print()
    print("  ✅ Development: Use DEBUG level to see everything")
    print("  ✅ Production: Use INFO level for monitoring")
    print("  ✅ Alerts: Monitor WARNING and ERROR levels")
    print("  ✅ Storage: Rotate log files to prevent disk issues")
    print()
    print("Next: Learn to debug broken agents with logs")
    print("  → python examples/example_2_debugging_broken_agent.py")
    print()


if __name__ == "__main__":
    asyncio.run(demo_basic_logging())
