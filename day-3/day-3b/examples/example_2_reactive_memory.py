"""
Example 2: Reactive Memory Retrieval (load_memory tool)

Demonstrates:
- Agent with load_memory tool
- Agent decides when to search memory
- Memory retrieval across different sessions
- More efficient (only searches when needed)

Key Pattern:
tools=[load_memory]  # Agent chooses when to use memory

Run:
python examples/example_2_reactive_memory.py
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
from google.adk.tools import load_memory
from google.genai import types

from utils import (
    load_api_key,
    create_retry_config,
    run_session,
    display_search_results,
)

# Configuration
APP_NAME = "ReactiveMemoryDemo"
USER_ID = "demo_user"


async def demo_reactive_memory():
    """
    Demonstrate reactive memory retrieval with load_memory tool.

    Steps:
    1. Store information in memory
    2. Create agent with load_memory tool
    3. Agent decides when to search memory
    4. Test with questions that need memory vs those that don't
    """
    print("\n" + "=" * 80)
    print("Example 2: Reactive Memory Retrieval (load_memory)")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    # Demo 1: Pre-populate memory with information
    print("\n" + "-" * 80)
    print("DEMO 1: Pre-populate memory with user information")
    print("-" * 80)

    # Create basic agent for storing info
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

    # Store favorite color
    await run_session(
        basic_runner,
        "My favorite color is purple.",
        session_id="store-color",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Save to memory
    color_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="store-color"
    )
    await memory_service.add_session_to_memory(color_session)

    # Store hobby
    await run_session(
        basic_runner,
        "I love playing guitar.",
        session_id="store-hobby",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    hobby_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="store-hobby"
    )
    await memory_service.add_session_to_memory(hobby_session)

    print("\n✅ Memory pre-populated with user preferences")

    # Demo 2: Create agent with load_memory tool
    print("\n" + "-" * 80)
    print("DEMO 2: Create agent with load_memory tool (reactive)")
    print("-" * 80)

    # Agent with load_memory - it decides when to use it!
    memory_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="ReactiveAgent",
        instruction="Answer user questions. Use load_memory tool if you need to recall past conversations.",
        tools=[load_memory],  # Agent can search memory when needed
    )

    memory_runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ Agent with load_memory tool created")

    # Demo 3: Test with question requiring memory
    print("\n" + "-" * 80)
    print("DEMO 3: Ask question requiring memory retrieval")
    print("-" * 80)
    print("Question: What is my favorite color?")
    print("Expected: Agent calls load_memory → retrieves 'purple'")
    print()

    await run_session(
        memory_runner,
        "What is my favorite color?",
        session_id="test-color",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Demo 4: Test with question NOT requiring memory
    print("\n" + "-" * 80)
    print("DEMO 4: Ask question NOT requiring memory")
    print("-" * 80)
    print("Question: What is 2+2?")
    print("Expected: Agent answers directly (no memory search)")
    print()

    await run_session(
        memory_runner,
        "What is 2+2?",
        session_id="test-math",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Demo 5: Another memory-required question
    print("\n" + "-" * 80)
    print("DEMO 5: Ask about hobby")
    print("-" * 80)
    print("Question: What instrument do I play?")
    print("Expected: Agent calls load_memory → retrieves 'guitar'")
    print()

    await run_session(
        memory_runner,
        "What instrument do I play?",
        session_id="test-hobby",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Demo 6: Manual search to verify
    print("\n" + "-" * 80)
    print("DEMO 6: Manual memory search (verification)")
    print("-" * 80)

    await display_search_results(memory_service, APP_NAME, USER_ID, "favorite color")
    await display_search_results(memory_service, APP_NAME, USER_ID, "guitar")

    # Summary
    print("\n" + "=" * 80)
    print("✅ Reactive Memory Retrieval Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("  • load_memory = Reactive pattern")
    print("  • Agent decides when to search memory")
    print("  • More efficient (saves tokens)")
    print("  • Risk: Agent might forget to search")
    print()
    print("Next: Learn proactive memory with preload_memory")
    print("  → python examples/example_3_proactive_memory.py")
    print()


if __name__ == "__main__":
    asyncio.run(demo_reactive_memory())
