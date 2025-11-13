"""
Interactive Demo - Session Management

A menu-driven interface to explore all session management concepts:
1. Stateful Agent (InMemorySessionService)
2. Persistent Sessions (DatabaseSessionService)
3. Context Compaction (EventsCompactionConfig)
4. Session State Management (Custom Tools)

Run this script to interactively explore each pattern.
"""

import asyncio
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from examples.example_1_stateful_agent import demo_stateful_agent
from examples.example_2_persistent_sessions import demo_persistent_sessions
from examples.example_3_context_compaction import demo_context_compaction
from examples.example_4_session_state import demo_session_state


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*80)
    print("  ___                _               __  __                                             _   ")
    print(" / __| ___  ___ ___ (_) ___  _ _    |  \\/  | __ _  _ _   __ _  __ _  ___  _ __   ___  _ _  | |_ ")
    print(" \\__ \\/ -_)(_-<(_-< | |/ _ \\| ' \\   | |\\/| |/ _` || ' \\ / _` |/ _` |/ -_)| '  \\ / -_)| ' \\ |  _|")
    print(" |___/\\___|/__//__/ |_|\\___/|_||_|  |_|  |_|\\__,_||_||_|\\__,_|\\__, |\\___||_|_|_|\\___||_||_| \\__|")
    print("                                                               |___/                            ")
    print("="*80)
    print()
    print("                📋 Agent Sessions - Day 3a")
    print()
    print("         Learn how to build stateful AI agents with memory!")
    print()
    print("="*80)


def print_menu():
    """Print main menu."""
    print("\n" + "="*80)
    print()
    print("📋 Choose which pattern to explore:")
    print()
    print("   1. Stateful Agent (InMemorySessionService)")
    print("   2. Persistent Sessions (DatabaseSessionService)")
    print("   3. Context Compaction (EventsCompactionConfig)")
    print("   4. Session State Management (Custom Tools)")
    print("   5. Run All Demos (Full Tour)")
    print("   6. Exit")
    print()
    print("="*80)


async def run_demo(choice: str):
    """Run the selected demo."""

    if choice == "1":
        print("\n⏳ Running Stateful Agent Demo...")
        print("="*80 + "\n")
        await demo_stateful_agent()

    elif choice == "2":
        print("\n⏳ Running Persistent Sessions Demo...")
        print("="*80 + "\n")
        await demo_persistent_sessions()

    elif choice == "3":
        print("\n⏳ Running Context Compaction Demo...")
        print("="*80 + "\n")
        await demo_context_compaction()

    elif choice == "4":
        print("\n⏳ Running Session State Management Demo...")
        print("="*80 + "\n")
        await demo_session_state()

    elif choice == "5":
        print("\n⏳ Running All Demos (Full Tour)...")
        print("="*80 + "\n")

        print("\n" + "🎬 "*20)
        print("DEMO 1: Stateful Agent")
        print("🎬 "*20 + "\n")
        await demo_stateful_agent()

        print("\n" + "🎬 "*20)
        print("DEMO 2: Persistent Sessions")
        print("🎬 "*20 + "\n")
        await demo_persistent_sessions()

        print("\n" + "🎬 "*20)
        print("DEMO 3: Context Compaction")
        print("🎬 "*20 + "\n")
        await demo_context_compaction()

        print("\n" + "🎬 "*20)
        print("DEMO 4: Session State Management")
        print("🎬 "*20 + "\n")
        await demo_session_state()

        print("\n" + "="*80)
        print("🎉 All Demos Complete!")
        print("="*80)
        print()
        print("You've explored all session management patterns!")
        print("Check the README.md for more detailed information.")
        print("="*80 + "\n")

    else:
        print("\n❌ Invalid choice. Please select 1-6.")


async def main():
    """Main interactive loop."""
    print_banner()

    print("\n📖 About Session Management")
    print("="*80)
    print()
    print("Large Language Models are stateless by default. They only see")
    print("what you send in a single API call. Sessions solve this problem")
    print("by maintaining conversation history and context.")
    print()
    print("In this demo, you'll learn:")
    print()
    print("  ✅ How to build stateful agents that remember conversations")
    print("  ✅ How to persist sessions across application restarts")
    print("  ✅ How to optimize long conversations with context compaction")
    print("  ✅ How to manage structured data with session state")
    print()
    print("="*80)

    while True:
        print_menu()

        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "6":
                print("\n" + "="*80)
                print("👋 Thanks for exploring session management!")
                print("="*80)
                print()
                print("Next Steps:")
                print("  - Read the full documentation in README.md")
                print("  - Explore the example files in examples/")
                print("  - Try modifying the examples for your use case")
                print()
                print("Happy agent building! 🤖")
                print("="*80 + "\n")
                break

            await run_demo(choice)

        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("👋 Goodbye!")
            print("="*80 + "\n")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nPlease try again or press Ctrl+C to exit.")


if __name__ == "__main__":
    # Check for .env file
    if not os.path.exists(".env"):
        print("\n" + "="*80)
        print("⚠️  WARNING: .env file not found!")
        print("="*80)
        print()
        print("Before running the demos, you need to:")
        print("1. Copy .env.example to .env")
        print("2. Add your GOOGLE_API_KEY to .env")
        print("3. Get your key from: https://aistudio.google.com/app/apikey")
        print()
        print("="*80 + "\n")
        sys.exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
