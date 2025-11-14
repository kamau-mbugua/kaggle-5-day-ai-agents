"""
Example 3: Production Logging with LoggingPlugin

Demonstrates:
- ADK's built-in LoggingPlugin for production observability
- Automatic capture of agent activity
- Structured logging output
- When to use LoggingPlugin vs custom solutions

Key Pattern:
runner = InMemoryRunner(
    agent=agent,
    plugins=[LoggingPlugin()]  # Automatic observability!
)

Run:
python examples/example_3_production_logging.py
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.tools.google_search_tool import google_search
from typing import List

from utils import (
    load_api_key,
    create_retry_config,
    cleanup_logs,
)


def count_papers(papers: List[str]) -> int:
    """Count the number of papers in a list."""
    return len(papers)


async def demo_production_logging():
    """
    Demonstrate production observability with LoggingPlugin.

    Shows:
    1. What LoggingPlugin captures automatically
    2. How to configure it for production
    3. Reading structured log output
    4. When to use LoggingPlugin vs manual logging
    """
    print("\n" + "=" * 80)
    print("Example 3: Production Logging with LoggingPlugin")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    cleanup_logs("production.log")

    # Demo 1: What is LoggingPlugin?
    print("\n" + "-" * 80)
    print("DEMO 1: Understanding LoggingPlugin")
    print("-" * 80)
    print()
    print("LoggingPlugin is ADK's built-in solution for production observability.")
    print()
    print("Automatically captures:")
    print("  🚀 User messages and agent responses")
    print("  ⏱️  Timing data for performance analysis")
    print("  🧠 LLM requests and responses")
    print("  🔧 Tool calls and results")
    print("  ✅ Complete execution traces")
    print()
    print("Zero configuration needed - just add to plugins list!")
    print()

    # Demo 2: Create agent with LoggingPlugin
    print("-" * 80)
    print("DEMO 2: Agent with LoggingPlugin")
    print("-" * 80)
    print()

    # Create search agent
    search_agent = LlmAgent(
        name="research_assistant",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="Use google_search to find research papers. Return concise results.",
        tools=[google_search, count_papers],
    )

    # Create runner with LoggingPlugin
    runner = InMemoryRunner(
        agent=search_agent,
        plugins=[LoggingPlugin()],  # This line enables comprehensive logging!
    )

    print("✅ Runner configured with LoggingPlugin")
    print()
    print("What happens now:")
    print("  • Every agent invocation is logged")
    print("  • Every tool call is logged")
    print("  • Every LLM request/response is logged")
    print("  • Everything happens automatically!")
    print()

    # Demo 3: Run agent and observe logging
    print("-" * 80)
    print("DEMO 3: Watch LoggingPlugin in Action")
    print("-" * 80)
    print()
    print("Running: 'Find papers on machine learning'")
    print()
    print("📊 Observe the structured logging output below:")
    print("=" * 80)
    print()

    response = await runner.run_debug("Find papers on machine learning")

    print()
    print("=" * 80)
    print()
    print("✅ Agent completed successfully")
    print(f"Response: {response[:200]}...")
    print()

    # Demo 4: Analyze logging output
    print("-" * 80)
    print("DEMO 4: Understanding the Log Output")
    print("-" * 80)
    print()
    print("LoggingPlugin generates structured logs with:")
    print()
    print("  [logging_plugin] 🚀 USER MESSAGE RECEIVED")
    print("    • Invocation ID (unique request identifier)")
    print("    • Session ID, User ID, App Name")
    print("    • Root agent name")
    print("    • User message content")
    print()
    print("  [logging_plugin] 🧠 LLM REQUEST")
    print("    • Model name")
    print("    • System instructions")
    print("    • Available tools")
    print()
    print("  [logging_plugin] 🧠 LLM RESPONSE")
    print("    • Model output")
    print("    • Token usage (input/output)")
    print()
    print("  [logging_plugin] 🔧 TOOL STARTING/COMPLETED")
    print("    • Tool name")
    print("    • Function arguments")
    print("    • Tool results")
    print()
    print("  [logging_plugin] ✅ INVOCATION COMPLETED")
    print("    • Final status")
    print("    • Total execution time")
    print()

    # Demo 5: Multiple queries to show consistency
    print("-" * 80)
    print("DEMO 5: Consistent Logging Across Queries")
    print("-" * 80)
    print()
    print("Running multiple queries to demonstrate consistent logging...")
    print()

    queries = [
        "What is quantum computing?",
        "Count the papers about AI",
        "Search for Python tutorials",
    ]

    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        await runner.run_debug(query)
        print()

    print("✅ All queries logged automatically!")
    print()

    # Demo 6: Production use cases
    print("-" * 80)
    print("DEMO 6: Production Use Cases")
    print("-" * 80)
    print()
    print("When to use LoggingPlugin:")
    print()
    print("  ✅ Production deployments")
    print("  ✅ Automated testing")
    print("  ✅ Performance monitoring")
    print("  ✅ Debugging production issues")
    print("  ✅ Audit trails")
    print()
    print("When NOT to use LoggingPlugin:")
    print()
    print("  ❌ Custom metrics needed")
    print("  ❌ Integration with external systems")
    print("  ❌ Special formatting requirements")
    print("  ❌ Selective logging (only certain events)")
    print()
    print("For these cases → Use Custom Plugins (Example 4)")
    print()

    # Demo 7: Configuration options
    print("-" * 80)
    print("DEMO 7: LoggingPlugin Configuration")
    print("-" * 80)
    print()
    print("Basic usage:")
    print()
    print("  plugins=[LoggingPlugin()]  # Default configuration")
    print()
    print("The plugin automatically:")
    print("  • Formats logs with timestamps")
    print("  • Adds context (agent name, invocation ID)")
    print("  • Includes emojis for readability")
    print("  • Captures all standard events")
    print()

    # Summary
    print("=" * 80)
    print("✅ Production Logging Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print()
    print("  ✅ LoggingPlugin = Zero-config observability")
    print("  ✅ Captures everything automatically")
    print("  ✅ Structured, consistent output")
    print("  ✅ Perfect for standard production needs")
    print()
    print("Decision Matrix:")
    print()
    print("┌─────────────────────────────┬──────────────────────────────┐")
    print("│ Use LoggingPlugin When      │ Use Custom Plugin When       │")
    print("├─────────────────────────────┼──────────────────────────────┤")
    print("│ Standard observability      │ Custom metrics tracking      │")
    print("│ Quick production setup      │ External system integration  │")
    print("│ Debugging issues            │ Special formatting needs     │")
    print("│ Audit trails                │ Selective event logging      │")
    print("└─────────────────────────────┴──────────────────────────────┘")
    print()
    print("Next: Learn to build custom plugins")
    print("  → python examples/example_4_custom_plugins.py")
    print()


if __name__ == "__main__":
    asyncio.run(demo_production_logging())
