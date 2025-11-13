"""
Interactive Demo - Memory Management

A menu-driven interface to explore all memory management concepts:
1. Manual Memory Storage (add_session_to_memory)
2. Reactive Memory Retrieval (load_memory tool)
3. Proactive Memory Retrieval (preload_memory tool)
4. Automated Memory with Callbacks

Run this script to interactively explore each pattern.
"""

import asyncio
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from examples.example_1_manual_memory import demo_manual_memory
from examples.example_2_reactive_memory import demo_reactive_memory
from examples.example_3_proactive_memory import demo_proactive_memory
from examples.example_4_automated_memory import demo_automated_memory


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 80)
    print("  __  __                                __  __                                             _   ")
    print(" |  \\/  | ___  _ __ ___    ___   _ __  _   _  |  \\/  | __ _  _ _   __ _  __ _  ___  _ __   ___  _ _  | |_ ")
    print(" | |\\/| |/ _ \\| '_ ` _ \\  / _ \\ | '__|| | | | | |\\/| |/ _` || ' \\ / _` |/ _` |/ _ \\| '  \\ / _ \\| ' \\ |  _|")
    print(" | |  | |  __/| | | | | || (_) || |   | |_| | | |  | | (_| || | || (_| || (_| |\\__/ || |_| || |_| || | || |_|")
    print(" |_|  |_|\\___||_| |_| |_| \\___/ |_|    \\__, | |_|  |_|\\__,_||_|_| \\__,_| \\__, |\\___||_||_| \\___||_||_| \\__|")
    print("                                       |___/                              |___/                            ")
    print("=" * 80)
    print()
    print("                🧠 Agent Memory - Day 3b")
    print()
    print("         Learn how to build agents with long-term memory!")
    print()
    print("=" * 80)


def print_menu():
    """Print main menu."""
    print("\n" + "=" * 80)
    print()
    print("🧠 Choose which memory pattern to explore:")
    print()
    print("   1. Manual Memory Storage (add_session_to_memory)")
    print("   2. Reactive Memory Retrieval (load_memory tool)")
    print("   3. Proactive Memory Retrieval (preload_memory tool)")
    print("   4. Automated Memory with Callbacks")
    print("   5. Run All Demos (Full Tour)")
    print("   6. Exit")
    print()
    print("=" * 80)


async def run_demo(choice: str):
    """Run the selected demo."""

    if choice == "1":
        print("\n⏳ Running Manual Memory Storage Demo...")
        print("=" * 80 + "\n")
        await demo_manual_memory()

    elif choice == "2":
        print("\n⏳ Running Reactive Memory Retrieval Demo...")
        print("=" * 80 + "\n")
        await demo_reactive_memory()

    elif choice == "3":
        print("\n⏳ Running Proactive Memory Retrieval Demo...")
        print("=" * 80 + "\n")
        await demo_proactive_memory()

    elif choice == "4":
        print("\n⏳ Running Automated Memory with Callbacks Demo...")
        print("=" * 80 + "\n")
        await demo_automated_memory()

    elif choice == "5":
        print("\n⏳ Running All Demos (Full Tour)...")
        print("=" * 80 + "\n")

        print("\n" + "🧠 " * 20)
        print("DEMO 1: Manual Memory Storage")
        print("🧠 " * 20 + "\n")
        await demo_manual_memory()

        print("\n" + "🧠 " * 20)
        print("DEMO 2: Reactive Memory Retrieval")
        print("🧠 " * 20 + "\n")
        await demo_reactive_memory()

        print("\n" + "🧠 " * 20)
        print("DEMO 3: Proactive Memory Retrieval")
        print("🧠 " * 20 + "\n")
        await demo_proactive_memory()

        print("\n" + "🧠 " * 20)
        print("DEMO 4: Automated Memory with Callbacks")
        print("🧠 " * 20 + "\n")
        await demo_automated_memory()

        print("\n" + "=" * 80)
        print("🎉 All Demos Complete!")
        print("=" * 80)
        print()
        print("You've explored all memory management patterns!")
        print("Check the README.md for more detailed information.")
        print("=" * 80 + "\n")

    else:
        print("\n❌ Invalid choice. Please select 1-6.")


async def main():
    """Main interactive loop."""
    print_banner()

    print("\n📖 About Memory Management")
    print("=" * 80)
    print()
    print("Sessions provide short-term memory for single conversations.")
    print("Memory provides long-term knowledge storage across conversations.")
    print()
    print("Key Differences:")
    print()
    print("  Session = Temporary conversation history (this chat)")
    print("  Memory  = Persistent knowledge base (all past chats)")
    print()
    print("In this demo, you'll learn:")
    print()
    print("  ✅ How to transfer session data to long-term memory")
    print("  ✅ How to retrieve memories with load_memory (reactive)")
    print("  ✅ How to auto-load memories with preload_memory (proactive)")
    print("  ✅ How to automate everything with callbacks")
    print()
    print("=" * 80)

    while True:
        print_menu()

        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "6":
                print("\n" + "=" * 80)
                print("👋 Thanks for exploring memory management!")
                print("=" * 80)
                print()
                print("Next Steps:")
                print("  - Read the full documentation in README.md")
                print("  - Explore the example files in examples/")
                print("  - Try modifying the examples for your use case")
                print()
                print("Next Course Day: Day 4 - Observability & Evaluation")
                print()
                print("Happy agent building! 🤖")
                print("=" * 80 + "\n")
                break

            await run_demo(choice)

        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("👋 Goodbye!")
            print("=" * 80 + "\n")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nPlease try again or press Ctrl+C to exit.")


if __name__ == "__main__":
    # Check for .env file
    if not os.path.exists(".env"):
        print("\n" + "=" * 80)
        print("⚠️  WARNING: .env file not found!")
        print("=" * 80)
        print()
        print("Before running the demos, you need to:")
        print("1. Copy .env.example to .env")
        print("2. Add your GOOGLE_API_KEY to .env")
        print("3. Get your key from: https://aistudio.google.com/app/apikey")
        print()
        print("=" * 80 + "\n")
        sys.exit(1)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
