"""
Example 2: Persistent Sessions with DatabaseSessionService

Demonstrates:
- Upgrading from temporary to persistent storage
- Using SQLite database for session persistence
- Conversations that survive application restarts
- Session isolation and privacy

Key Concept:
DatabaseSessionService = Sessions persist across restarts
Sessions are isolated per user and application
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner

from utils import run_session, load_api_key, create_retry_config


# Configuration
APP_NAME = "persistent_demo"
USER_ID = "demo_user"
MODEL_NAME = "gemini-2.5-flash-lite"
DB_PATH = "agent_sessions.db"


async def demo_persistent_sessions():
    """Demonstrate persistent session storage with SQLite."""

    print("\n" + "="*80)
    print("💾 PERSISTENT SESSIONS - DatabaseSessionService")
    print("="*80 + "\n")

    # Step 1: Load API key
    load_api_key()

    # Step 2: Configure retry logic
    retry_config = create_retry_config()

    # Step 3: Create the agent
    print("🤖 Creating chatbot agent...")
    chatbot_agent = LlmAgent(
        model=Gemini(model=MODEL_NAME, retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot with persistent memory",
    )
    print("✅ Agent created!\n")

    # Step 4: Upgrade to DatabaseSessionService
    # SQLite database will be created automatically
    print("💾 Setting up persistent storage...")
    db_url = f"sqlite:///{DB_PATH}"
    session_service = DatabaseSessionService(db_url=db_url)
    print(f"✅ Using DatabaseSessionService")
    print(f"   Database: {DB_PATH}")
    print(f"   Sessions will survive restarts!\n")

    # Step 5: Create Runner with persistent storage
    runner = Runner(
        agent=chatbot_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("📋 Configuration:")
    print(f"   - Application: {APP_NAME}")
    print(f"   - User: {USER_ID}")
    print(f"   - Model: {MODEL_NAME}")
    print(f"   - Storage: DatabaseSessionService (persistent)")
    print()

    # DEMO 1: First conversation - Store information
    print("\n" + "="*80)
    print("DEMO 1: First Conversation - Storing Information")
    print("="*80)

    await run_session(
        runner,
        [
            "Hi, I am Sam! What is the capital of the United States?",
            "Hello! What is my name?"
        ],
        "test-db-session-01",
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   The conversation is now stored in the SQLite database.")
    print("   This session will survive application restarts!")

    # DEMO 2: Continue the conversation
    print("\n" + "="*80)
    print("DEMO 2: Continuing Previous Conversation")
    print("="*80)

    await run_session(
        runner,
        [
            "What is the capital of India?",
            "Hello! What is my name again?"
        ],
        "test-db-session-01",  # Same session ID
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   The agent still remembers your name from the first demo!")
    print("   The database preserves full conversation history.")

    # DEMO 3: Isolated sessions
    print("\n" + "="*80)
    print("DEMO 3: Session Isolation - Different Session")
    print("="*80)

    await run_session(
        runner,
        ["Hello! What is my name?"],
        "test-db-session-02",  # Different session ID
        USER_ID,
        MODEL_NAME
    )

    print("\n💡 Key Insight:")
    print("   With a different session_id, the agent has no memory.")
    print("   Sessions are completely isolated from each other.")

    # DEMO 4: Inspect the database
    print("\n" + "="*80)
    print("DEMO 4: Database Inspection")
    print("="*80)

    inspect_database(DB_PATH)

    # Summary
    print("\n" + "="*80)
    print("📊 Summary - Persistent Sessions")
    print("="*80)
    print()
    print("✅ DatabaseSessionService stores sessions permanently")
    print("✅ Conversations survive application restarts")
    print("✅ Sessions remain isolated per session_id")
    print("✅ SQLite provides simple, self-contained storage")
    print()
    print("🎯 Production Use Cases:")
    print("   - Customer support chatbots")
    print("   - Personal assistants")
    print("   - Multi-turn research agents")
    print("   - Any application requiring conversation history")
    print()
    print("💡 Next Step:")
    print("   Run example 3 to see context compaction for long conversations!")
    print("="*80 + "\n")


def inspect_database(db_path: str):
    """Inspect the SQLite database to show stored events."""
    import sqlite3

    print("\n🔍 Inspecting Database Contents:")
    print("-" * 80)

    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()

            # Get column names
            result = cursor.execute(
                "SELECT app_name, session_id, author, content FROM events"
            )

            print(f"\n{'App Name':<20} {'Session ID':<25} {'Author':<20} {'Content Preview':<50}")
            print("-" * 115)

            # Fetch and display rows
            for row in result.fetchall():
                app_name, session_id, author, content = row

                # Truncate content for display
                content_preview = content[:50] + "..." if len(content) > 50 else content
                print(f"{app_name:<20} {session_id:<25} {author:<20} {content_preview:<50}")

            print("-" * 115)

            # Count events
            count_result = cursor.execute("SELECT COUNT(*) FROM events").fetchone()
            print(f"\n📊 Total events stored: {count_result[0]}")

    except Exception as e:
        print(f"❌ Error inspecting database: {e}")

    print()


async def main():
    """Main function."""
    try:
        await demo_persistent_sessions()

        print("\n" + "="*80)
        print("🔄 Testing Persistence")
        print("="*80)
        print()
        print("To test that sessions truly persist:")
        print("1. Stop this script (Ctrl+C)")
        print("2. Run it again")
        print("3. The agent will still remember your name!")
        print()
        print(f"The session data is stored in: {DB_PATH}")
        print("="*80 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
