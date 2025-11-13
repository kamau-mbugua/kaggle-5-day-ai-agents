"""
Example 1: Stateful Agent with InMemorySessionService

Demonstrates:
- Building an agent that remembers conversation history
- Using InMemorySessionService for temporary storage
- How sessions maintain context across multiple queries

Key Concept:
Session = Container for conversation history
Events = Individual messages (user input, agent response, tool calls)
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from utils import run_session, load_api_key, create_retry_config


# Configuration
APP_NAME = "stateful_demo"
USER_ID = "demo_user"
MODEL_NAME = "gemini-2.5-flash-lite"


async def demo_stateful_agent():
    """Demonstrate how sessions maintain conversation context."""

    print("\n" + "="*80)
    print("🧠 STATEFUL AGENT - Memory with InMemorySessionService")
    print("="*80 + "\n")

    # Step 1: Load API key
    load_api_key()

    # Step 2: Configure retry logic
    retry_config = create_retry_config()

    # Step 3: Create the agent
    print("🤖 Creating stateful agent...")
    root_agent = Agent(
        model=Gemini(model=MODEL_NAME, retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot that remembers conversation history"
    )
    print("✅ Agent created!\n")

    # Step 4: Set up InMemorySessionService
    # This stores conversations in RAM (temporary - lost on restart)
    print("💾 Setting up session management...")
    session_service = InMemorySessionService()
    print("✅ Using InMemorySessionService (temporary storage)\n")

    # Step 5: Create the Runner
    # The Runner orchestrates the conversation and maintains history
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("📋 Configuration:")
    print(f"   - Application: {APP_NAME}")
    print(f"   - User: {USER_ID}")
    print(f"   - Model: {MODEL_NAME}")
    print(f"   - Storage: InMemorySessionService (temporary)")
    print()

    # DEMO 1: First conversation - Agent learns information
    print("\n" + "="*80)
    print("DEMO 1: First Conversation - Introduction")
    print("="*80)

    await run_session(
        runner,
        [
            "Hi, I am Sam! What is the capital of the United States?",
            "Hello! What is my name?",  # Agent should remember from previous message
        ],
        "stateful-session-demo",
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   The agent remembered your name because both queries were in the SAME session.")
    print("   The Runner automatically maintained the conversation history.")

    # DEMO 2: Same session, continued conversation
    print("\n" + "="*80)
    print("DEMO 2: Continuing the Conversation")
    print("="*80)

    await run_session(
        runner,
        [
            "What did we talk about in the first message?",
            "Can you remind me which capital I asked about?"
        ],
        "stateful-session-demo",  # Same session ID
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   By using the same session_id, the agent has access to the full history.")
    print("   It can refer back to earlier parts of the conversation.")

    # DEMO 3: New session - Agent forgets
    print("\n" + "="*80)
    print("DEMO 3: New Session - Fresh Start")
    print("="*80)

    await run_session(
        runner,
        [
            "Hi! What's my name?",
            "What did we discuss earlier?"
        ],
        "new-isolated-session",  # Different session ID
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   With a NEW session_id, the agent has no memory of the previous conversation.")
    print("   Each session is isolated and independent.")

    # Summary
    print("\n" + "="*80)
    print("📊 Summary - Session Management")
    print("="*80)
    print()
    print("✅ Session = Container for a conversation")
    print("✅ Same session_id = Agent remembers history")
    print("✅ Different session_id = Fresh start, no memory")
    print("✅ InMemorySessionService = Temporary (lost on restart)")
    print()
    print("⚠️  Limitation:")
    print("   InMemorySessionService is great for testing, but conversations")
    print("   are lost when the application restarts.")
    print()
    print("💡 Next Step:")
    print("   Run example 2 to see persistent storage with DatabaseSessionService!")
    print("="*80 + "\n")


async def main():
    """Main function."""
    try:
        await demo_stateful_agent()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
