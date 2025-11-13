"""
Example 4: Session State Management with Custom Tools

Demonstrates:
- Using session.state as a key-value store
- Custom tools that read/write session state
- Sharing data across conversation turns
- State isolation between sessions

Key Concept:
Session State = Agent's scratchpad for storing structured data
Available to all tools and subagents
Persists across turns within a session
Isolated per session
"""

import asyncio
import sys
import os
from typing import Any, Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext

from utils import run_session, load_api_key, create_retry_config


# Configuration
APP_NAME = "state_demo"
USER_ID = "demo_user"
MODEL_NAME = "gemini-2.5-flash-lite"


# Custom Tools for Session State Management

def save_userinfo(
    tool_context: ToolContext,
    user_name: str,
    country: str
) -> Dict[str, Any]:
    """
    Tool to record and save user name and country in session state.

    This demonstrates how tools can WRITE to session state.
    Use the 'user:' prefix for user-specific data following best practices.

    Args:
        tool_context: Context providing access to session state
        user_name: The username to store
        country: The user's country

    Returns:
        Dict with status indicating success
    """
    # Write to session state using descriptive key prefixes
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {
        "status": "success",
        "message": f"Saved: name={user_name}, country={country}"
    }


def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve user name and country from session state.

    This demonstrates how tools can READ from session state.

    Args:
        tool_context: Context providing access to session state

    Returns:
        Dict with status and retrieved user information
    """
    # Read from session state with defaults
    user_name = tool_context.state.get("user:name", "Unknown")
    country = tool_context.state.get("user:country", "Unknown")

    return {
        "status": "success",
        "user_name": user_name,
        "country": country
    }


async def demo_session_state():
    """Demonstrate session state management with custom tools."""

    print("\n" + "="*80)
    print("💾 SESSION STATE - Managing Structured Data")
    print("="*80 + "\n")

    # Step 1: Load API key
    load_api_key()

    # Step 2: Configure retry logic
    retry_config = create_retry_config()

    # Step 3: Create agent with state management tools
    print("🤖 Creating agent with session state tools...")
    root_agent = LlmAgent(
        model=Gemini(model=MODEL_NAME, retry_options=retry_config),
        name="state_manager_bot",
        description="""A chatbot with session state management tools.

        Tools for managing user context:
        * To record username and country when provided, use `save_userinfo` tool
        * To fetch username and country when required, use `retrieve_userinfo` tool
        """,
        tools=[save_userinfo, retrieve_userinfo],
    )
    print("✅ Agent created with state management tools!\n")

    # Step 4: Set up session service
    print("💾 Setting up session management...")
    session_service = InMemorySessionService()
    print("✅ Using InMemorySessionService\n")

    # Step 5: Create Runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("📋 Configuration:")
    print(f"   - Application: {APP_NAME}")
    print(f"   - User: {USER_ID}")
    print(f"   - Model: {MODEL_NAME}")
    print(f"   - Tools: save_userinfo, retrieve_userinfo")
    print()

    # DEMO 1: Initial interaction - no state yet
    print("\n" + "="*80)
    print("DEMO 1: Before Saving State")
    print("="*80)

    await run_session(
        runner,
        ["Hi there! What is my name?"],
        "state-demo-session",
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   The agent doesn't know your name yet - no state is stored.")

    # DEMO 2: Save information to state
    print("\n" + "="*80)
    print("DEMO 2: Saving Information to State")
    print("="*80)

    await run_session(
        runner,
        ["My name is Sam. I'm from Poland."],
        "state-demo-session",
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   The agent used save_userinfo tool to store your data in session state.")

    # Inspect state
    print("\n" + "="*80)
    print("🔍 Inspecting Session State")
    print("="*80)

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="state-demo-session"
    )

    print("\nSession State Contents:")
    print("-" * 80)
    for key, value in session.state.items():
        print(f"  {key}: {value}")
    print("-" * 80)
    print("\n✅ Notice the 'user:name' and 'user:country' keys!")

    # DEMO 3: Retrieve from state
    print("\n" + "="*80)
    print("DEMO 3: Retrieving Information from State")
    print("="*80)

    await run_session(
        runner,
        [
            "What is my name?",
            "Which country am I from?"
        ],
        "state-demo-session",
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   The agent used retrieve_userinfo tool to fetch data from session state.")
    print("   The information persists across conversation turns!")

    # DEMO 4: State isolation
    print("\n" + "="*80)
    print("DEMO 4: State Isolation - New Session")
    print("="*80)

    await run_session(
        runner,
        ["Hi! What is my name?"],
        "new-isolated-session",  # Different session
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   With a different session_id, the state is empty.")
    print("   Each session has its own isolated state!")

    # Verify isolation
    print("\n" + "="*80)
    print("🔍 Verifying State Isolation")
    print("="*80)

    new_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="new-isolated-session"
    )

    print("\nNew Session State:")
    print("-" * 80)
    if new_session.state:
        for key, value in new_session.state.items():
            print(f"  {key}: {value}")
    else:
        print("  (empty)")
    print("-" * 80)

    # Summary
    print("\n" + "="*80)
    print("📊 Summary - Session State Management")
    print("="*80)
    print()
    print("✅ Session State = Key-value store for structured data")
    print("✅ Tools can read/write to session.state via ToolContext")
    print("✅ State persists across turns within a session")
    print("✅ Each session has isolated state")
    print()
    print("🎯 Use Cases:")
    print("   - User preferences and settings")
    print("   - Multi-step workflow data")
    print("   - Temporary calculations")
    print("   - Form data collection")
    print("   - User profile information")
    print()
    print("📝 Best Practices:")
    print("   - Use descriptive key prefixes (user:, app:, temp:)")
    print("   - Store structured data, not full conversation history")
    print("   - Clean up temporary data when no longer needed")
    print("   - Document what data your tools store/retrieve")
    print()
    print("💡 Comparison:")
    print("   Session Events  = Full conversation history (messages)")
    print("   Session State   = Structured data (key-value pairs)")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_session_state()

        print("\n" + "="*80)
        print("💡 Session State vs Events")
        print("="*80)
        print()
        print("Events (session.events):")
        print("  - User messages")
        print("  - Agent responses")
        print("  - Tool calls and results")
        print("  - Full conversation flow")
        print("  → Use for: Conversation history, context for LLM")
        print()
        print("State (session.state):")
        print("  - Structured key-value data")
        print("  - User preferences")
        print("  - Workflow variables")
        print("  - Calculated values")
        print("  → Use for: Sharing data between tools, storing facts")
        print()
        print("Both work together to create powerful stateful agents!")
        print("="*80 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
