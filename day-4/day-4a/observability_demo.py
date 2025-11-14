"""
Interactive Demo - Agent Observability

A menu-driven interface to explore all observability concepts:
1. Basic Logging Setup (DEBUG, INFO, WARNING, ERROR)
2. Debugging Broken Agents (symptom → logs → fix workflow)
3. Production Logging with LoggingPlugin
4. Custom Plugins and Callbacks

Run this script to interactively explore each pattern.
"""

import asyncio
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from examples.example_1_basic_logging import demo_basic_logging
from examples.example_2_debugging_broken_agent import demo_debugging_broken_agent
from examples.example_3_production_logging import demo_production_logging
from examples.example_4_custom_plugins import demo_custom_plugins


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 80)
    print("     ____  __                               __    _ ___ __         ")
    print("    / __ \\/ /_  ________  ______   ______ _/ /_  (_) (_) /___  __")
    print("   / / / / __ \\/ ___/ _ \\/ ___/ | / / __ `/ __ \\/ / / / __/ / / /")
    print("  / /_/ / /_/ (__  )  __/ /   | |/ / /_/ / /_/ / / / / /_/ /_/ / ")
    print("  \\____/_.___/____/\\___/_/    |___/\\__,_/_.___/_/_/_/\\__/\\__, /  ")
    print("                                                         /____/   ")
    print("=" * 80)
    print()
    print("                🔍 Agent Observability - Day 4a")
    print()
    print("         Learn to monitor, debug, and optimize your agents!")
    print()
    print("=" * 80)


def print_menu():
    """Print main menu."""
    print("\n" + "=" * 80)
    print()
    print("🔍 Choose which observability pattern to explore:")
    print()
    print("   1. Basic Logging Setup (Log Levels & Configuration)")
    print("   2. Debugging Broken Agents (Find & Fix Issues)")
    print("   3. Production Logging with LoggingPlugin")
    print("   4. Custom Plugins and Callbacks (Advanced)")
    print("   5. Run All Demos (Full Tour)")
    print("   6. Exit")
    print()
    print("=" * 80)


async def run_demo(choice: str):
    """Run the selected demo."""

    if choice == "1":
        print("\n⏳ Running Basic Logging Setup Demo...")
        print("=" * 80 + "\n")
        await demo_basic_logging()

    elif choice == "2":
        print("\n⏳ Running Debugging Broken Agent Demo...")
        print("=" * 80 + "\n")
        await demo_debugging_broken_agent()

    elif choice == "3":
        print("\n⏳ Running Production Logging with LoggingPlugin Demo...")
        print("=" * 80 + "\n")
        await demo_production_logging()

    elif choice == "4":
        print("\n⏳ Running Custom Plugins and Callbacks Demo...")
        print("=" * 80 + "\n")
        await demo_custom_plugins()

    elif choice == "5":
        print("\n⏳ Running All Demos (Full Tour)...")
        print("=" * 80 + "\n")

        print("\n" + "🔍 " * 20)
        print("DEMO 1: Basic Logging Setup")
        print("🔍 " * 20 + "\n")
        await demo_basic_logging()

        print("\n" + "🔍 " * 20)
        print("DEMO 2: Debugging Broken Agents")
        print("🔍 " * 20 + "\n")
        await demo_debugging_broken_agent()

        print("\n" + "🔍 " * 20)
        print("DEMO 3: Production Logging with LoggingPlugin")
        print("🔍 " * 20 + "\n")
        await demo_production_logging()

        print("\n" + "🔍 " * 20)
        print("DEMO 4: Custom Plugins and Callbacks")
        print("🔍 " * 20 + "\n")
        await demo_custom_plugins()

        print("\n" + "=" * 80)
        print("🎉 All Demos Complete!")
        print("=" * 80)
        print()
        print("You've explored all observability patterns!")
        print("Check the README.md for more detailed information.")
        print("=" * 80 + "\n")

    else:
        print("\n❌ Invalid choice. Please select 1-6.")


async def main():
    """Main interactive loop."""
    print_banner()

    print("\n📖 About Agent Observability")
    print("=" * 80)
    print()
    print("Unlike traditional software, AI agents can fail mysteriously:")
    print()
    print("  ❌ \"I cannot help with that request\"  (Why? Tool missing? Bad prompt?)")
    print()
    print("Observability gives you X-ray vision into agent decision-making:")
    print()
    print("  ✅ See exact prompts sent to the LLM")
    print("  ✅ Watch which tools are available")
    print("  ✅ Track how models respond")
    print("  ✅ Identify where failures occur")
    print()
    print("In this demo, you'll learn:")
    print()
    print("  🔍 Logging Levels: DEBUG, INFO, WARNING, ERROR")
    print("  🐛 Debugging: symptom → logs → root cause → fix")
    print("  📊 Production: LoggingPlugin for automated observability")
    print("  🔧 Custom Plugins: Build your own monitoring tools")
    print()
    print("=" * 80)

    while True:
        print_menu()

        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "6":
                print("\n" + "=" * 80)
                print("👋 Thanks for exploring agent observability!")
                print("=" * 80)
                print()
                print("Next Steps:")
                print("  - Read the full documentation in README.md")
                print("  - Explore the example files in examples/")
                print("  - Apply observability to your own agents")
                print()
                print("Next Course Day: Day 4b - Agent Evaluation")
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
