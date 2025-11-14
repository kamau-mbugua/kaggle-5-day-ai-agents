"""
Example 2: Debugging Broken Agents

Demonstrates:
- Intentionally create a broken agent
- Use DEBUG logs to identify the root cause
- Follow the debugging workflow: symptom → logs → root cause → fix
- Common agent failure patterns

Key Pattern:
Symptom → Check logs → Find root cause → Fix → Verify

Run:
python examples/example_2_debugging_broken_agent.py
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
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from typing import List

from utils import (
    load_api_key,
    create_retry_config,
    setup_logging,
    cleanup_logs,
    run_agent_with_logging,
    print_log_summary,
)


# Intentionally broken tool - wrong type annotation
def count_papers_broken(papers: str):  # Should be List[str]!
    """
    Count the number of papers in a list.

    Bug: Type annotation says 'str' but we need 'List[str]'
    This will cause type errors when agent passes a list.

    Args:
        papers: Should be List[str], not str

    Returns:
        Number of papers
    """
    return len(papers)


# Fixed tool - correct type annotation
def count_papers_fixed(papers: List[str]):
    """
    Count the number of papers in a list.

    Args:
        papers: A list of paper strings

    Returns:
        Number of papers
    """
    return len(papers)


async def demo_debugging_broken_agent():
    """
    Demonstrate debugging workflow for broken agents.

    Shows:
    1. Create broken agent (intentional bug)
    2. Observe failure symptom
    3. Examine DEBUG logs
    4. Identify root cause
    5. Fix and verify
    """
    print("\n" + "=" * 80)
    print("Example 2: Debugging Broken Agents")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Clean up old logs
    print("\n" + "-" * 80)
    print("SETUP: Prepare debugging environment")
    print("-" * 80)
    cleanup_logs("broken_agent.log", "fixed_agent.log")
    setup_logging("broken_agent.log", logging.DEBUG)

    # Demo 1: Create intentionally broken agent
    print("\n" + "-" * 80)
    print("DEMO 1: Research Paper Finder (Broken Version)")
    print("-" * 80)
    print()
    print("We're building an agent that:")
    print("  1. Searches for research papers")
    print("  2. Counts the papers found")
    print()
    print("But we've introduced a bug... 🐛")
    print()

    # Google search agent
    google_search_agent = LlmAgent(
        name="google_search_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Searches for information using Google search",
        instruction="Use the google_search tool to find information. Return raw search results as a list.",
        tools=[google_search],
    )

    # Broken root agent
    broken_research_agent = LlmAgent(
        name="research_paper_finder",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Find research papers and count them.

        Steps:
        1) Use 'google_search_agent' to find papers
        2) Pass the papers list to 'count_papers' tool
        3) Return both the list and count
        """,
        tools=[AgentTool(agent=google_search_agent), count_papers_broken],
    )

    runner = InMemoryRunner(agent=broken_research_agent)

    print("Running broken agent...")
    await run_agent_with_logging(
        runner,
        "Find recent quantum computing papers",
    )

    # Demo 2: Analyze the failure
    print("\n" + "-" * 80)
    print("DEMO 2: Analyze the Failure")
    print("-" * 80)
    print()
    print("🔍 SYMPTOM: Agent returned unexpected count")
    print()
    print("Let's examine the DEBUG logs to find the root cause...")
    print()

    print_log_summary("broken_agent.log", max_lines=30)

    # Demo 3: Identify root cause
    print("\n" + "-" * 80)
    print("DEMO 3: Root Cause Analysis")
    print("-" * 80)
    print()
    print("🎯 DEBUGGING WORKFLOW:")
    print()
    print("  Step 1: Symptom → Count is suspiciously high")
    print()
    print("  Step 2: Check Logs → Search for 'count_papers'")
    print()
    print("  Step 3: Find LLM Request → Look at function call")
    print()
    print("  Step 4: Root Cause → Type mismatch!")
    print("          • count_papers expects: str")
    print("          • Agent passes: List[str]")
    print("          • Result: len() counts characters, not items!")
    print()
    print("  Step 5: Fix → Change type annotation to List[str]")
    print()

    # Demo 4: Fix and verify
    print("\n" + "-" * 80)
    print("DEMO 4: Fix and Verify")
    print("-" * 80)
    print()
    print("Applying fix: count_papers_broken → count_papers_fixed")
    print()

    setup_logging("fixed_agent.log", logging.DEBUG)

    # Fixed agent
    fixed_research_agent = LlmAgent(
        name="research_paper_finder",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Find research papers and count them.

        Steps:
        1) Use 'google_search_agent' to find papers
        2) Pass the papers list to 'count_papers' tool
        3) Return both the list and count
        """,
        tools=[AgentTool(agent=google_search_agent), count_papers_fixed],
    )

    runner = InMemoryRunner(agent=fixed_research_agent)

    print("Running fixed agent...")
    await run_agent_with_logging(
        runner,
        "Find recent quantum computing papers",
    )

    print("\n✅ Agent now works correctly!")
    print_log_summary("fixed_agent.log", max_lines=20)

    # Demo 5: Common failure patterns
    print("\n" + "-" * 80)
    print("DEMO 5: Common Agent Failure Patterns")
    print("-" * 80)
    print()
    print("┌─────────────────────────────┬──────────────────────────────────┐")
    print("│ Symptom                     │ Root Cause                       │")
    print("├─────────────────────────────┼──────────────────────────────────┤")
    print("│ Agent says 'cannot help'    │ Missing tool in tools list       │")
    print("│ Wrong results               │ Type mismatch in tool args       │")
    print("│ Agent loops forever         │ Ambiguous instructions           │")
    print("│ Tool not called             │ Poor tool description            │")
    print("│ Timeout errors              │ Infinite recursion               │")
    print("└─────────────────────────────┴──────────────────────────────────┘")
    print()

    # Summary
    print("=" * 80)
    print("✅ Debugging Complete!")
    print("=" * 80)
    print()
    print("The Core Debugging Pattern:")
    print()
    print("  1. Symptom    → What went wrong?")
    print("  2. Logs       → Check DEBUG logs")
    print("  3. Root Cause → Trace execution flow")
    print("  4. Fix        → Apply correction")
    print("  5. Verify     → Test with same input")
    print()
    print("Key Skills Learned:")
    print()
    print("  ✅ Read and interpret DEBUG logs")
    print("  ✅ Trace agent execution flow")
    print("  ✅ Identify type mismatches")
    print("  ✅ Verify fixes with logging")
    print()
    print("Next: Production logging with LoggingPlugin")
    print("  → python examples/example_3_production_logging.py")
    print()


if __name__ == "__main__":
    asyncio.run(demo_debugging_broken_agent())
