"""
Example 1: Manual Memory Storage

Demonstrates:
- Initialize MemoryService alongside SessionService
- Have conversations stored in sessions
- Manually transfer session data to memory using add_session_to_memory()
- Verify memory storage

Key Pattern:
await memory_service.add_session_to_memory(session)

Run:
python examples/example_1_manual_memory.py
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
from google.genai import types

from utils import (
    load_api_key,
    create_retry_config,
    run_session,
    display_memory_contents,
)

# Configuration
APP_NAME = "ManualMemoryDemo"
USER_ID = "demo_user"


async def demo_manual_memory():
    """
    Demonstrate manual memory storage workflow.

    Steps:
    1. Create agent with session and memory services
    2. Have a conversation (stored in session)
    3. Manually save session to memory
    4. Verify memory contents
    """
    print("\n" + "=" * 80)
    print("Example 1: Manual Memory Storage")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    # Create agent (without memory tools - just basic chat)
    agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="MemoryDemo",
        instruction="Answer user questions in simple words.",
    )

    # Create runner with BOTH services
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("\n✅ Setup complete: Agent, Session Service, and Memory Service ready")

    # Demo 1: First conversation about favorite color
    print("\n" + "-" * 80)
    print("DEMO 1: Store favorite color in session")
    print("-" * 80)

    await run_session(
        runner,
        "My favorite color is blue-green. Can you write a haiku about it?",
        session_id="color-session",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Verify session contains the conversation
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="color-session"
    )

    print(f"\n📝 Session '{session.id}' contains {len(session.events)} events")

    # Demo 2: Manually save to memory
    print("\n" + "-" * 80)
    print("DEMO 2: Manually save session to memory")
    print("-" * 80)

    # This is the KEY operation!
    await memory_service.add_session_to_memory(session)
    print("✅ Session data transferred to memory storage")

    # Demo 3: Verify memory contents
    print("\n" + "-" * 80)
    print("DEMO 3: Verify memory contents")
    print("-" * 80)

    await display_memory_contents(memory_service, APP_NAME, USER_ID)

    # Demo 4: Another conversation about birthday
    print("\n" + "-" * 80)
    print("DEMO 4: Store birthday information")
    print("-" * 80)

    await run_session(
        runner,
        "My birthday is on March 15th.",
        session_id="birthday-session",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Manually save birthday session
    birthday_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session"
    )
    await memory_service.add_session_to_memory(birthday_session)
    print("\n✅ Birthday session saved to memory")

    # Show updated memory contents
    print("\n" + "-" * 80)
    print("Updated memory contents:")
    print("-" * 80)

    await display_memory_contents(memory_service, APP_NAME, USER_ID)

    # Summary
    print("\n" + "=" * 80)
    print("✅ Manual Memory Storage Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("  • Sessions store conversation events (temporary)")
    print("  • Memory stores long-term knowledge")
    print("  • Use add_session_to_memory() to transfer data")
    print("  • Memory persists across different sessions")
    print()
    print("Next: Learn how to retrieve memories with load_memory tool")
    print("  → python examples/example_2_reactive_memory.py")
    print()


if __name__ == "__main__":
    asyncio.run(demo_manual_memory())
