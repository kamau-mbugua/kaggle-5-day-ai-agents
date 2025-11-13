"""
Example 4: Automated Memory Storage with Callbacks

Demonstrates:
- Callback system for automatic memory storage
- after_agent_callback to save after each turn
- Combining automated storage with preload_memory
- Zero-intervention memory management

Key Pattern:
after_agent_callback=auto_save_callback  # Automatic saving!

Run:
python examples/example_4_automated_memory.py
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
APP_NAME = "AutomatedMemoryDemo"
USER_ID = "demo_user"


async def auto_save_to_memory(callback_context):
    """
    Callback function to automatically save session to memory.

    This function is called after each agent turn.
    It accesses the memory service and current session from callback_context.

    Args:
        callback_context: Automatically provided by ADK containing runtime info
    """
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


async def demo_automated_memory():
    """
    Demonstrate automated memory management with callbacks.

    Steps:
    1. Create callback function for auto-saving
    2. Create agent with callback + preload_memory
    3. Have conversations - automatic storage + retrieval
    4. Verify zero-intervention workflow
    """
    print("\n" + "=" * 80)
    print("Example 4: Automated Memory with Callbacks")
    print("=" * 80)

    # Setup
    load_api_key()
    retry_config = create_retry_config()

    # Create services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    # Demo 1: Create agent with automated memory
    print("\n" + "-" * 80)
    print("DEMO 1: Create agent with automated memory management")
    print("-" * 80)

    # Agent with BOTH automated storage AND retrieval!
    automated_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="AutomatedAgent",
        instruction="Answer user questions and remember what users tell you.",
        tools=[preload_memory],  # Automatic retrieval
        after_agent_callback=auto_save_to_memory,  # Automatic storage!
    )

    automated_runner = Runner(
        agent=automated_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    print("✅ Agent created with:")
    print("   → preload_memory (automatic retrieval)")
    print("   → after_agent_callback (automatic storage)")
    print("   → Zero manual intervention required!")

    # Demo 2: First conversation
    print("\n" + "-" * 80)
    print("DEMO 2: First conversation - Tell agent about gift")
    print("-" * 80)
    print("What happens:")
    print("  1. User tells about gift")
    print("  2. Agent responds")
    print("  3. Callback automatically saves to memory ✨")
    print()

    await run_session(
        automated_runner,
        "I gifted a new toy car to my nephew on his 1st birthday!",
        session_id="gift-conversation",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("\n✅ Conversation complete - memory automatically saved!")

    # Verify memory
    await display_memory_contents(memory_service, APP_NAME, USER_ID, max_display=5)

    # Demo 3: Second conversation (NEW session)
    print("\n" + "-" * 80)
    print("DEMO 3: Second conversation - Ask about the gift")
    print("-" * 80)
    print("What happens:")
    print("  1. preload_memory automatically loads past memories ✨")
    print("  2. Agent recalls the gift information")
    print("  3. Agent answers correctly")
    print("  4. This conversation also saved to memory ✨")
    print()

    await run_session(
        automated_runner,
        "What did I gift my nephew?",
        session_id="recall-conversation",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Demo 4: Third conversation - Additional info
    print("\n" + "-" * 80)
    print("DEMO 4: Third conversation - Add more information")
    print("-" * 80)

    await run_session(
        automated_runner,
        "My nephew's name is Liam and he loves cars.",
        session_id="additional-info",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Demo 5: Fourth conversation - Test comprehensive memory
    print("\n" + "-" * 80)
    print("DEMO 5: Fourth conversation - Ask comprehensive question")
    print("-" * 80)

    await run_session(
        automated_runner,
        "Tell me everything you know about my nephew.",
        session_id="comprehensive-recall",
        user_id=USER_ID,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Show final memory state
    print("\n" + "-" * 80)
    print("Final Memory State")
    print("-" * 80)

    await display_memory_contents(memory_service, APP_NAME, USER_ID, max_display=10)

    # Demo 6: Callback workflow explanation
    print("\n" + "-" * 80)
    print("DEMO 6: How callbacks work")
    print("-" * 80)
    print()
    print("Callback Execution Flow:")
    print()
    print("  User sends message")
    print("       ↓")
    print("  Agent processes (LLM call, tool use, etc.)")
    print("       ↓")
    print("  Agent generates response")
    print("       ↓")
    print("  after_agent_callback TRIGGERS ⚡")
    print("       ↓")
    print("  auto_save_to_memory() executes")
    print("       ↓")
    print("  Session data → Memory storage ✅")
    print()
    print("This happens automatically after EVERY agent turn!")

    # Summary
    print("\n" + "=" * 80)
    print("✅ Automated Memory Management Complete!")
    print("=" * 80)
    print()
    print("Complete Automation Achieved:")
    print()
    print("  ✅ Storage: after_agent_callback → auto-saves every turn")
    print("  ✅ Retrieval: preload_memory → auto-loads every turn")
    print("  ✅ Result: Zero manual memory management!")
    print()
    print("Production Benefits:")
    print("  • No forgetting to save important conversations")
    print("  • Consistent memory access across all sessions")
    print("  • Reduced development complexity")
    print("  • Scalable for multi-user systems")
    print()
    print("When to save to memory:")
    print("  • After every turn → Real-time updates (this example)")
    print("  • End of conversation → Batch processing")
    print("  • Periodic intervals → Long-running chats")
    print()
    print("Day 3b Complete! 🎉")
    print("Next: Day 4 - Observability and Evaluation")
    print()


if __name__ == "__main__":
    asyncio.run(demo_automated_memory())
