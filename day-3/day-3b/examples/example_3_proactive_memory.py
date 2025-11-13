"""
Example 3: Proactive Memory Retrieval (preload_memory tool)

Demonstrates:
- Agent with preload_memory tool
- Automatic memory loading before every turn
- Guaranteed memory context (no forgetting)
- Trade-off: Less efficient but more reliable

Key Pattern:
tools=[preload_memory]  # Automatic memory loading

Run:
python examples/example_3_proactive_memory.py
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import preload_memory
from google.genai import types

from utils import (
    load_api_key,
    create_retry_config,
    run_session,
    display_memory_contents,
)

# Configuration
APP_NAME = "ProactiveMemoryDemo"
USER_ID = "demo_user"


async def demo_proactive_memory():
    """
    Demonstrate proactive memory retrieval with preload_memory tool.

    Steps:
    1. Store information in memory
    2. Create agent with preload_memory tool
    3. Memory automatically loaded before every turn
    4. Compare with reactive approach
    """
    print("\n" + "=" * 80)
    print("Example 3: Proactive Memory Retrieval (preload_memory)")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    # Demo 1: Pre-populate memory
    print("\n" + "-" * 80)
    print("DEMO 1: Pre-populate memory with user information")
    print("-" * 80)

    # Create basic agent for storing
    basic_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="BasicAgent",
        instruction="Answer user questions.",
    )

    basic_runner = Runner(
        agent=basic_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    # Store multiple pieces of information
    conversations = [
        ("My name is Alex.", "store-name"),
        ("I live in Portland, Oregon.", "store-location"),
        ("I'm a software engineer.", "store-job"),
    ]

    for query, session_id in conversations:
        await run_session(
            basic_runner,
            query,
            session_id=session_id,
            user_id=USER_ID,
            app_name=APP_NAME,
            session_service=session_service,
        )

        # Save each to memory
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
        await memory_service.add_session_to_memory(session)

    print("\n✅ Memory pre-populated with 3 pieces of information")

    # Show memory contents
    await display_memory_contents(memory_service, APP_NAME, USER_ID)

    # Demo 2: Create agent with preload_memory
    print("\n" + "-" * 80)
    print("DEMO 2: Create agent with preload_memory (proactive)")
    print("-" * 80)

    # Agent with preload_memory - automatic loading!
    proactive_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="ProactiveAgent",
        instruction="Answer user questions using available information.",
        tools=[preload_memory],  # Automatically loads memory every turn!
    )

    proactive_runner = Runner(
        agent=proactive_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ Agent with preload_memory tool created")
    print("   → Memory will be automatically loaded before EVERY turn")

    # Demo 3: Test multiple questions in NEW session
    print("\n" + "-" * 80)
    print("DEMO 3: Test multiple questions (new session)")
    print("-" * 80)
    print("All questions in a DIFFERENT session from where info was stored")
    print()

    questions = [
        "What is my name?",
        "Where do I live?",
        "What is my job?",
        "Tell me everything you know about me.",
    ]

    for i, question in enumerate(questions):
        await run_session(
            proactive_runner,
            question,
            session_id=f"test-{i+1}",
            user_id=USER_ID,
            app_name=APP_NAME,
            session_service=session_service,
        )

    # Demo 4: Compare with math question
    print("\n" + "-" * 80)
    print("DEMO 4: Non-memory question")
    print("-" * 80)
    print("Question: What is 5 x 7?")
    print("Note: Memory still loaded, even though not needed")
    print()

    await run_session(
        proactive_runner,
        "What is 5 x 7?",
        session_id="test-math",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Summary
    print("\n" + "=" * 80)
    print("✅ Proactive Memory Retrieval Complete!")
    print("=" * 80)
    print()
    print("Reactive (load_memory) vs Proactive (preload_memory):")
    print()
    print("┌─────────────────────┬──────────────────┬────────────────────┐")
    print("│ Aspect              │ load_memory      │ preload_memory     │")
    print("├─────────────────────┼──────────────────┼────────────────────┤")
    print("│ When it searches    │ Agent decides    │ Every turn         │")
    print("│ Efficiency          │ More efficient   │ Less efficient     │")
    print("│ Reliability         │ Might forget     │ Guaranteed context │")
    print("│ Use case            │ Smart agents     │ Critical memory    │")
    print("└─────────────────────┴──────────────────┴────────────────────┘")
    print()
    print("Next: Learn automated memory storage with callbacks")
    print("  → python examples/example_4_automated_memory.py")
    print()


if __name__ == "__main__":
    asyncio.run(demo_proactive_memory())
