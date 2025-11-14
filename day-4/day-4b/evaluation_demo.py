"""
Interactive Demo - Agent Evaluation

A menu-driven interface to explore all evaluation concepts:
1. Basic Evaluation Setup (metrics and workflow)
2. Creating Test Cases (evalsets and configs)
3. Running Evaluations (CLI commands)
4. Analyzing and Fixing Failures (debugging workflow)
5. Create Home Agent (hands-on practice)

Run this script to interactively explore each pattern.
"""

import asyncio
import sys
import os
import subprocess

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from examples.example_1_basic_evaluation import demo_basic_evaluation
from examples.example_2_test_cases import demo_test_cases
from examples.example_3_running_evaluations import demo_running_evaluations
from examples.example_4_analysis_and_fixes import demo_analysis_and_fixes


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 80)
    print("     ______            __            __  _            ")
    print("    / ____/   ______ _/ /_  ______ _/ /_(_)___  ____  ")
    print("   / __/ | | / / __ `/ / / / / __ `/ __/ / __ \\/ __ \\ ")
    print("  / /___ | |/ / /_/ / / /_/ / /_/ / /_/ / /_/ / / / / ")
    print(" /_____/ |___/\\__,_/_/\\__,_/\\__,_/\\__/_/\\____/_/ /_/  ")
    print("=" * 80)
    print()
    print("                🧪 Agent Evaluation - Day 4b")
    print()
    print("        Learn to test, measure, and improve your agents!")
    print()
    print("=" * 80)


def print_menu():
    """Print main menu."""
    print("\n" + "=" * 80)
    print()
    print("🧪 Choose which evaluation pattern to explore:")
    print()
    print("   1. Basic Evaluation Setup (Concepts & Metrics)")
    print("   2. Creating Test Cases (Evalsets & Config)")
    print("   3. Running Evaluations (CLI & Results)")
    print("   4. Analyzing and Fixing Failures (Debug Workflow)")
    print("   5. Create Home Automation Agent (Hands-on)")
    print("   6. Run All Demos (Full Tour)")
    print("   7. Exit")
    print()
    print("=" * 80)


async def run_demo(choice: str):
    """Run the selected demo."""

    if choice == "1":
        print("\n⏳ Running Basic Evaluation Setup Demo...")
        print("=" * 80 + "\n")
        await demo_basic_evaluation()

    elif choice == "2":
        print("\n⏳ Running Creating Test Cases Demo...")
        print("=" * 80 + "\n")
        await demo_test_cases()

    elif choice == "3":
        print("\n⏳ Running Running Evaluations Demo...")
        print("=" * 80 + "\n")
        await demo_running_evaluations()

    elif choice == "4":
        print("\n⏳ Running Analysis and Fixes Demo...")
        print("=" * 80 + "\n")
        await demo_analysis_and_fixes()

    elif choice == "5":
        print("\n⏳ Creating Home Automation Agent...")
        print("=" * 80 + "\n")
        # Run the create_home_agent.py script
        result = subprocess.run(
            [sys.executable, "create_home_agent.py"],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

    elif choice == "6":
        print("\n⏳ Running All Demos (Full Tour)...")
        print("=" * 80 + "\n")

        print("\n" + "🧪 " * 20)
        print("DEMO 1: Basic Evaluation Setup")
        print("🧪 " * 20 + "\n")
        await demo_basic_evaluation()

        print("\n" + "🧪 " * 20)
        print("DEMO 2: Creating Test Cases")
        print("🧪 " * 20 + "\n")
        await demo_test_cases()

        print("\n" + "🧪 " * 20)
        print("DEMO 3: Running Evaluations")
        print("🧪 " * 20 + "\n")
        await demo_running_evaluations()

        print("\n" + "🧪 " * 20)
        print("DEMO 4: Analyzing and Fixing Failures")
        print("🧪 " * 20 + "\n")
        await demo_analysis_and_fixes()

        print("\n" + "🧪 " * 20)
        print("DEMO 5: Create Home Automation Agent")
        print("🧪 " * 20 + "\n")
        result = subprocess.run(
            [sys.executable, "create_home_agent.py"],
            capture_output=True,
            text=True,
        )
        print(result.stdout)

        print("\n" + "=" * 80)
        print("🎉 All Demos Complete!")
        print("=" * 80)
        print()
        print("You've explored all evaluation patterns!")
        print("Check the README.md for more detailed information.")
        print("=" * 80 + "\n")

    else:
        print("\n❌ Invalid choice. Please select 1-7.")


async def main():
    """Main interactive loop."""
    print_banner()

    print("\n📖 About Agent Evaluation")
    print("=" * 80)
    print()
    print("Unlike traditional software, AI agents need special testing approaches:")
    print()
    print("  ❌ Traditional: divide(10, 0) → ZeroDivisionError (clear)")
    print("  ❓ AI Agent: 'Find papers' → ??? (how to measure quality?)")
    print()
    print("Evaluation provides systematic quality measurement:")
    print()
    print("  ✅ response_match_score: Text similarity (0.0-1.0)")
    print("  ✅ tool_trajectory_avg_score: Tool usage correctness (0.0-1.0)")
    print("  ✅ Automated testing with adk eval CLI")
    print("  ✅ Catch regressions before deployment")
    print()
    print("In this demo, you'll learn:")
    print()
    print("  🧪 Evaluation Metrics: Response match + tool trajectory")
    print("  📝 Test Cases: Creating evalsets and configs")
    print("  🏃 Running Evals: Using adk eval CLI")
    print("  🔍 Debugging: Analyze failures and apply fixes")
    print()
    print("=" * 80)

    while True:
        print_menu()

        try:
            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == "7":
                print("\n" + "=" * 80)
                print("👋 Thanks for exploring agent evaluation!")
                print("=" * 80)
                print()
                print("Next Steps:")
                print("  - Read the full documentation in README.md")
                print("  - Explore the example files in examples/")
                print("  - Create your home automation agent")
                print("  - Run evaluations and practice debugging")
                print()
                print("Next Course Day: Day 5 - Advanced Topics")
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
        print("Note: Examples 1-4 don't require API calls, but you'll need")
        print("the key for creating and evaluating the home automation agent.")
        print()
        print("=" * 80 + "\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
