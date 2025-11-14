"""
Example 2: Creating Test Cases and Evalsets

Demonstrates:
- How to structure evaluation test cases
- Creating evalsets programmatically
- Writing evalset JSON files
- Test case design best practices

Key Pattern:
evalset = create_evalset(
    eval_set_id="suite_name",
    eval_cases=[...]
)
save_evalset(evalset, "path/to/file.evalset.json")

Run:
python examples/example_2_test_cases.py
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    create_evalset,
    create_eval_case,
    save_evalset,
    create_test_config,
    save_test_config,
)


async def demo_test_cases():
    """
    Demonstrate creating test cases and evalsets.

    Shows:
    1. Anatomy of a test case
    2. Creating simple test cases
    3. Creating test cases with tool expectations
    4. Saving evalsets to files
    5. Test case design best practices
    """
    print("\n" + "=" * 80)
    print("Example 2: Creating Test Cases and Evalsets")
    print("=" * 80)

    # Demo 1: Anatomy of a test case
    print("\n" + "-" * 80)
    print("DEMO 1: Anatomy of a Test Case")
    print("-" * 80)
    print()
    print("A test case has three key components:")
    print()
    print("1. eval_id")
    print("   → Unique identifier for this test")
    print('   → Example: "test_turn_on_living_room_lights"')
    print()
    print("2. user_content")
    print("   → The user's input query")
    print('   → Example: "Turn on the living room lights"')
    print()
    print("3. Expected Outcomes")
    print("   a) final_response")
    print("      → What the agent should say")
    print('      → Example: "The living room lights are now on."')
    print()
    print("   b) intermediate_data.tool_uses (optional)")
    print("      → Which tools should be called")
    print("      → What parameters should be used")
    print("      → Example: set_device_status(location='living_room', ...)")
    print()

    # Demo 2: Simple test case (no tools)
    print("-" * 80)
    print("DEMO 2: Create a Simple Test Case (No Tools)")
    print("-" * 80)
    print()
    print("Use Case: Information query that doesn't require tools")
    print()

    simple_case = create_eval_case(
        eval_id="test_info_query",
        user_query="What can you help me with?",
        expected_response="I can help you control smart home devices like lights, thermostats, and more.",
    )

    print("Created test case:")
    print(json.dumps(simple_case, indent=2))
    print()
    print("Notice:")
    print("  • No 'intermediate_data' field")
    print("  • Only response matching will be evaluated")
    print()

    # Demo 3: Test case with tools
    print("-" * 80)
    print("DEMO 3: Create a Test Case with Tool Expectations")
    print("-" * 80)
    print()
    print("Use Case: Action that requires specific tool call")
    print()

    tool_case = create_eval_case(
        eval_id="test_turn_on_lights",
        user_query="Turn on the living room lights",
        expected_response="The living room lights are now on.",
        expected_tools=[
            {
                "name": "set_device_status",
                "args": {
                    "location": "living_room",
                    "device_id": "lights",
                    "status": "on",
                },
            }
        ],
    )

    print("Created test case:")
    print(json.dumps(tool_case, indent=2))
    print()
    print("Notice:")
    print("  • Has 'intermediate_data.tool_uses' field")
    print("  • Specifies exact tool name and arguments")
    print("  • Both response AND tool usage will be evaluated")
    print()

    # Demo 4: Creating a full evalset
    print("-" * 80)
    print("DEMO 4: Create a Complete Evalset")
    print("-" * 80)
    print()
    print("Let's create a comprehensive test suite for home automation...")
    print()

    # Create multiple test cases
    test_cases = [
        # Test 1: Turn on lights
        create_eval_case(
            eval_id="test_turn_on_living_room_lights",
            user_query="Turn on the living room lights",
            expected_response="The living room lights are now on.",
            expected_tools=[
                {
                    "name": "set_device_status",
                    "args": {
                        "location": "living_room",
                        "device_id": "lights",
                        "status": "on",
                    },
                }
            ],
        ),
        # Test 2: Turn off lights
        create_eval_case(
            eval_id="test_turn_off_bedroom_lights",
            user_query="Turn off the bedroom lights",
            expected_response="The bedroom lights are now off.",
            expected_tools=[
                {
                    "name": "set_device_status",
                    "args": {
                        "location": "bedroom",
                        "device_id": "lights",
                        "status": "off",
                    },
                }
            ],
        ),
        # Test 3: Set thermostat
        create_eval_case(
            eval_id="test_set_thermostat_temperature",
            user_query="Set the living room thermostat to 72 degrees",
            expected_response="The living room thermostat has been set to 72 degrees.",
            expected_tools=[
                {
                    "name": "set_device_status",
                    "args": {
                        "location": "living_room",
                        "device_id": "thermostat",
                        "status": "72",
                    },
                }
            ],
        ),
        # Test 4: Multiple devices
        create_eval_case(
            eval_id="test_turn_off_all_kitchen_devices",
            user_query="Turn off all devices in the kitchen",
            expected_response="All kitchen devices have been turned off.",
            expected_tools=[
                {
                    "name": "set_device_status",
                    "args": {
                        "location": "kitchen",
                        "device_id": "lights",
                        "status": "off",
                    },
                }
            ],
        ),
        # Test 5: Info query (no tools)
        create_eval_case(
            eval_id="test_capability_query",
            user_query="What devices can you control?",
            expected_response="I can control lights, thermostats, and other smart home devices in various rooms.",
        ),
    ]

    # Create evalset
    evalset = create_evalset(
        eval_set_id="home_automation_integration_suite", eval_cases=test_cases
    )

    print("✅ Created evalset with 5 test cases:")
    for i, case in enumerate(test_cases, 1):
        eval_id = case["eval_id"]
        has_tools = "intermediate_data" in case["conversation"][0]
        print(f"  {i}. {eval_id} {'(with tools)' if has_tools else '(no tools)'}")
    print()

    # Demo 5: Save evalset to file
    print("-" * 80)
    print("DEMO 5: Save Evalset to File")
    print("-" * 80)
    print()

    # Create demo directory
    demo_dir = Path("demo_agent")
    demo_dir.mkdir(exist_ok=True)

    evalset_path = demo_dir / "integration.evalset.json"
    save_evalset(evalset, str(evalset_path))

    print(f"✅ Saved evalset to: {evalset_path}")
    print()
    print("File structure:")
    print("  demo_agent/")
    print("  └── integration.evalset.json")
    print()

    # Display saved content
    print("Saved content (first test case):")
    with open(evalset_path, "r") as f:
        saved_data = json.load(f)
        first_case = saved_data["eval_cases"][0]
        print(json.dumps(first_case, indent=2))
    print()

    # Demo 6: Create test configuration
    print("-" * 80)
    print("DEMO 6: Create Test Configuration")
    print("-" * 80)
    print()
    print("Test configuration defines pass/fail thresholds...")
    print()

    test_config = create_test_config(
        response_match_threshold=0.8,  # 80% semantic similarity
        tool_trajectory_threshold=1.0,  # Exact tool match
    )

    print("Created test config:")
    print(json.dumps(test_config, indent=2))
    print()

    config_path = demo_dir / "test_config.json"
    save_test_config(test_config, str(config_path))

    print(f"✅ Saved test config to: {config_path}")
    print()
    print("File structure:")
    print("  demo_agent/")
    print("  ├── integration.evalset.json")
    print("  └── test_config.json")
    print()

    # Demo 7: Best practices
    print("-" * 80)
    print("DEMO 7: Test Case Design Best Practices")
    print("-" * 80)
    print()
    print("✅ DO:")
    print()
    print("  1. Use descriptive eval_id names")
    print('     ✅ "test_turn_on_living_room_lights"')
    print('     ❌ "test1"')
    print()
    print("  2. Test one behavior per case")
    print("     ✅ Separate tests for 'turn on' and 'turn off'")
    print("     ❌ Combined test for multiple unrelated actions")
    print()
    print("  3. Cover positive AND negative cases")
    print("     ✅ Test valid inputs AND error scenarios")
    print("     ❌ Only test happy path")
    print()
    print("  4. Use realistic user queries")
    print('     ✅ "Turn on the living room lights"')
    print('     ❌ "execute set_device_status()"')
    print()
    print("  5. Specify exact expected responses")
    print('     ✅ "The living room lights are now on."')
    print('     ❌ "ok" or "success"')
    print()
    print("  6. Include tool parameters")
    print("     ✅ All required args specified")
    print("     ❌ Missing location or device_id")
    print()
    print("❌ DON'T:")
    print()
    print("  • Make tests dependent on each other")
    print("  • Test multiple unrelated behaviors in one case")
    print("  • Use vague expected responses")
    print("  • Forget to test error cases")
    print("  • Hardcode API keys or secrets in evalsets")
    print()

    # Demo 8: Test coverage matrix
    print("-" * 80)
    print("DEMO 8: Test Coverage Matrix")
    print("-" * 80)
    print()
    print("Recommended test categories:")
    print()
    print("┌────────────────────┬─────────────────────────────────────────┐")
    print("│ Category           │ Examples                                │")
    print("├────────────────────┼─────────────────────────────────────────┤")
    print("│ Happy Path         │ Valid inputs, expected tool calls       │")
    print("│ Edge Cases         │ Empty inputs, extreme values            │")
    print("│ Error Handling     │ Invalid locations, unknown devices      │")
    print("│ Multi-step         │ Complex queries requiring reasoning     │")
    print("│ Ambiguous Queries  │ Vague instructions needing clarification│")
    print("│ Tool Selection     │ Right tool chosen from multiple options │")
    print("└────────────────────┴─────────────────────────────────────────┘")
    print()

    # Demo 9: Organizing evalsets
    print("-" * 80)
    print("DEMO 9: Organizing Multiple Evalsets")
    print("-" * 80)
    print()
    print("For larger projects, organize by test type:")
    print()
    print("  agent_directory/")
    print("  ├── agent.py")
    print("  ├── test_config.json              # Shared configuration")
    print("  ├── integration.evalset.json      # End-to-end tests")
    print("  ├── unit.evalset.json             # Individual tool tests")
    print("  ├── regression.evalset.json       # Bug prevention tests")
    print("  └── performance.evalset.json      # Speed/efficiency tests")
    print()
    print("Benefits:")
    print("  • Organize tests by purpose")
    print("  • Run specific test suites")
    print("  • Easier maintenance")
    print()

    # Summary
    print("=" * 80)
    print("✅ Test Case Creation Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print()
    print("  ✅ Test cases = eval_id + user_query + expected outcomes")
    print("  ✅ Use create_eval_case() helper for consistency")
    print("  ✅ Evalsets contain multiple test cases")
    print("  ✅ Test configs define pass/fail thresholds")
    print("  ✅ Follow best practices for maintainable tests")
    print()
    print("Created Files:")
    print(f"  • {evalset_path}")
    print(f"  • {config_path}")
    print()
    print("Next Steps:")
    print("  → Example 3: Run evaluations on these test cases")
    print("  → Example 4: Analyze results and fix failures")
    print()


if __name__ == "__main__":
    asyncio.run(demo_test_cases())
