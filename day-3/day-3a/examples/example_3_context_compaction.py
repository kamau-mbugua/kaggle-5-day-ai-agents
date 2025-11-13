"""
Example 3: Context Compaction for Long Conversations

Demonstrates:
- EventsCompactionConfig for automatic history summarization
- Reducing context size while maintaining conversation coherence
- Configuring compaction interval and overlap size
- How compaction improves performance and reduces costs

Key Concept:
Context Compaction = Automatically summarize old conversation history
Keeps recent context + summary of older messages
Reduces token usage for long conversations
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner

from utils import run_session, load_api_key, create_retry_config


# Configuration
APP_NAME = "compaction_demo"
USER_ID = "demo_user"
MODEL_NAME = "gemini-2.5-flash-lite"
DB_PATH = "agent_compaction.db"


async def demo_context_compaction():
    """Demonstrate automatic context compaction for long conversations."""

    print("\n" + "="*80)
    print("📦 CONTEXT COMPACTION - Automatic History Summarization")
    print("="*80 + "\n")

    # Step 1: Load API key
    load_api_key()

    # Step 2: Configure retry logic
    retry_config = create_retry_config()

    # Step 3: Create the agent
    print("🤖 Creating chatbot agent...")
    chatbot_agent = LlmAgent(
        model=Gemini(model=MODEL_NAME, retry_options=retry_config),
        name="research_agent",
        description="A research assistant with context compaction",
    )
    print("✅ Agent created!\n")

    # Step 4: Create App with EventsCompactionConfig
    print("📦 Configuring context compaction...")
    research_app = App(
        name=APP_NAME,
        root_agent=chatbot_agent,
        # Configure automatic compaction
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # Trigger compaction every 3 turns
            overlap_size=1,  # Keep 1 previous turn for context
        ),
    )
    print("✅ Compaction configured:")
    print("   - Compaction interval: Every 3 turns")
    print("   - Overlap size: 1 turn")
    print()

    # Step 5: Set up database and runner
    print("💾 Setting up persistent storage...")
    db_url = f"sqlite:///{DB_PATH}"
    session_service = DatabaseSessionService(db_url=db_url)
    print(f"✅ Database: {DB_PATH}\n")

    # Create Runner with the App (not just agent)
    runner = Runner(
        app=research_app,
        session_service=session_service
    )

    print("📋 Configuration:")
    print(f"   - Application: {APP_NAME}")
    print(f"   - User: {USER_ID}")
    print(f"   - Model: {MODEL_NAME}")
    print(f"   - Compaction: Enabled (every 3 turns)")
    print()

    # DEMO: Long conversation that triggers compaction
    print("\n" + "="*80)
    print("DEMO: Long Conversation with Automatic Compaction")
    print("="*80)
    print()
    print("We'll have a 4-turn conversation.")
    print("After Turn 3, compaction will automatically trigger.")
    print("The agent will still maintain context while using less memory.")
    print()

    # Turn 1
    print("\n--- Turn 1 ---")
    await run_session(
        runner,
        "What is the latest news about AI in healthcare?",
        "compaction-demo-session",
        USER_ID,
        MODEL_NAME
    )

    # Turn 2
    print("\n--- Turn 2 ---")
    await run_session(
        runner,
        "Are there any new developments in drug discovery?",
        "compaction-demo-session",
        USER_ID,
        MODEL_NAME
    )

    # Turn 3 - Compaction should trigger after this!
    print("\n--- Turn 3 (Compaction will trigger after this) ---")
    await run_session(
        runner,
        "Tell me more about the second development you found.",
        "compaction-demo-session",
        USER_ID,
        MODEL_NAME
    )

    print("\n🔄 Compaction triggered! Old history summarized.")

    # Turn 4 - Agent uses summarized history
    print("\n--- Turn 4 (Using compacted history) ---")
    await run_session(
        runner,
        "Who are the main companies involved in that?",
        "compaction-demo-session",
        USER_ID,
        MODEL_NAME
    )

    # Verify compaction
    print("\n" + "="*80)
    print("🔍 Verifying Compaction")
    print("="*80)

    await verify_compaction(session_service, runner, USER_ID)

    # Summary
    print("\n" + "="*80)
    print("📊 Summary - Context Compaction")
    print("="*80)
    print()
    print("✅ Automatic summarization of conversation history")
    print("✅ Reduces token usage for long conversations")
    print("✅ Maintains conversation coherence")
    print("✅ Improves performance and reduces costs")
    print()
    print("🎯 How It Works:")
    print("   1. Agent has a normal conversation")
    print("   2. After N turns (compaction_interval), old history is summarized")
    print("   3. Summary replaces detailed history")
    print("   4. Recent turns (overlap_size) are kept for context")
    print()
    print("💰 Benefits:")
    print("   - Reduced API costs (fewer tokens)")
    print("   - Faster response times")
    print("   - Support for longer conversations")
    print("   - Automatic - no manual intervention needed")
    print()
    print("💡 Next Step:")
    print("   Run example 4 to see session state management!")
    print("="*80 + "\n")


async def verify_compaction(session_service, runner, user_id):
    """Verify that compaction occurred by inspecting the session."""

    print("\n📋 Searching for compaction event in session history...")

    # Get the session
    final_session = await session_service.get_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id="compaction-demo-session",
    )

    print(f"📊 Total events in session: {len(final_session.events)}")

    # Look for compaction event
    found_compaction = False
    for i, event in enumerate(final_session.events):
        if event.actions and event.actions.compaction:
            found_compaction = True
            print(f"\n✅ Compaction Event Found (Event #{i + 1}):")
            print(f"   Author: {event.author}")
            print(f"   Invocation ID: {event.invocation_id}")

            # Extract compacted content preview
            compacted_data = event.actions.compaction
            if "compacted_content" in compacted_data:
                content = compacted_data["compacted_content"]
                if "parts" in content and len(content["parts"]) > 0:
                    text = content["parts"][0].get("text", "")
                    preview = text[:200] + "..." if len(text) > 200 else text
                    print(f"\n   Compacted Summary Preview:")
                    print(f"   {preview}")
            break

    if not found_compaction:
        print("\n⚠️  No compaction event found yet.")
        print("   Try running more conversation turns to trigger compaction.")


async def main():
    """Main function."""
    try:
        await demo_context_compaction()

        print("\n" + "="*80)
        print("💡 Understanding Compaction")
        print("="*80)
        print()
        print("Without Compaction:")
        print("  Turn 1: 500 tokens")
        print("  Turn 2: 1000 tokens (includes Turn 1)")
        print("  Turn 3: 1500 tokens (includes Turn 1 + 2)")
        print("  Turn 4: 2000 tokens (includes Turn 1 + 2 + 3)")
        print()
        print("With Compaction (interval=3, overlap=1):")
        print("  Turn 1: 500 tokens")
        print("  Turn 2: 1000 tokens")
        print("  Turn 3: 1500 tokens → Compaction triggered!")
        print("  Turn 4: ~800 tokens (summary + Turn 3 + new turn)")
        print()
        print("📉 Result: ~60% token reduction on Turn 4!")
        print("="*80 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
